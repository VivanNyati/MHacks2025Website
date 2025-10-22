// Wait for the entire HTML document to be loaded and parsed before running any scripts.
document.addEventListener('DOMContentLoaded', () => {
    // --- Initialize Donation Form ---
    const donationForm = document.getElementById('donation-form');
    if (donationForm) {
        // Attach the Stripe payment handler to its submit event.
        donationForm.addEventListener('submit', handleStripeDonation);

        // Add logic to change the image based on the selected cause.
        const causeSelect = document.getElementById('cause');
        const causeImage = document.getElementById('cause-image');
        const causeImages = {
            'disaster-relief': 'https://images.unsplash.com/photo-1593113598332-cd288d649414?q=80&w=2070&auto=format&fit=crop',
            'reforestation': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?q=80&w=2070&auto=format&fit=crop',
            'ocean-cleanup': 'https://images.unsplash.com/photo-1574862806224-c1b7a7833a6f?q=80&w=1974&auto=format&fit=crop'
        };

        causeSelect.addEventListener('change', (event) => {
            if (causeImage) {
                causeImage.style.opacity = 0;
                setTimeout(() => {
                    causeImage.src = causeImages[event.target.value];
                    causeImage.style.opacity = 1;
                }, 400); // Corresponds to the CSS transition time
            }
        });
    }

    // --- Initialize Dashboard ---
    const dashboard = document.querySelector('.dashboard-section');
    if (dashboard) {
        fetchDonationData();
        fetchClimateData();
        fetchAgentMailUpdates();
    }

    // --- Initialize Email Signup Form ---
    const emailForm = document.getElementById('email-signup-form');
    if (emailForm) {
        emailForm.addEventListener('submit', handleEmailSignup);
    }

    // Helper to load and show Plotly graphs
    function fetchAndRenderPlot(endpoint, divId) {
        const graphDiv = document.getElementById(divId);
        if (!graphDiv) return; // Only fetch if the div exists on the page
        
        fetch(endpoint)
            .then(response => response.json())
            .then(graphJSON => {
                let figObj = (typeof graphJSON === "string") ? JSON.parse(graphJSON) : graphJSON;
                Plotly.newPlot(divId, figObj.data, figObj.layout || {});
            })
            .catch(err => {
                console.error("Error rendering Plotly graph for div #" + divId + ":", err);
            });
    }

    // Call once per graph, with the correct div id and endpoint
    fetchAndRenderPlot('/api/temperature_graph', 'temperature-graph');
    fetchAndRenderPlot('/api/severe_weather_graph', 'severe-weather-graph');
    fetchAndRenderPlot('/api/ocean_levels_graph', 'ocean-levels-graph');
    fetchAndRenderPlot('/api/forest_graph', 'forest-graph');
    fetchAndRenderPlot('/api/aqi_graph', 'aqi-graph');
});


/**
 * Handles the Stripe donation process.
 */
async function handleStripeDonation(event) {
    event.preventDefault();
    const donationForm = document.getElementById('donation-form');
    const statusDiv = document.getElementById('donation-status');
    const donateButton = document.getElementById('donate-button');

    const originalButtonText = donateButton.querySelector('.btn-text').textContent;
    donateButton.disabled = true;
    donateButton.querySelector('.btn-text').textContent = 'Processing...';


    const stripeKey = donationForm.dataset.stripeKey;
    if (!stripeKey) {
        statusDiv.textContent = "Configuration error: Stripe key not found.";
        statusDiv.style.color = 'red';
        console.error("Stripe key is missing from the form's data-stripe-key attribute.");
        donateButton.disabled = false;
        donateButton.querySelector('.btn-text').textContent = originalButtonText;
        return;
    }

    const name = document.getElementById('name').value || 'Anonymous';
    const cause = document.getElementById('cause').value;
    const amount = parseFloat(document.getElementById('amount').value);

    if (!amount || amount < 1) {
        statusDiv.textContent = 'Please enter a valid donation amount of at least $1.00.';
        statusDiv.style.color = 'red';
        donateButton.disabled = false;
        donateButton.querySelector('.btn-text').textContent = originalButtonText;
        return;
    }

    statusDiv.textContent = "Creating secure payment session...";
    statusDiv.style.color = 'blue';

    try {
        const response = await fetch('/create-checkout-session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, cause, amount })
        });

        if (!response.ok) {
           throw new Error(`Server error: ${response.statusText}`);
        }

        const session = await response.json();

        if (session.error) {
            statusDiv.textContent = session.error;
            statusDiv.style.color = 'red';
            donateButton.disabled = false;
            donateButton.querySelector('.btn-text').textContent = originalButtonText;
            return;
        }

        const stripe = Stripe(stripeKey);
        const result = await stripe.redirectToCheckout({ sessionId: session.id });

        if (result.error) {
            statusDiv.textContent = result.error.message;
            statusDiv.style.color = 'red';
            donateButton.disabled = false;
            donateButton.querySelector('.btn-text').textContent = originalButtonText;
        }
    } catch (err) {
        console.error('Payment Error:', err);
        statusDiv.textContent = "Error creating payment session. Please try again.";
        statusDiv.style.color = 'red';
        donateButton.disabled = false;
        donateButton.querySelector('.btn-text').textContent = originalButtonText;
    }
}

