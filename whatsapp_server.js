require('dotenv').config();
const express = require('express');
const axios = require('axios');
const { PythonShell } = require('python-shell');
const app = express();

// Initialize Python bot
const pyshell = new PythonShell('whatsapp_bot.py', {
    mode: 'text',
    pythonOptions: ['-u']
});

app.use(express.json());

// Webhook verification
app.get('/webhook', (req, res) => {
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode && token) {
        if (mode === 'subscribe' && token === process.env.VERIFY_TOKEN) {
            console.log('Webhook verified');
            res.status(200).send(challenge);
        } else {
            res.sendStatus(403);
        }
    }
});

// Handle incoming messages
app.post('/webhook', async (req, res) => {
    try {
        const changes = req.body?.entry?.[0]?.changes?.[0]?.value?.messages?.[0];
        if (changes && changes.text) {
            const phone_number_id = req.body.entry[0].changes[0].value.metadata.phone_number_id;
            const from = changes.from;
            const msg_body = changes.text.body;

            // Send message to Python bot
            pyshell.send(JSON.stringify({
                type: 'message',
                sender: from,
                content: msg_body
            }));
        }
        res.sendStatus(200);
    } catch (error) {
        console.error('Error processing webhook:', error);
        res.sendStatus(500);
    }
});

// Handle Python bot responses
pyshell.on('message', async (response) => {
    try {
        const data = JSON.parse(response);
        if (data.type === 'response') {
            await sendWhatsAppMessage(data.recipient, data.content);
        }
    } catch (error) {
        console.error('Error processing bot response:', error);
    }
});

// Function to send WhatsApp message
async function sendWhatsAppMessage(recipient, message) {
    try {
        await axios({
            method: 'POST',
            url: `https://graph.facebook.com/v17.0/${process.env.PHONE_NUMBER_ID}/messages`,
            headers: {
                'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`,
                'Content-Type': 'application/json'
            },
            data: {
                messaging_product: 'whatsapp',
                to: recipient,
                text: { body: message }
            }
        });
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
