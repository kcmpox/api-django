from dotenv import load_dotenv

import requests
import json
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_USER = os.getenv("API_USER")
PASSWORD = os.getenv("PASSWORD")

TOKEN_URL = "http://127.0.0.1:8000/o/token/"
API_URL = "http://127.0.0.1:8000/v1/api/"

session = requests.Session()

def obter_token():
    data = {
        'grant_type': 'password',
        'username': API_USER,
        'password': PASSWORD
    }

    response = session.post(
        TOKEN_URL,
        data=data,
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=15
    )

    if response.status_code == 200:
        json_resp = response.json()

        # Evite printar token em produção
        print("Token obtido com sucesso")

        return json_resp['access_token'], json_resp.get('refresh_token')
    else:
        print(f"Erro ao obter token: {response.status_code}")
        print(response.text)
        return None, None


def fazer_requisicao(token):
    headers = {'Authorization': f"Bearer {token}"}

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
    with open('pesquisa.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("Dados salvos em pesquisa.json")


def main():
    access_token, refresh_token = obter_token()

    if not access_token:
        print("Não foi possível obter o token de acesso.")
        return

    dados = fazer_requisicao(access_token)

    if dados:
        salvar_json(dados)
    else:
        print("Nenhum dado recebido da API.")


if __name__ == "__main__":
    main()
