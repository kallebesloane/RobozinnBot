print("[DEBUG] regra_escanteios.py carregado")

from probabilidade_escanteios import calcular_probabilidade_escanteios

def verificar_escanteios(jogos):
    resultados = []

    for jogo in jogos:
        minuto = jogo['fixture']['status']['elapsed']
        gols_casa = jogo['goals']['home']
        gols_fora = jogo['goals']['away']
        liga = jogo['league']['name']
        casa = jogo['teams']['home']['name']
        fora = jogo['teams']['away']['name']
        id_casa = jogo['teams']['home']['id']
        id_fora = jogo['teams']['away']['id']

        # Alerta se for a partir dos 70 minutos e time da casa estiver perdendo por 1
        if minuto is not None and minuto >= 70 and (gols_fora - gols_casa == 1):

            resultados.append(
                f"🟥 ESCANTEIOS\n🏟️ Liga: {liga}\n⏱ {minuto}min — {casa} perdendo pra {fora}\n🔢 Placar: {gols_casa} x {gols_fora}"
            )

    return resultados
