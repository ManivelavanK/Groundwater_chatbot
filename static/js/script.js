document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const loadingIndicator = document.getElementById('loading-indicator');

    chatForm.addEventListener('submit', async(e) => {
        e.preventDefault();
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        // Display user message
        appendMessage(messageText, 'user-message');
        userInput.value = '';

        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            // Display bot response
            appendMessage(data.response, 'bot-message');

        } catch (error) {
            console.error('Error:', error);
            appendMessage(`Sorry, something went wrong: ${error.message}`, 'bot-message');
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });

    function appendMessage(text, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        messageElement.innerText = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    }
});