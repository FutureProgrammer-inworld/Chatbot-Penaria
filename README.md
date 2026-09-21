# Penaria — Creative Writing Companion

Penaria adalah chatbot berbasis Large Language Model (LLM) yang dirancang sebagai
teman dan pendamping dalam proses creative writing.

Penaria membantu pengguna dalam mengembangkan ide cerita, karakter, plot,
dialog, serta memberikan feedback terhadap tulisan. Penaria tidak menulis
seluruh cerita untuk pengguna, tetapi membantu pengguna menemukan dan
mengembangkan ide mereka sendiri.


---

## 1. Tema dan Konsep Chatbot

### Tema Chatbot : Asisten Penulis Pemula

### Nama Chatbot

**Penaria — Creative Writing Companion**

### Konsep

Penaria merupakan chatbot dengan karakter fiksi bernama Penaria, seorang
"Master of Stories" dari dunia fiksi bernama **Inkbound World**.

Dalam aplikasi ini, Penaria berperan sebagai creative writing companion.
Pengguna dapat berdiskusi dengan Penaria mengenai berbagai aspek penulisan,
seperti:

- brainstorming ide cerita
- pengembangan karakter
- pengembangan plot
- pembuatan dan pengembangan konflik
- pengembangan dialog
- mencari ide ketika mengalami writer's block
- memberikan feedback terhadap draft
- mendiskusikan genre cerita
- mendapatkan referensi mengenai publikasi karya

Penaria memiliki kepribadian yang ramah, sabar, kritis, dan
solution-oriented. Bahasa utama yang digunakan adalah Bahasa Indonesia.

### Fitur Utama

Aplikasi Penaria terdiri dari beberapa bagian utama:

#### 1. Chat with Penaria

Halaman utama untuk berdiskusi langsung dengan Penaria.

Pengguna dapat mengirim pertanyaan atau ide dan Penaria akan merespons
berdasarkan system prompt serta conversation history.

#### 2. Arena Tulis

Arena Tulis merupakan ruang untuk menulis dan menyimpan draft cerita.

Fitur yang tersedia:

- judul draft
- text editor
- penghitung jumlah kata
- penghitung jumlah karakter
- penyimpanan draft menggunakan browser localStorage

Arena Tulis berfokus pada proses menulis, sedangkan diskusi dan brainstorming
dengan AI dilakukan melalui halaman Chat with Penaria.

#### 3. Genre Guide

Halaman referensi genre yang memberikan penjelasan singkat mengenai beberapa
genre cerita:

- Fantasy
- Mystery
- Science Fiction
- Romance
- Horror
- Adventure
- Slice of Life
- School
- Comedy

Setiap genre memiliki penjelasan dan tips singkat yang dapat digunakan
sebagai referensi saat mengembangkan cerita.

#### 4. Publishing Guide

Halaman referensi mengenai beberapa pilihan platform untuk membagikan karya
digital.

Platform yang dibahas dalam aplikasi antara lain:

- Trakteer
- KaryaKarsa

Halaman ini juga menyediakan checklist sebelum karya dipublikasikan.

---

# 2. Teknologi yang Digunakan

Project ini menggunakan:

- **Python**
- **Flask** — web framework untuk backend
- **Groq API** — API untuk mengakses Large Language Model
- **OpenAI GPT-OSS 120B** melalui Groq
- **HTML** — struktur halaman web
- **CSS** — tampilan dan layout
- **JavaScript** — interaksi frontend
- **JSON** — penyimpanan conversation history
- **localStorage** — penyimpanan draft pada Arena Tulis
- **python-dotenv** — membaca API key dari file `.env`

---

# 3. Struktur Project

Struktur utama project Penaria adalah sebagai berikut:

```text
Chatbot-Penaria/
│
├── app.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
├── prompts/
│   └── system_prompt.py
│
├── templates/
│   ├── index.html
│   ├── writing_arena.html
│   ├── genre_guide.html
│   └── publishing_guide.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   └── writing_arena.js
│   │
│   └── images/
│       └── penaria.png
|       └── penaria_waiting.png
│
└── data/
    └── conversation/
        └── conversation.json
```
### Bagian yang Dibantu AI Assistant
1. Brainstroming konsep chatbot Penaria
