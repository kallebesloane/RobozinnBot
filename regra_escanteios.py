print("[DEBUG] regra_escanteios.py carregado")

def verificar_sinais(jogos):
    resultados = []

    for jogo in jogos:
        try:
            minuto = jogo.get('time', {}).get('minute')
            gols_casa = jogo.get('scores', {}).get('localteam_score')
            gols_fora = jogo.get('scores', {}).get('visitorteam_score')
            liga = jogo.get('league', {}).get('data', {}).get('name', 'Desconhecida')
            
            participantes = jogo.get('participants', {}).get('data', [])
            casa = ""
            fora = ""
            for p in participantes:
                if p.get('meta', {}).get('location') == 'home':
                    casa = p.get('name')
                elif p.get('meta', {}).get('location') == 'away':
                    fora = p.get('name')

            if minuto is not None and minuto >= 70 and gols_casa is not None and gols_fora is not None:
                if (gols_fora - gols_casa) == 1:
                    placar = f"{gols_casa} x {gols_fora}"
                    resultados.append(
                        f"🟥 ESCANTEIOS\n🏟️ Liga: {liga}\n⏱ {minuto}min — {casa} perdendo pra {fora}\n🔢 Placar: {placar}\n🔗 [Aposte](https://www.bet365.com/#/IP/B1)"
                    )
        except Exception as e:
            print(f"[ERRO] ao processar jogo: {e}")

    return resultados
