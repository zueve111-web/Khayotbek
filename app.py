import os
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
@app.get("/")
def home():
    return render_template("index.html")
@app.post("/api/chat")
def chat():
    data=request.get_json(silent=True) or {}
    message=(data.get("message") or "").strip()
    if not message:
        return jsonify({"reply":"Напиши сообщение, и я постараюсь помочь."}),400
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response=client.responses.create(model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),instructions="Ты Khayotbek AI — дружелюбный помощник. Отвечай на языке пользователя, ясно и полезно.",input=message)
            return jsonify({"reply":response.output_text})
        except Exception:
            app.logger.exception("AI API request failed")
            return jsonify({"reply":"Не удалось связаться с ИИ. Проверь OPENAI_API_KEY и доступ к API в Render."}),502
    return jsonify({"reply":"Интерфейс Khayotbek AI работает! Чтобы включить настоящие ответы ИИ, добавь OPENAI_API_KEY в Environment на Render. Пока ты написал: «"+message[:500]+"»."})
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","10000")))
