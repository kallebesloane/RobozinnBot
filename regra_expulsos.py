def verificar_expulsos(jogos):
    resultados = []

    for jogo in jogos:
        minuto = jogo['fixture']['status']['elapsed']
        gols_casa = jogo['goals']['home']
        gols_fora = jogo['goals']['away']
        liga = jogo['league']['name']
        casa = jogo['teams']['home']['name']
        fora = jogo['teams']['away']['name']

        # Verifica cartões vermelhos da casa
        estatisticas = jogo.get('teams', {}).get('home', {})
        vermelhos = estatisticas.get('red', 0)

        # Se o campo 'red' não existir, tenta outro jeito
        if vermelhos is None:
            cards = jogo.get('statistics', [])
            vermelhos = 0
            for time in cards:
                if time['team']['name'] == casa:
                    for estat in time['statistics']:
                        if estat['type'] == 'Red Cards':
                            vermelhos = estat['value']

        if minuto is not None and minuto >= 70 and (gols_casa - gols_fora == 1) and vermelhos >= 1:
            placar = f"{gols_casa} x {gols_fora}"
            resultados.append(
                f"⚠️ EXPULSÃO EM TIME VENCENDO\n🏟️ Liga: {liga}\n⏱ {minuto}min — {casa} vencendo por 1 gol mas com jogador expulso!\n🔢 Placar: {placar}\n🟥 Cartões vermelhos: {vermelhos}\n🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
            )

    return resultados
