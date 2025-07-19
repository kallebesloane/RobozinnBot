print("[DEBUG] regra_expulsos.py carregado")

def verificar_expulsos(jogos):
    resultados = []

    for jogo in jogos:
        try:
            minuto = jogo.get('time', {}).get('minute')
            if minuto is None or minuto < 45:
                continue

            participantes = jogo.get('participants', [])
            if len(participantes) < 2:
                continue

            casa = [p for p in participantes if p.get('meta', {}).get('location') == 'home']
            fora = [p for p in participantes if p.get('meta', {}).get('location') == 'away']

            if not casa or not fora:
                continue

            time_casa = casa[0]['name']
            time_fora = fora[0]['name']
            red_casa = casa[0].get('meta', {}).get('redcards', 0)
            red_fora = fora[0].get('meta', {}).get('redcards', 0)

            if red_casa > 0 or red_fora > 0:
                liga = jogo.get('league', {}).get('name', 'Desconhecida')
                placar = f"{jogo.get('scores', {}).get('home_score', 0)} x {jogo.get('scores', {}).get('away_score', 0)}"
                mensagem = (
                    f"🚨 EXPULSO\n"
                    f"🏟️ Liga: {liga}\n"
                    f"⏱ {minuto}min — {time_casa} x {time_fora}\n"
                    f"🟥 Vermelhos: {red_casa} x {red_fora}\n"
                    f"🔢 Placar: {placar}\n"
                    f"🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
                )
                resultados.append(mensagem)
        except Exception as e:
            print(f"[ERRO expulsos] {e}")
            continue

    return resultados
