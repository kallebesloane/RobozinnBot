from flask import Flask
import threading
import requests
import os
import time
from telegram import Bot

from regra_escanteios import verificar_escanteios
from regra_expulsos import verificar_expulsos

app = Flask(__name__)

# Variáveis de ambiente
API_KEY = os.getenv("API_FOOTBALL_KEY")  # agora é a chave da SportMonks
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

bot = Bot(token=TELEGRAM_TOKEN)

def verificar_jogos():
    url = f"https://api.sportmonks.com/v3/football/fixtures?include=goals,teams,league,stats&filters=live"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        jogos = data.get("data", [])

        mensagens = []
        mensagens += verificar_escanteios(jogos)
        mensagens += verificar_expulsos(jogos)

        if mensagens:
            texto = "📊 ALERTAS AO VIVO:\n\n" + "\n\n".join(mensagens)
            for cid in CHAT_IDS:
                bot.send_message(chat_id=cid, text=texto, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        for cid in CHAT_IDS:
            bot.send_message(chat_id=cid, text=f"❌ Erro: {e}")

def iniciar_loop():
    while True:
        verificar_jogos()
        time.sleep(900)  # 15 minutos

threading.Thread(target=iniciar_loop).start()

@app.route('/')
def index():
    return "✅ Bot rodando com SportMonks (escanteios + expulsos)"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
