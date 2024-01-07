
function getCurrentTime() {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();

    // Format hours and minutes to always be two digits
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    return hours + ':' + minutes;
}


function doctorMSG(doctorAnswer) {
    return `
    <div class="chat chat-start">
    <div class="chat-image avatar">
      <div class="w-10 rounded-full">
        <img alt="Llama doctor chad"
            class="w-10 h-10"
            src="static/img/llama-doc-icon.png" />
      </div>
    </div>
    <div class="chat-header">
      Dr. Chad (llama-7b-hf-ft)
      <time class="text-xs opacity-50">${getCurrentTime()}</time>
    </div>
    <div class="chat-bubble message">${doctorAnswer}</div>
    <div class="chat-footer opacity-50">
      Answers are auto-generated.
    </div>
  </div>`;
}

function replaceDocMSG(resp) {
    let latest = document.querySelector('.doc-chat .chat-start:last-child .message');
    latest.innerHTML = resp;
}

function userMSG(userQuestion) {
    return `
    <div class="chat chat-end">
    <div class="chat-image avatar">
      <div class="w-10 rounded-full">
        <span class="material-symbols-outlined text-4xl">
            person
        </span>
      </div>
    </div>
    <div class="chat-header">
      You
      <time class="text-xs opacity-50">${getCurrentTime()}</time>
    </div>
    <div class="chat-bubble user-message message">${userQuestion}</div>
    <!--
    <div class="chat-footer opacity-50">
      Answers are auto-generated.
    </div>
    -->
  </div>`;
}

function appendMSG(html) {
    // append new chat msg to chat (.doc-chat)
    document.querySelector(".doc-chat").innerHTML += html;
}


async function askDoc() {

    const userQuestionTextArea = document.querySelector("#newMSG")
    const userQuestion = userQuestionTextArea.value;
    appendMSG(userMSG(userQuestion));

    // clear input
    userQuestionTextArea.value = "";

    // get the chat history (all messages except the last one)
    // the last one is (see above) the new user message
    let chatHistoryDivs = Array.from(
        document.querySelectorAll('.chat:not(:last-child)')
    );

    let chatHistory = [];
    chatHistoryDivs.forEach((el, i) => {
        chatHistory.push(
            i % 2 == 0 ? "Dr. Chad: " + el.querySelector(".chat-bubble").textContent : "Patient: " + el.querySelector(".chat-bubble").textContent
        );
    });

    // chatId --> generated in the backend (app.py)
    const chatId = document.querySelector('.doc-chat').id;

    // send question to the local backend server
    // -> handles calling of HF inference endpoint
    // + RAG-System / storing of messages, ...

    const data = {
        "question": userQuestion,
        "history": chatHistory,
        "chat_id": chatId
    }

    appendMSG(doctorMSG('<span class="loading loading-dots loading-sm"></span>'));

    console.log(data);

    const csrf_token = document.getElementsByName("csrf_token")[0].value;
    const url = "/api/ask";
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(response => {
            console.log(response);
            replaceDocMSG(response.answer);
        });

    // replaceDocMSG(response.json().answer);
}


function autoScaleTextArea(el) {
    // thanks to https://forum.mendix.com/link/space/ui-&-front-end/questions/122884
    setTimeout(function () {
        el.style.cssText = 'min-height:37px; height: 37px;';
        //   for box-sizing other than "content-box" use:
        //   el.style.cssText = '-moz-box-sizing:content-box';
        el.style.cssText = 'height:' + el.scrollHeight + 'px';
    }, 0);
}

document.addEventListener("DOMContentLoaded", function () {

    console.log("ready");

    // greet the user
    appendMSG(
        doctorMSG("Hello, this is Dr. Chad! How may I help you today?")
    )

    const newMSGtextarea = document.querySelector("#newMSG");
    newMSGtextarea.addEventListener('keydown', function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            askDoc();
        }
    });

    const sendBTN = document.querySelector("#sendMSG");
    sendBTN.addEventListener("click", function () {

        askDoc();

    });

});