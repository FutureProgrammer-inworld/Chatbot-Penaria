const draftTitle = document.getElementById("draftTitle");
const draftEditor = document.getElementById("draftEditor");

const wordCount = document.getElementById("wordCount");
const characterCount = document.getElementById("characterCount");

const saveDraftButton = document.getElementById("saveDraftButton");
const draftStatus = document.getElementById("draftStatus");


/* ========================================
   WORD & CHARACTER COUNTER
======================================== */

function updateCounts() {

    const text = draftEditor.value.trim();

    const characters = draftEditor.value.length;

    const words = text
        ? text.split(/\s+/).length
        : 0;

    wordCount.textContent = words;
    characterCount.textContent = characters;
}


/* ========================================
   SAVE DRAFT
======================================== */

function saveDraft() {

    const draft = {
        title: draftTitle.value,
        content: draftEditor.value
    };

    localStorage.setItem(
        "penariaDraft",
        JSON.stringify(draft)
    );

    draftStatus.innerHTML = `
        <span class="status-dot"></span>
        Draft tersimpan
    `;

    console.log("Draft berhasil disimpan.");
}


/* ========================================
   LOAD DRAFT
======================================== */

function loadDraft() {

    const savedDraft =
        localStorage.getItem("penariaDraft");

    if (!savedDraft) return;

    try {

        const draft = JSON.parse(savedDraft);

        draftTitle.value = draft.title || "";
        draftEditor.value = draft.content || "";

        updateCounts();

        draftStatus.innerHTML = `
            <span class="status-dot"></span>
            Draft tersimpan
        `;

    } catch (error) {

        console.error(
            "Gagal membaca draft:",
            error
        );

    }
}


/* ========================================
   EVENTS
======================================== */

draftEditor.addEventListener(
    "input",
    updateCounts
);

draftTitle.addEventListener(
    "input",
    function () {

        draftStatus.innerHTML = `
            <span class="status-dot"></span>
            Ada perubahan
        `;

    }
);

draftEditor.addEventListener(
    "input",
    function () {

        draftStatus.innerHTML = `
            <span class="status-dot"></span>
            Ada perubahan
        `;

    }
);

saveDraftButton.addEventListener(
    "click",
    saveDraft
);


/* ========================================
   INITIALIZE
======================================== */

loadDraft();
updateCounts();