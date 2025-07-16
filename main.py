import requests
import asyncio
import os
from telegram import Bot

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS").split(",")

bot = Bot(token=TELEGRAM_TOKEN)

async def enviar_alerta():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        jogos = data["response"]
        lista_jogos = []

        for jogo in jogos:
            minuto = jogo['fixture']['status']['elapsed']
            gols_casa = jogo['goals']['home']
            gols_fora = jogo['goals']['away']

            if minuto >= 25 and (gols_fora - gols_casa == 1):
                casa = jogo['teams']['home']['name']
                fora = jogo['teams']['away']['name']
                placar = f"{gols_casa} x {gols_fora}"
                lista_jogos.append(
                    f"⏱ {minuto}min — {casa} (casa) perdendo pra {fora}\n🔢 Placar: {placar}\n🔗 [Aposte na Bet365](https://www.bet365.com/#/IP/B1)"
                )

        if lista_jogos:
            mensagem = "🚨 Jogos com o time da casa perdendo por 1 gol após 25 minutos:\n\n" + "\n\n".join(lista_jogos)
        else:
            mensagem = "⚠️ Nenhum jogo com o time da casa perdendo por 1 gol após 25 minutos no momento."

        for chat_id in CHAT_IDS:
            await bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")

    except Exception as e:
        for chat_id in CHAT_IDS:
            await bot.send_message(chat_id=chat_id, text=f"❌ Erro: {e}")

# Executa
asyncio.run(enviar_alerta())
