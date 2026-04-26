@app.post("/")
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        try:
            respuesta = consultar_ia(user_text)
        except:
            respuesta = "Error con la IA, pero el sistema funciona"

        enviar_mensaje(chat_id, respuesta)

    return {"ok": True}
