"""
Fluxo de autenticação OAuth 2.0 do Mercado Livre.

Rode este script uma vez para obter o access_token e refresh_token
do usuário de teste, e cole os valores no seu .env.

TODO: revisar contra a documentação oficial de Autenticação e Autorização
(URL exata de autorização, nomes de parâmetros, tempo de expiração do token).
"""

import os
import webbrowser
import httpx
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("ML_CLIENT_ID")
CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")
REDIRECT_URI = os.getenv("ML_REDIRECT_URI")

AUTH_URL = (
    f"https://auth.mercadolivre.com.br/authorization"
    f"?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
)


def step_1_open_authorization_url():
    print("Abrindo navegador para autorizar a aplicação...")
    print(AUTH_URL)
    webbrowser.open(AUTH_URL)
    print("\nApós autorizar, copie o parâmetro 'code' da URL de redirecionamento.")


def step_2_exchange_code_for_token(auth_code: str) -> dict:
    response = httpx.post(
        "https://api.mercadolibre.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
        },
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    step_1_open_authorization_url()
    code = input("\nCole aqui o código de autorização (code=...): ").strip()
    tokens = step_2_exchange_code_for_token(code)
    print("\nAdicione estes valores ao seu .env:")
    print(f"ML_ACCESS_TOKEN={tokens['access_token']}")
    print(f"ML_REFRESH_TOKEN={tokens['refresh_token']}")
