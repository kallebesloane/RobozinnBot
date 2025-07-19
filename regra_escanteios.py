print("[DEBUG] regra_escanteios.py carregado")

def verificar_escanteios(jogos):
    resultados = []

    for jogo in jogos:
        try:
            # Minuto do jogo
            minuto = jogo['time']['minute'] if 'time' in jogo and jogo['time'] else None
            if minuto is None or minuto < 70:
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
            gols_casa = jogo.get('scores', {}).get('home_score', 0)
            gols_fora = jogo.get('scores', {}).get('away_score', 0)

            if gols_fora - gols_casa == 1:
                liga = jogo.get('league', {}).get('name', 'Desconhecida')
                placar = f"{gols_casa} x {gols_fora}"
                resultados.append(
                    f"🟥 ESCANTEIOS\n🏟️ Liga: {liga}\n⏱ {minuto}min — {time_casa} perdendo pra {time_fora}\n🔢 Placar: {placar}\n🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
                )
        except Exception as e:
            print(f"[ERRO escanteios] {e}")
            continue

    return resultados
