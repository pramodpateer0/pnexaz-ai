from flask import Flask, request, jsonify, send_from_directory
import os
import json
import urllib.request
import urllib.error

app = Flask(__name__)

API_URL = "https://api.openai.com/v1/responses"


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/logo.png")
def logo():
    return send_from_directory(".", "logo.png")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please type a message."})

    text = message.lower()

    # Creator reply
    creator_words = [
        "kisne banaya",
        "kisne bnaya",
        "banaya kisne",
        "aapko kisne banaya",
        "tumhe kisne banaya",
        "who created you",
        "who made you",
        "who is your creator",
        "creator",
        "maker"
    ]

    if any(word in text for word in creator_words):
        return jsonify({
            "reply": "Mujhe Pramod Pateer ne banaya hai, aur woh mere Boss hain. 😎🤖"
        })

    # Development/status reply
    ready_words = [
        "kab tak taiyar",
        "kab tak tayyar",
        "kab ready",
        "kitne din me ready",
        "kitne din mein ready",
        "when will you be ready",
        "when will you be complete",
        "when are you ready"
    ]

    if any(word in text for word in ready_words):
        return jsonify({
            "reply": "Mujhe kuchh dino se lekar 2 mahine ke andar andar ekdam taiyar karne ka target hai. 🚀"
        })

    # Basic offline replies
    if text in ["hello", "hi", "hii", "hey", "namaste", "नमस्ते"]:
        return jsonify({
            "reply": "Hello! 👋 Main PnexaZ AI hoon. Aap mujhse kuchh bhi pooch sakte hain."
        })

    if "tumhara naam" in text or "aapka naam" in text or "your name" in text:
        return jsonify({
            "reply": "Mera naam PnexaZ AI hai. 🤖"
        })

    if "kya kar sakte" in text or "what can you do" in text:
        return jsonify({
            "reply": "Main questions ka jawab dene, ideas dene aur information samjhane mein madad kar sakta hoon."
        })

    # OpenAI API
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return jsonify({
            "reply": "Abhi meri AI service ki API key available nahi hai. Lekin mere basic features kaam kar rahe hain. 🤖"
        })

    payload = {
        "model": "gpt-5-mini",
        "input": message
    }

    try:
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + api_key
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        reply = result.get("output_text")

        if not reply:
            reply = "AI se response nahi mila."

        return jsonify({"reply": reply})

    except urllib.error.HTTPError as e:
        error_text = e.read().decode(
            "utf-8",
            errors="ignore"
        )

        print("API ERROR:", error_text)

        return jsonify({
            "reply": "Abhi AI service ke credits available nahi hain."
        }), 500

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "reply": "AI connection mein problem aa rahi hai."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000
    )
