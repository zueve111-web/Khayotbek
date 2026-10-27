
import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Напиши сообщение!"}), 400

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "reply": "Добавь GEMINI_API_KEY в настройках Render."
        }), 500

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=message
        )
        return jsonify({
            "reply": response.text or "Попробуй задать вопрос иначе."
        })
    except Exception:
        app.logger.exception("Gemini API request failed")
        return jsonify({
            "reply": "Не удалось получить ответ. Проверь настройки Gemini."
        }), 502

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )
