document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.getElementById('chat-button');
    const chatModal = document.getElementById('chat-modal');
    const closeChat = document.getElementById('close-chat');
    const sendMessageButton = document.getElementById('send-message');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');

    chatButton.addEventListener('click', function(event) {
        event.preventDefault();
        chatModal.style.display = 'block';
    });

    closeChat.addEventListener('click', function() {
        chatModal.style.display = 'none';
    });

    sendMessageButton.addEventListener('click', async function() {
        const message = chatInput.value;
        if (message.trim() !== '') {
            chatMessages.innerHTML += `<div class="message user-message">${message}</div>`;
            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll ke bawah

            // Kirim pesan ke backend dan terima respons
            try {
                const response = await sendMessage(message);
                chatMessages.innerHTML += `<div class="message bot-message">${response}</div>`;
                chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll ke bawah
            } catch (error) {
                chatMessages.innerHTML += `<div class="message bot-message">Terjadi kesalahan: ${error.message}</div>`;
                chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll ke bawah
            }
        }
    });

    async function sendMessage(message) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/handle_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });
            const data = await response.json();
            if (data.products) {
                return data.products.map(product => `Nama: ${product.name}\nDeskripsi: ${product.description}\nHarga: ${product.price}`).join('\n\n');
            } else if (data.answer) {
                return data.answer;
            } else {
                return data.message;
            }
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
});
