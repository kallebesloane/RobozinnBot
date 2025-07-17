import json
import os

# Arquivo onde salvaremos os dados temporários
ARQUIVO_SINAIS = "sinais_escanteios.json"

print("[DEBUG] regra_escanteios_green.py carregado")

def carregar_sinais_salvos():
    if os.path.exists(ARQUIVO_SINAIS):
        with open(ARQUIVO_SINAIS, "r") as f:
            return json.load(f)
    return {}

def salvar_sinais(sinais):
    with open(ARQUIVO_SINAIS, "w") as f:
        json.dump(sinais, f)

def verificar_sinais(jogos):
    sinais_salvos = carregar_sinais_salvos()
    mensagens = []

    for jogo in jogos:
        fixture_id = str(jogo['fixture']['id'])
        minuto = jogo['fixture']['status']['elapsed']
        gols_casa = jogo['goals']['home']
        gols_fora = jogo['goals']['away']
        escanteios_total = jogo.get("statistics", [{}])[0].get("statistics", [])
        liga = jogo['league']['name']
        casa = jogo['teams']['home']['name']
        fora = jogo['teams']['away']['name']

        # Pega número de escanteios (método alternativo caso a estrutura varie)
        total_escanteios = 0
        for estat in escanteios_total:
            if estat.get("type") == "Total Corners":
                total_escanteios = estat.get("value", 0)

        # Caso o jogo esteja entre 80 e 89 min e time da casa perdendo por 1 gol
        if minuto is not None and 80 <= minuto <= 89 and (gols_fora - gols_casa == 1):
            if fixture_id not in sinais_salvos:
                sinais_salvos[fixture_id] = {
                    "escanteios_iniciais": total_escanteios,
                    "minuto_envio": minuto,
                    "status": "aguardando",
                    "casa": casa,
                    "fora": fora,
                    "liga": liga,
                    "placar": f"{gols_casa} x {gols_fora}"
                }

                mensagens.append(
                    f"🟡 ESCANTEIOS POSSÍVEL GREEN\n🏟️ Liga: {liga}\n⏱ {minuto}min — {casa} perdendo pra {fora}\n🔢 Placar: {gols_casa} x {gols_fora}\n📊 Escanteios atuais: {total_escanteios}\n🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
                )

        # Se o jogo finalizou, verificar se foi Green
        if jogo['fixture']['status']['short'] == "FT" and fixture_id in sinais_salvos:
            esc_inicial = sinais_salvos[fixture_id]["escanteios_iniciais"]
            status = sinais_salvos[fixture_id]["status"]
            if status == "aguardando":
                resultado = "🟢 GREEN" if total_escanteios >= esc_inicial + 2 else "🔴 RED"
                mensagens.append(
                    f"{resultado} — FIM DE JOGO\n🏟️ Liga: {liga}\n{casa} x {fora}\nPlacar final: {gols_casa} x {gols_fora}\nEscanteios iniciais: {esc_inicial}\nEscanteios finais: {total_escanteios}"
                )
                sinais_salvos[fixture_id]["status"] = resultado

    salvar_sinais(sinais_salvos)
    return mensagens
