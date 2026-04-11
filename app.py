import os
from dotenv import load_dotenv

import functions.validador as validador
import functions.gerador as gerador

# Carregar variáveis de ambiente
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URL = "http://127.0.0.1:8000/o/token/"
AUTH_URL = "http://127.0.0.1:8000/o/authorize/"
REDIRECT_URI = "http://localhost:8080/callback"
API_URL = "http://127.0.0.1:8000/v1/api/"


def main():
    try:
        validador.variaveis_globais(CLIENT_ID, CLIENT_SECRET)
    except Exception as e:
        print("Erro de configuração:", e)
        return

    access_token, refresh_token = gerador.obter_token(CLIENT_ID, REDIRECT_URI, AUTH_URL, TOKEN_URL, CLIENT_SECRET)

    if access_token:
        print("\nAutenticação realizada com sucesso")
    else:
        print("\nFalha na autenticação")

if __name__ == "__main__":
    main()
