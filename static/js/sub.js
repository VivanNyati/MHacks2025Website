// window.addEventListener("scroll", function () {
//   const img = document.querySelector('.donate_nav');
//   let offset = window.scrollY * 0.4;
//   img.style.transform = `translateY(${offset}px)`;
// });

document.getElementById('donate_sierra_club').addEventListener('click', async () => {
    try {
        if (!window.solana || !window.solana.isPhantom) {
            alert("Please install the Phantom wallet extension!");
            return;
        }

        // Fixed recipient public address (replace with your destination address)
        const DESTINATION_ADDRESS = "AiKoVs9zCcWhmfEMtqvqZT2Lhi1Z6rKESjm5UznK3kaF";

        // Get amount
        // Amount to send (in SOL)
        const AMOUNT = document.getElementById("sierra_club").value;

        // Connect to wallet
        const resp = await window.solana.connect();
        const provider = window.solana;

        // Prepare connection & transaction
        const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
        
        const fromPubkey = new solanaWeb3.PublicKey(resp.publicKey.toString());
        const toPubkey = new solanaWeb3.PublicKey(DESTINATION_ADDRESS);
        const lamports = AMOUNT * solanaWeb3.LAMPORTS_PER_SOL;
        
        // Create transfer transaction
        const transaction = new solanaWeb3.Transaction().add(
            solanaWeb3.SystemProgram.transfer({
                fromPubkey,
                toPubkey,
                lamports,
            })
        );

        // Request user signature and send transaction
        const { signature } = await provider.signAndSendTransaction(transaction);
        alert("Transaction sent! Signature: " + signature);

        // Optionally, wait for confirmation
        await connection.confirmTransaction(signature, 'confirmed');
        alert("Transaction confirmed!");

    } catch (err) {
        alert("Error: " + err.message);
    }
});

document.getElementById('donate_appalachian_voices').addEventListener('click', async () => {
    try {
        if (!window.solana || !window.solana.isPhantom) {
            alert("Please install the Phantom wallet extension!");
            return;
        }

        // Fixed recipient public address (replace with your destination address)
        const DESTINATION_ADDRESS = "AiKoVs9zCcWhmfEMtqvqZT2Lhi1Z6rKESjm5UznK3kaF";

        // Get amount
        // Amount to send (in SOL)
        const AMOUNT = document.getElementById("appalachian_voices").value;

        // Connect to wallet
        const resp = await window.solana.connect();
        const provider = window.solana;

        // Prepare connection & transaction
        const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
        
        const fromPubkey = new solanaWeb3.PublicKey(resp.publicKey.toString());
        const toPubkey = new solanaWeb3.PublicKey(DESTINATION_ADDRESS);
        const lamports = AMOUNT * solanaWeb3.LAMPORTS_PER_SOL;
        
        // Create transfer transaction
        const transaction = new solanaWeb3.Transaction().add(
            solanaWeb3.SystemProgram.transfer({
                fromPubkey,
                toPubkey,
                lamports,
            })
        );

        // Request user signature and send transaction
        const { signature } = await provider.signAndSendTransaction(transaction);
        alert("Transaction sent! Signature: " + signature);

        // Optionally, wait for confirmation
        await connection.confirmTransaction(signature, 'confirmed');
        alert("Transaction confirmed!");

    } catch (err) {
        alert("Error: " + err.message);
    }
});

document.getElementById('donate_earth_justice').addEventListener('click', async () => {
    try {
        if (!window.solana || !window.solana.isPhantom) {
            alert("Please install the Phantom wallet extension!");
            return;
        }

        // Fixed recipient public address (replace with your destination address)
        const DESTINATION_ADDRESS = "AiKoVs9zCcWhmfEMtqvqZT2Lhi1Z6rKESjm5UznK3kaF";

        // Get amount
        // Amount to send (in SOL)
        const AMOUNT = document.getElementById("earth_justice").value;

        // Connect to wallet
        const resp = await window.solana.connect();
        const provider = window.solana;

        // Prepare connection & transaction
        const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
        
        const fromPubkey = new solanaWeb3.PublicKey(resp.publicKey.toString());
        const toPubkey = new solanaWeb3.PublicKey(DESTINATION_ADDRESS);
        const lamports = AMOUNT * solanaWeb3.LAMPORTS_PER_SOL;
        
        // Create transfer transaction
        const transaction = new solanaWeb3.Transaction().add(
            solanaWeb3.SystemProgram.transfer({
                fromPubkey,
                toPubkey,
                lamports,
            })
        );

        // Request user signature and send transaction
        const { signature } = await provider.signAndSendTransaction(transaction);
        alert("Transaction sent! Signature: " + signature);

        // Optionally, wait for confirmation
        await connection.confirmTransaction(signature, 'confirmed');
        alert("Transaction confirmed!");

    } catch (err) {
        alert("Error: " + err.message);
    }
});

document.getElementById('donate_arcadia_center').addEventListener('click', async () => {
    try {
        if (!window.solana || !window.solana.isPhantom) {
            alert("Please install the Phantom wallet extension!");
            return;
        }

        // Fixed recipient public address (replace with your destination address)
        const DESTINATION_ADDRESS = "AiKoVs9zCcWhmfEMtqvqZT2Lhi1Z6rKESjm5UznK3kaF";

        // Get amount
        // Amount to send (in SOL)
        const AMOUNT = document.getElementById("arcadia_center").value;

        // Connect to wallet
        const resp = await window.solana.connect();
        const provider = window.solana;

        // Prepare connection & transaction
        const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
        
        const fromPubkey = new solanaWeb3.PublicKey(resp.publicKey.toString());
        const toPubkey = new solanaWeb3.PublicKey(DESTINATION_ADDRESS);
        const lamports = AMOUNT * solanaWeb3.LAMPORTS_PER_SOL;
        
        // Create transfer transaction
        const transaction = new solanaWeb3.Transaction().add(
            solanaWeb3.SystemProgram.transfer({
                fromPubkey,
                toPubkey,
                lamports,
            })
        );

        // Request user signature and send transaction
        const { signature } = await provider.signAndSendTransaction(transaction);
        alert("Transaction sent! Signature: " + signature);

        // Optionally, wait for confirmation
        await connection.confirmTransaction(signature, 'confirmed');
        alert("Transaction confirmed!");

    } catch (err) {
        alert("Error: " + err.message);
    }
});