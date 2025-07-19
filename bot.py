from flask import Flask
import threading
import requests
import os
import time
from telegram import Bot

# Importa regra de escanteios adaptada para SportMonks
from regra_escanteios import verificar_sinais

app = Flask(__name__)

API_KEY = os.getenv("SPORTMONKS_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

bot = Bot(token=TELEGRAM_TOKEN)

def obter_jogos_ao_vivo():
    url = f"https://api.sportmonks.com/v3/football/livescores/inplay?include=participants;scores;league"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados.get("data", [])
    except Exception as e:
        print(f"[ERRO] Falha ao obter jogos ao vivo: {e}")
        return []

def verificar_jogos():
    jogos = obter_jogos_ao_vivo()
    mensagens = verificar_sinais(jogos)
    if mensagens:
        texto = "📊 ALERTAS AO VIVO:\n\n" + "\n\n".join(mensagens)
        for cid in CHAT_IDS:
            bot.send_message(chat_id=cid, text=texto, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        print("[INFO] Nenhum jogo com critério encontrado.")

def loop():
    while True:
        verificar_jogos()
        time.sleep(900)  # 15 minutos

threading.Thread(target=loop, daemon=True).start()

@app.route('/')
def index():
    return "✅ Bot rodando com SportMonks e alertas de escanteios."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
