import secrets
import hashlib
import base64
from urllib.parse import urlencode
import requests


def gerar_pkce():
    code_verifier = secrets.token_urlsafe(64)

    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )

    return code_verifier, code_challenge


def gerar_url_autorizacao(code_challenge, CLIENT_ID, REDIRECT_URI, AUTH_URL):
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


def trocar_code_por_token(
    code, code_verifier, REDIRECT_URI, TOKEN_URL, CLIENT_ID, CLIENT_SECRET
):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    try:
        response = requests.Session().post(
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


def obter_token(CLIENT_ID, REDIRECT_URI, AUTH_URL, TOKEN_URL, CLIENT_SECRET):
    code_verifier, code_challenge = gerar_pkce()

    url = gerar_url_autorizacao(code_challenge, CLIENT_ID, REDIRECT_URI, AUTH_URL)

    print("Acesse:", url)

    code = obter_code()

    return trocar_code_por_token(
        code, code_verifier, REDIRECT_URI, TOKEN_URL, CLIENT_ID, CLIENT_SECRET
    )
