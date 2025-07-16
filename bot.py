from flask import Flask
import threading
import requests
import os
import time
from telegram import Bot

app = Flask(__name__)

# Variáveis de ambiente
API_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

bot = Bot(token=TELEGRAM_TOKEN)

# Função principal que verifica os jogos
def verificar_jogos():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_KEY}

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        jogos = data["response"]
        lista = []

        for jogo in jogos:
            minuto = jogo['fixture']['status']['elapsed']
            gols_casa = jogo['goals']['home']
            gols_fora = jogo['goals']['away']

            if minuto >= 70 and (gols_fora - gols_casa == 1):
                casa = jogo['teams']['home']['name']
                fora = jogo['teams']['away']['name']
                placar = f"{gols_casa} x {gols_fora}"
                lista.append(
                    f"⏱ {minuto}min — {casa} perdendo pra {fora}\n🔢 Placar: {placar}\n🔗 [Aposte na Bet365](https://www.bet365.com/#/IP/B1)"
                )

        if lista:
            mensagem = "🚨 Jogos com o time da casa perdendo por 1 gol após 70 minutos:\n\n" + "\n\n".join(lista)
        else:
            mensagem = "⚠️ Nenhum jogo com o time da casa perdendo por 1 gol após 70 minutos no momento."

        for cid in CHAT_IDS:
            bot.send_message(chat_id=cid, text=mensagem, parse_mode="Markdown")

    except Exception as e:
        for cid in CHAT_IDS:
            bot.send_message(chat_id=cid, text=f"❌ Erro: {e}")

# Loop automático a cada 10 minutos
def iniciar_loop():
    while True:
        verificar_jogos()
        time.sleep(600)  # 10 minutos

# Iniciar o loop em uma thread separada
threading.Thread(target=iniciar_loop).start()

# Rota básica do Flask
@app.route('/')
def index():
    return "✅ Bot rodando com verificação automática!"

# Rodar o Flask no Render
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
