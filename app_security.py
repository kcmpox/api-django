import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode

import secrets
import hashlib
import base64

import json

# Carregar variáveis de ambiente
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URL = "http://127.0.0.1:8000/o/token/"
AUTH_URL = "http://127.0.0.1:8000/o/authorize/"
REDIRECT_URI = "http://localhost:8080/callback"
API_URL = "http://127.0.0.1:8000/v1/api/"

session = requests.Session()


def gerar_pkce():
    code_verifier = secrets.token_urlsafe(64)

    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )

    return code_verifier, code_challenge


def validar_variaveis_globais():
    variaveis = {
        "CLIENT_ID": CLIENT_ID,
        "CLIENT_SECRET": CLIENT_SECRET,
    }

    faltando = [nome for nome, valor in variaveis.items() if not valor]

    if faltando:
        raise Exception(f"Variáveis ausentes: {', '.join(faltando)}")


def gerar_url_autorizacao(code_challenge):
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    return f"{AUTH_URL}?{urlencode(params)}"


def obter_code():
    print("\nApós login, você será redirecionado para uma URL.")
    print("Copie apenas o valor do parâmetro 'code'.\n")
    return input("Cole o code aqui: ").strip()


def trocar_code_por_token(code, code_verifier):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    try:
        response = session.post(
            TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET), timeout=15
        )
    except requests.exceptions.RequestException as e:
        print("Erro de conexão:", e)
        return None, None

    if response.status_code == 200:
        json_resp = response.json()
        print("Token obtido com sucesso")
        return json_resp["access_token"], json_resp.get("refresh_token")
    else:
        print("Erro ao obter token:", response.status_code)
        print(response.text)
        return None, None


def obter_token():
    code_verifier, code_challenge = gerar_pkce()

    url = gerar_url_autorizacao(code_challenge)

    print("Acesse:", url)

    code = obter_code()

    return trocar_code_por_token(code, code_verifier)


def fazer_requisicao(token):
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = session.get(API_URL, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


def salvar_json(dados):
    with open("pesquisa.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("Dados salvos em pesquisa.json")


def main():
    try:
        validar_variaveis_globais()
    except Exception as e:
        print("Erro de configuração:", e)
        return

    access_token, refresh_token = obter_token()

    if access_token:
        print("\nAutenticação realizada com sucesso")
    else:
        print("\nFalha na autenticação")

    dados = fazer_requisicao(access_token)
    salvar_json(dados)


if __name__ == "__main__":
    main()
