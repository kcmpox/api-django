def variaveis_globais(client_id, client_secret):
    variaveis = {
        "CLIENT_ID": client_id,
        "CLIENT_SECRET": client_secret,
    }

    faltando = [nome for nome, valor in variaveis.items() if not valor]

    if faltando:
        raise Exception(f"Variáveis ausentes: {', '.join(faltando)}")
