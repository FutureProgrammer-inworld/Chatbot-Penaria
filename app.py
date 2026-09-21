import os

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq

import json
from pathlib import Path

from prompts.system_prompt import SYSTEM_PROMPT

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil API Key
api_key = os.getenv("GROQ_API_KEY")

# Membuat Flask app
app = Flask(__name__)

# Memastikan API Key tersedia 
if not api_key:
    raise ValueError("GROQ_API_KEY tidak ditemukan. Pastikan sudah diatur di file .env.")

# Membuat Groq Client
client = Groq(api_key=api_key)

# =========================================================
# CONVERSATION STORAGE
# =========================================================

# Lokasi folder project
BASE_DIR = Path(__file__).resolve().parent

# Folder untuk menyimpan riwayat percakapan
CONVERSATION_DIR = BASE_DIR / "data" / "conversation"

# File JSON tempat history disimpan
CONVERSATION_FILE = CONVERSATION_DIR / "conversation.json"


def load_conversation():
    """
    Memuat riwayat percakapan dari file JSON.

    System prompt selalu dibuat dari SYSTEM_PROMPT
    dan tidak disimpan di conversation.json.
    """

    # System prompt selalu menjadi pesan pertama
    history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Jika file belum ada, gunakan history baru
    if not CONVERSATION_FILE.exists():
        print("Belum ada conversation.json. Memulai percakapan baru.")
        return history

    try:
        with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
            saved_messages = json.load(file)

        # Pastikan isi JSON berupa list
        if not isinstance(saved_messages, list):
            print("Format conversation.json tidak valid.")
            return history

        # Masukkan hanya pesan user dan assistant
        for message in saved_messages:

            if not isinstance(message, dict):
                continue

            role = message.get("role")
            content = message.get("content")

            if role not in ["user", "assistant"]:
                continue

            if not isinstance(content, str):
                continue

            history.append(
                {
                    "role": role,
                    "content": content
                }
            )

        print(
            f"Conversation history berhasil dimuat: "
            f"{len(history) - 1} pesan."
        )

    except json.JSONDecodeError:
        print(
            "conversation.json rusak atau bukan JSON yang valid. "
            "Memulai percakapan baru."
        )

    except OSError as error:
        print(
            f"Gagal membaca conversation.json: {error}. "
            "Memulai percakapan baru."
        )

    return history


def save_conversation(history):
    """
    Menyimpan conversation history ke file JSON.

    System prompt tidak ikut disimpan.
    Hanya pesan user dan assistant yang disimpan.
    """

    try:
        # Pastikan folder data/conversation tersedia
        CONVERSATION_DIR.mkdir(parents=True, exist_ok=True)

        # Ambil hanya pesan user dan assistant
        messages_to_save = []

        for message in history:

            if message.get("role") in ["user", "assistant"]:
                messages_to_save.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                )

        # Simpan ke file sementara terlebih dahulu
        # agar file utama tidak mudah rusak jika proses terganggu
        temp_file = CONVERSATION_FILE.with_suffix(".tmp")

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(
                messages_to_save,
                file,
                ensure_ascii=False,
                indent=2
            )

        # Setelah berhasil, ganti file lama
        temp_file.replace(CONVERSATION_FILE)

        print(
            f"Conversation history berhasil disimpan: "
            f"{len(messages_to_save)} pesan."
        )

    except OSError as error:
        print(f"Gagal menyimpan conversation history: {error}")


# =========================================================
# LOAD CONVERSATION HISTORY SAAT APLIKASI START
# =========================================================

conversation_history = load_conversation()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/arena_tulis")
def writing_arena():
    return render_template("writing_arena.html")


@app.route("/genre_guide")
def genre_guide():
    return render_template("genre_guide.html")


@app.route("/publishing_guide")
def publishing_guide():
    return render_template("publishing_guide.html")

# =========================================================
# TEST AI
# =========================================================

@app.route("/test-ai")
def test_ai():

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": "Halo Penaria, perkenalkan dirimu."
                }
            ]
        )

        return jsonify(
            {
                "success": True,
                "message": response.choices[0].message.content
            }
        )

    except Exception as error:

        print(f"Error test AI: {error}")

        return jsonify(
            {
                "success": False,
                "error": str(error)
            }
        ), 500

# =========================================================
# TEST CONVERSATION HISTORY
# =========================================================

@app.route("/test-history")
def test_history():

    try:

        # Buat percakapan test khusus
        test_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": "Nama karakterku adalah Aisha."
            }
        ]

        first_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=test_messages
        )

        first_answer = first_response.choices[0].message.content

        test_messages.append(
            {
                "role": "assistant",
                "content": first_answer
            }
        )

        test_messages.append(
            {
                "role": "user",
                "content": "Siapa nama karakterku?"
            }
        )

        second_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=test_messages
        )

        second_answer = second_response.choices[0].message.content

        return jsonify(
            {
                "success": True,
                "first_response": first_answer,
                "second_response": second_answer
            }
        )

    except Exception as error:

        print(f"Error test history: {error}")

        return jsonify(
            {
                "success": False,
                "error": str(error)
            }
        ), 500


# Chat Endpoint untuk menerima input dari pengguna
@app.route("/chat", methods=["POST"])
def chat():

    global conversation_history

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request tidak berisi data JSON."
            }), 400

        user_message = data.get("message")

        if not isinstance(user_message, str):
            return jsonify({
                "success": False,
                "error": "Pesan harus berupa teks."
            }), 400

        user_message = user_message.strip()

        if not user_message:
            return jsonify({
                "success": False,
                "error": "Pesan tidak boleh kosong."
            }), 400

        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=conversation_history
        )

        assistant_message = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # -------------------------------------------------
        # Simpan history ke JSON
        # -------------------------------------------------

        save_conversation(conversation_history)

        return jsonify({
            "success": True,
            "message": assistant_message
        }), 200

    except Exception as e:

        print(f"Error saat menghubungi Groq: {e}")

        return jsonify({
            "success": False,
            "error": (
                "Maaf, Penaria sedang mengalami masalah "
                "saat memproses pesanmu. Silakan coba lagi."
            )
        }), 500

# =========================================================
# CLEAR CONVERSATION
# =========================================================

@app.route("/clear-conversation", methods=["POST"])
def clear_conversation():

    global conversation_history

    try:

        # Reset history
        conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Simpan ulang JSON tanpa pesan
        save_conversation(conversation_history)

        return jsonify(
            {
                "success": True,
                "message": "Conversation history berhasil dihapus."
            }
        ), 200

    except Exception as error:

        print(f"Error saat menghapus conversation: {error}")

        return jsonify(
            {
                "success": False,
                "error": "Gagal menghapus conversation history."
            }
        ), 500

if __name__ == "__main__":
    app.run(debug=True)