/**
 * Fetches and displays total donation data for the dashboard.
 */
async function fetchDonationData() {
    const container = document.getElementById('total-donations');
    if (!container) return;
    try {
        const response = await fetch('/api/donations');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();

        container.innerHTML = `
            <h3>Total Donated (USD)</h3>
            <p style="font-size: 2rem; font-weight: bold; color: #03045e;">$${data.total_donated.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</p>
        `;
        renderDonationsChart(data.recent_donations);
    } catch (error) {
        container.innerHTML = `<p style="color: red;">Failed to load donation data.</p>`;
        console.error('Error fetching donation data:', error);
    }
}

/**
 * Fetches and displays global climate data for the dashboard.
 */
async function fetchClimateData() {
    const container = document.getElementById('climate-metrics');
    if (!container) return;
    try {
        const response = await fetch('/api/climate');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        container.innerHTML = `
            <p><strong>Global Temperature Anomaly:</strong> +${data.global_temperature_anomaly}°C</p>
            <p><strong>Sea Level Rise (annual):</strong> ${data.sea_level_rise} mm</p>
            <p><strong>CO2 Concentration:</strong> ${data.co2_concentration} ppm</p>
        `;
    } catch (error) {
        container.innerHTML = `<p style="color: red;">Failed to load climate data.</p>`;
        console.error('Error fetching climate data:', error);
    }
}

/**
 * Fetches and displays updates from AgentMail for the dashboard.
 */
async function fetchAgentMailUpdates() {
    const container = document.getElementById('agentmail-feed');
    if (!container) return;
    try {
        const response = await fetch('/api/agentmail');
        if (!response.ok) throw new Error('Network response was not ok');
        const updates = await response.json();
        if (updates.length === 0) {
            container.innerHTML = `<p>No recent updates.</p>`;
            return;
        }

        let updatesHtml = '<ul>';
        updates.forEach(update => {
            updatesHtml += `<li style="margin-bottom: 1rem;"><strong>${update.subject}</strong><br>${update.body}</li>`;
        });
        updatesHtml += '</ul>';
        container.innerHTML = updatesHtml;
    } catch (error) {
        container.innerHTML = `<p style="color: red;">Failed to load updates.</p>`;
        console.error('Error fetching AgentMail updates:', error);
    }
}

/**
 * Renders a bar chart for recent donations, aggregating amounts by cause.
 * @param {Array} recentDonations - Array of donation objects from the API.
 */
function renderDonationsChart(recentDonations) {
    const ctx = document.getElementById('donationsChart')?.getContext('2d');
    if (!ctx) return;

    const causeTotals = recentDonations.reduce((acc, donation) => {
        const causeName = donation.cause.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        acc[causeName] = (acc[causeName] || 0) + donation.amount;
        return acc;
    }, {});

    const labels = Object.keys(causeTotals);
    const data = Object.values(causeTotals);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Recent Donations by Cause (USD)',
                data: data,
                backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(75, 192, 192, 0.6)', 'rgba(255, 159, 64, 0.6)'],
                borderColor: ['rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(255, 159, 64, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

/**
 * Handles the footer email signup form submission by sending data to the backend.
 */
async function handleEmailSignup(event) {
    event.preventDefault();
    const form = event.target;
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const agreed = document.getElementById('signup-agree').checked;

    if (!agreed) {
        alert("You must agree to receive emails.");
        return;
    }

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email })
        });
        const data = await response.json();
        if (data.status === 'success') {
            alert(`Thanks for signing up, ${name}! We'll be in touch at ${email}.`);
            form.reset();
        } else {
            alert('There was an error: ' + data.message);
        }
    } catch (error) {
        console.error('Signup error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Parallax scroll for hero section
window.addEventListener("scroll", function () {
  const parallax = document.querySelector('.parallax-bg');
  if (!parallax) return;
  let offset = window.scrollY * 0.4;
  parallax.style.transform = `translateY(${offset}px)`;
});