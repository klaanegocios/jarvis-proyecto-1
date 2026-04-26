from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


@app.post("/")
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        try:
            respuesta = consultar_ia(user_text)
        except Exception as e:
            print("Error IA:", e)
            respuesta = "Error con la IA, pero el sistema funciona"

        enviar_mensaje(chat_id, respuesta)

    return {"ok": True}


def consultar_ia(texto):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Sos un asistente tipo JARVIS, directo y claro."},
            {"role": "user", "content": texto}
        ]
    }

    r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:
        print("Error API:", r.text)
        return "La IA no respondió correctamente"

    data = r.json()
    return data["choices"][0]["message"]["content"]


def enviar_mensaje(chat_id, texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": chat_id,
        "text": texto
    })
