import os
import sqlite3
import uuid
import csv
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, url_for
import plotly.io as pio
import json
from graphs import aqi_graph, forest, ocean_levels, severe_weather, temperature_graph

import stripe
from agentmail import AgentMail
from solana.rpc.api import Client as SolanaRpcClient
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.system_program import TransferParams, transfer

# Load environment variables first
load_dotenv()

# ✅ Create Flask app BEFORE using any routes
app = Flask(__name__)


# --- CONFIGURATION ---
DB_PATH = 'donations.db'
CSV_FILE = "signups.csv"

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_ENDPOINT_SECRET")
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
AGENTMAIL_API_KEY = os.getenv("AGENTMAIL_API_KEY")

stripe.api_key = STRIPE_SECRET_KEY
SOLANA_RPC = SolanaRpcClient(SOLANA_RPC_URL)
CREATOR_KEYPAIR = Keypair()

# --- DATABASE AND CSV INITIALIZATION ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id TEXT PRIMARY KEY,
            name TEXT,
            cause TEXT,
            amount REAL,
            tracking_tx TEXT,
            solana_tx_signature TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'email'])

init_db()
init_csv()

# --- MOCK DATA ---
mock_climate_data = {
    'global_temperature_anomaly': 1.2,
    'sea_level_rise': 3.5,
    'co2_concentration': 420,
}


# --- HTML PAGE ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/transactions')
def transactions():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT name, cause, amount, solana_tx_signature FROM donations ORDER BY rowid DESC')
    rows = c.fetchall()
    conn.close()
    donation_data = [{'name': r[0], 'cause': r[1], 'amount': r[2], 'solana_tx': r[3]} for r in rows]
    return render_template('transactions.html', donations=donation_data)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

# --- API ROUTES ---
@app.route('/api/donations')
def get_donation_data():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT name, cause, amount FROM donations ORDER BY rowid DESC LIMIT 10')
    rows = c.fetchall()
    c.execute('SELECT SUM(amount) FROM donations')
    total = c.fetchone()[0] or 0
    conn.close()
    recent = [{'name': r[0], 'cause': r[1], 'amount': r[2]} for r in rows]
    return jsonify({'total_donated': total, 'recent_donations': recent})

@app.route('/api/climate')
def get_climate_data():
    return jsonify(mock_climate_data)

@app.route('/api/agentmail')
def get_agentmail_updates():
    try:
        client = AgentMail(api_key=AGENTMAIL_API_KEY)
        threads = client.inboxes.threads.list("betterwater373@agentmail.to", labels=['received'], limit=5)
        updates = [{'subject': t.subject, 'body': t.snippet} for t in threads]
        return jsonify(updates)
    except Exception as e:
        return jsonify([{'subject': 'Error fetching updates', 'body': str(e)}])

# --- PAYMENT AND WEBHOOK LOGIC ---
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    name = data.get('name', 'Anonymous')
    cause = data.get('cause', 'general')
    amount = int(float(data.get('amount', 0)) * 100)

    if amount < 50:
        return jsonify({'error': 'Amount must be at least $0.50'}), 400

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Donation to {cause}'},
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
            metadata={'name': name, 'cause': cause}
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_ENDPOINT_SECRET)
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)

    return jsonify(status='success')

def handle_successful_payment(session):
    name = session['metadata']['name']
    cause = session['metadata']['cause']
    amount = session['amount_total'] / 100.0
    tracking_tx = f"stripe_{session['id']}"

    solana_tx_signature = record_donation_on_solana(name, cause, amount)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT id FROM donations WHERE tracking_tx = ?", (tracking_tx,))
    if c.fetchone() is None:
        c.execute(
            'INSERT INTO donations (id, name, cause, amount, tracking_tx, solana_tx_signature) VALUES (?, ?, ?, ?, ?, ?)',
            (str(uuid.uuid4()), name, cause, amount, tracking_tx, solana_tx_signature)
        )
        conn.commit()
    conn.close()

def record_donation_on_solana(name: str, cause: str, amount: float) -> str:
    try:
        sender = CREATOR_KEYPAIR
        recipient = sender.pubkey()
        lamports = int(amount * 1_000_000_000)
        ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=lamports))
        resp = SOLANA_RPC.get_latest_blockhash()
        blockhash = resp.value.blockhash
        msg = MessageV0.try_compile(
            payer=sender.pubkey(),
            instructions=[ix],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash
        )
        txn = VersionedTransaction(msg, [sender])
        send_resp = SOLANA_RPC.send_transaction(txn)
        sig = send_resp.value
        SOLANA_RPC.confirm_transaction(sig)
        return str(sig)
    except Exception as e:
        print(f"Solana recording error: {e}")
        return "failed_to_record"

# --- EMAIL SIGNUP ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    if not name or not email:
        return jsonify({'status': 'error', 'message': 'Both name and email are required.'}), 400
    with open("./mail/mail_list.txt", "a") as f:
        f.write(email + "\n")
    return jsonify({'status': 'success'})

@app.route('/api/aqi_graph')
def get_aqi():
    return aqi_graph.create_aqi_graph()
@app.route('/api/forest_graph')
def get_forest():
    return forest.create_forest_graph()
@app.route('/api/ocean_levels_graph')
def get_ocean_levels():
    return ocean_levels.create_ocean_levels_graph()
@app.route('/api/temperature_graph')
def get_temperature():
    return temperature_graph.create_temperature_graph()
@app.route('/api/severe_weather_graph')
def get_severe_weather():
    return severe_weather.create_severe_weather_graph()

# --- APP EXECUTION ---
if __name__ == '__main__':
    app.run(debug=True, port=10000)
