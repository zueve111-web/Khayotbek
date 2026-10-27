# Khayotbek AI
Футуристический веб-интерфейс AI-помощника на Flask.

## Render
Build command: `pip install -r requirements.txt`
Start command: `gunicorn app:app`

Без `OPENAI_API_KEY` доступен демонстрационный режим. Для настоящих ответов добавьте `OPENAI_API_KEY` в Environment на Render. Не публикуйте ключ в GitHub.
Можно задать `OPENAI_MODEL`; по умолчанию `gpt-4.1-mini`.
