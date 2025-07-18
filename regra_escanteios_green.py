import json
import os

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

def extrair_escanteios(jogo):
    total_escanteios = 0
    statistics = jogo.get("statistics", [])
    for time_stats in statistics:
        for stat in time_stats.get("statistics", []):
            if stat.get("type") == "Total Corners":
                total_escanteios += stat.get("value") or 0
    return total_escanteios

def verificar_sinais(jogos):
    sinais_salvos = carregar_sinais_salvos()
    mensagens = []

    for jogo in jogos:
        fixture_id = str(jogo['fixture']['id'])
        minuto = jogo['fixture']['status']['elapsed']
        status = jogo['fixture']['status']['short']
        gols_casa = jogo['goals']['home']
        gols_fora = jogo['goals']['away']
        liga = jogo['league']['name']
        casa = jogo['teams']['home']['name']
        fora = jogo['teams']['away']['name']
        total_escanteios = extrair_escanteios(jogo)

        # ⚠️ Envia o sinal entre 80 e 89 min se time da casa estiver perdendo por 1 gol
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

        # ✅ Jogo finalizado → Verifica se deu green ou red
        if status == "FT" and fixture_id in sinais_salvos:
            sinal = sinais_salvos[fixture_id]
            if sinal["status"] == "aguardando":
                esc_inicial = sinal["escanteios_iniciais"]
                resultado = "🟢 GREEN" if total_escanteios >= esc_inicial + 2 else "🔴 RED"
                mensagens.append(
                    f"{resultado} — FIM DE JOGO\n🏟️ Liga: {liga}\n{casa} x {fora}\n🔢 Placar final: {gols_casa} x {gols_fora}\n📊 Escanteios iniciais: {esc_inicial}\n📊 Escanteios finais: {total_escanteios}"
                )
                sinais_salvos[fixture_id]["status"] = resultado

    salvar_sinais(sinais_salvos)
    return mensagens
