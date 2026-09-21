const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatArea = document.getElementById("chatArea");
const sendButton = document.getElementById("sendButton");

console.log("Penaria app.js berhasil dimuat.");


/* =========================================
   SUBMIT CHAT
========================================= */

chatForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    console.log("Form berhasil disubmit.");

    const message = messageInput.value.trim();

    console.log("Pesan:", message);

    if (!message) {
        return;
    }

    // Tampilkan pesan user
    addUserMessage(message);

    // Kosongkan input
    messageInput.value = "";

    // Disable tombol
    sendButton.disabled = true;
    sendButton.classList.add("loading");

    // Proses Berpikir Penaria
    const typingIndicator = addTypingIndicator();

    try {

        console.log("Mengirim request ke /chat...");

        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        console.log("Response status:", response.status);

        const data = await response.json();

        console.log("Response data:", data);

        if (!response.ok || !data.success) {
            throw new Error(
                data.error || "Terjadi kesalahan."
            );
        }

        // Penaria selesai berpikir, hapus indikator
        removeTypingIndicator(typingIndicator);

        // Tampilkan jawaban Penaria
        addPenariaMessage(data.message);

    } catch (error) {

        console.error("Error:", error);

        // Hapus indikator berpikir Penaria
        removeTypingIndicator(typingIndicator);

        addPenariaMessage(
            "Maaf, terjadi masalah saat menghubungi Penaria. ✨"
        );

    } finally {

        sendButton.disabled = false;
        sendButton.classList.remove("loading");

        messageInput.focus();

    }

});


/* =========================================
   USER MESSAGE
========================================= */

function addUserMessage(message) {

    const row = document.createElement("div");

    row.classList.add(
        "message-row",
        "user-message"
    );


    const content = document.createElement("div");

    content.classList.add("message-content");


    const name = document.createElement("div");

    name.classList.add("message-name");

    name.textContent = "You";


    const bubble = document.createElement("div");

    bubble.classList.add("chat-bubble");

    bubble.textContent = message;


    content.appendChild(name);

    content.appendChild(bubble);

    row.appendChild(content);

    chatArea.appendChild(row);


    scrollToBottom();

}


/* =========================================
   PENARIA MESSAGE
========================================= */

function addPenariaMessage(message) {

    const row = document.createElement("div");

    row.classList.add(
        "message-row",
        "penaria-message"
    );


    // Avatar Penaria
    const avatar = document.createElement("img");

    avatar.src = "/static/images/penaria.png";

    avatar.alt = "Penaria";

    avatar.classList.add("chat-avatar");


    // Content
    const content = document.createElement("div");

    content.classList.add("message-content");


    // Nama
    const name = document.createElement("div");

    name.classList.add("message-name");

    name.textContent = "Penaria";


    // Bubble
    const bubble = document.createElement("div");

    bubble.classList.add("chat-bubble");


    // Pisahkan berdasarkan baris
    const paragraphs = message.split("\n");


    paragraphs.forEach(function (paragraph) {

        if (paragraph.trim() !== "") {

            const p = document.createElement("p");

            p.textContent = paragraph;

            bubble.appendChild(p);

        }

    });


    content.appendChild(name);

    content.appendChild(bubble);

    row.appendChild(avatar);

    row.appendChild(content);

    chatArea.appendChild(row);


    scrollToBottom();

}


/* =========================================
   AUTO SCROLL
========================================= */

function scrollToBottom() {

    chatArea.scrollTop = chatArea.scrollHeight;

}


/* =========================================
   ENTER = SEND
========================================= */

messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        chatForm.requestSubmit();

    }

});

/* =========================================
   TYPING INDICATOR
========================================= */

function addTypingIndicator() {

    const row = document.createElement("div");

    row.classList.add(
        "message-row",
        "penaria-message",
        "typing-row"
    );


    const avatar = document.createElement("img");

    avatar.src = "/static/images/penaria.png";

    avatar.alt = "Penaria";

    avatar.classList.add("chat-avatar");


    const content = document.createElement("div");

    content.classList.add("message-content");


    const name = document.createElement("div");

    name.classList.add("message-name");

    name.textContent = "Penaria";


    const bubble = document.createElement("div");

    bubble.classList.add(
        "chat-bubble",
        "typing-bubble"
    );


    for (let i = 0; i < 3; i++) {

        const dot = document.createElement("span");

        dot.classList.add("typing-dot");

        bubble.appendChild(dot);

    }


    content.appendChild(name);

    content.appendChild(bubble);

    row.appendChild(avatar);

    row.appendChild(content);

    chatArea.appendChild(row);


    scrollToBottom();


    return row;
}


function removeTypingIndicator(element) {

    if (element && element.parentNode) {
        element.remove();
    }

}