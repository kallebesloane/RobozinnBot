from flask import Flask
import threading
import requests
import os
import time
from telegram import Bot

# Importa os arquivos de regras
from regra_escanteios import verificar_escanteios
from regra_expulsos import verificar_expulsos

app = Flask(__name__)

# Carregar variáveis do ambiente (somente Telegram aqui)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

# Chave da RapidAPI (direto no código por enquanto)
RAPIDAPI_KEY = "8ecad7e0damsha69225ed9c94c69p1650cfjsn425f2e9e7de8"  # <<--- Substitua pela sua chave verdadeira

bot = Bot(token=TELEGRAM_TOKEN)

def verificar_jogos():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        jogos = res.json().get("response", [])

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
    return "✅ Bot rodando com múltiplas regras (escanteios + expulsos)"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
