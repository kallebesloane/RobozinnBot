import os
import requests

API_KEY = os.getenv("SPORTMONKS_API_KEY")
URL_LIVESCORES = "https://api.sportmonks.com/v3/football/livescores/inplay"
HEADERS = {
    "accept": "application/json"
}

print("[DEBUG] regra_expulsos.py carregado")

def verificar_expulsos():
    try:
        response = requests.get(
            URL_LIVESCORES + "?include=participants;events;league",
            headers=HEADERS,
            params={"api_token": API_KEY}
        )
        data = response.json()

        mensagens = []

        for jogo in data.get("data", []):
            if not jogo.get("events"):
                continue

            minuto = jogo.get("time", {}).get("minute", 0)
            if minuto < 45:
                continue

            expulsos = [e for e in jogo["events"] if e["type"] == "redcard"]

            if expulsos:
                liga = jogo["league"]["name"]
                casa = jogo["participants"][0]["name"]
                fora = jogo["participants"][1]["name"]
                placar_casa = jogo["scores"]["local_score"]
                placar_fora = jogo["scores"]["visitor_score"]

                mensagem = f"ð¨ EXPULSO
ðï¸ Liga: {liga}
â± {minuto}min â {casa} x {fora}
ð´ Jogador expulso!
ð¢ Placar: {placar_casa} x {placar_fora}"
                mensagens.append(mensagem)

        return mensagens

    except Exception as e:
        print(f"[ERRO regra_expulsos.py] {e}")
        return []
