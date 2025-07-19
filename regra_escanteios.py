print("[DEBUG] regra_escanteios.py carregado")

def verificar_escanteios(jogos):
    resultados = []

    for jogo in jogos:
        fixture = jogo
        stats = fixture.get("stats", {}).get("data", [])
        minuto = fixture['time']['minute']
        status = fixture['time']['status']
        gols_casa = fixture["scores"]["localteam_score"]
        gols_fora = fixture["scores"]["visitorteam_score"]
        liga = fixture["league"]["data"]["name"]

        casa = fixture["teams"]["data"]["localteam"]["name"]
        fora = fixture["teams"]["data"]["visitorteam"]["name"]

        # Calcula escanteios
        total_escanteios = 0
        for item in stats:
            if item.get("type") == "corners":
                local = int(item.get("value", {}).get("localteam", 0))
                visitante = int(item.get("value", {}).get("visitorteam", 0))
                total_escanteios = local + visitante
                break

        if minuto is not None and minuto >= 70 and (gols_fora - gols_casa == 1):
            resultados.append(
                f"🟥 ESCANTEIOS\n🏟️ Liga: {liga}\n⏱ {minuto}min — {casa} perdendo pra {fora}\n"
                f"🔢 Placar: {gols_casa} x {gols_fora}\n"
                f"📊 Escanteios atuais: {total_escanteios}\n"
                f"🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
            )

    return resultados
