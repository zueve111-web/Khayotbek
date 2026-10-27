
import os
import random
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

def simple_reply(message):
    text = message.lower().strip()

    if any(x in text for x in ["привет", "здравствуй", "салам"]):
        return "Привет! Я Khayotbek AI 😊 Чем могу помочь?"
    if "как тебя зовут" in text:
        return "Я Khayotbek AI — твой виртуальный помощник!"
    if any(x in text for x in ["как дела", "как ты"]):
        return "У меня всё хорошо! 😊 А у тебя как дела?"
    if any(x in text for x in ["спасибо", "благодарю"]):
        return "Пожалуйста! Всегда рад помочь 😊"
    if any(x in text for x in ["пока", "до свидания"]):
        return "До встречи! Заходи ещё 😊"
    if "помощь" in text:
        return "Я могу поболтать с тобой и ответить на простые вопросы. Напиши, что тебя интересует."
    return random.choice([
        "Я тебя слушаю! Расскажи немного подробнее 😊",
        "Интересный вопрос! Можешь уточнить, что именно ты хочешь узнать?",
        "Я Khayotbek AI. Давай попробуем разобраться вместе!",
        "Пока мой ИИ может быть временно недоступен. Попробуй спросить немного иначе."
    ])

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

    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
                contents=message
            )
            if response.text:
                return jsonify({"reply": response.text})
        except Exception:
            app.logger.exception("Gemini API request failed")

    return jsonify({"reply": simple_reply(message)})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )
