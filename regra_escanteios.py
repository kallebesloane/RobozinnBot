print("[DEBUG] regra_escanteios.py carregado")
def verificar_escanteios(jogos):
    resultados = []

    for jogo in jogos:
        minuto = jogo['fixture']['status']['elapsed']
        gols_casa = jogo['goals']['home']
        gols_fora = jogo['goals']['away']
        liga = jogo['league']['name']

        if minuto is not None and minuto >= 70 and (gols_fora - gols_casa == 1):
            casa = jogo['teams']['home']['name']
            fora = jogo['teams']['away']['name']
            placar = f"{gols_casa} x {gols_fora}"
            resultados.append(
                f"🟥 ESCANTEIOS\n🏟️ Liga: {liga}\n⏱ {minuto}min — {casa} perdendo pra {fora}\n🔢 Placar: {placar}\n🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
            )

    return resultados
