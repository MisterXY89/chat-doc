
async function askDocApi(data) {
    const url = '/api/ask_doc';

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(data)
    });

    return response.json();
}


async function askDoc() {
    // get the latest user message from the chat
    const userMessage = document.querySelector('.chat .user-message:last-child');
    const userQuestion = userMessage.querySelector('.text').textContent;

    // get the chat history (all messages except the last one)
    // the last one is (see above) the new user message
    const chatHistory = document.querySelectorAll('.chat .message:not(:last-child)');

    // chatId --> generated in the backend (app.py)
    const chatId = document.querySelector('.chat').id;

    // send question to the local backend server
    // -> handles calling of HF inference endpoint
    // + RAG-System / storing of messages, ...

    const data = {
        "question": userQuestion,
        "history": chatHistory,
        "chat_id": chatId
    }

    const url = "/chat-doc"

}