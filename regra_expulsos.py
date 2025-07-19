print("[DEBUG] regra_expulsos.py carregado")

def verificar_expulsos(jogos):
    resultados = []

    for jogo in jogos:
        stats = jogo.get("stats", {}).get("data", [])
        minuto = jogo["time"]["minute"]
        status = jogo["time"]["status"]

        casa = jogo["teams"]["data"]["localteam"]["name"]
        fora = jogo["teams"]["data"]["visitorteam"]["name"]
        liga = jogo["league"]["data"]["name"]

        vermelhos_casa = 0
        vermelhos_fora = 0

        # Verifica cartões vermelhos na estatística
        for item in stats:
            if item.get("type") == "redcards":
                valores = item.get("value", {})
                vermelhos_casa = int(valores.get("localteam", 0))
                vermelhos_fora = int(valores.get("visitorteam", 0))
                break

        # Se algum time tiver 1 ou mais cartões vermelhos
        if minuto is not None and minuto >= 30 and (vermelhos_casa > 0 or vermelhos_fora > 0):
            resultados.append(
                f"🟥 EXPULSÃO\n🏟️ Liga: {liga}\n⏱ {minuto}min\n"
                f"📌 Cartões vermelhos: {casa} {vermelhos_casa} x {vermelhos_fora} {fora}\n"
                f"🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
            )

    return resultados
