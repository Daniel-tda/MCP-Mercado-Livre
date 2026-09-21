
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

url = "https://api.mercadolibre.com/sites/MLB/categories"

headers = {}

if ACCESS_TOKEN:
    headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

try:
    response = httpx.get(
        url,
        headers=headers,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Request ID:", response.headers.get("x-request-id"))
    print("Bloqueio:", response.headers.get("x-policy-agent-block-code"))
    print("Resposta:", response.text)

    if response.status_code == 200:
        for categoria in response.json():
            print(categoria["id"], "-", categoria["name"])

except httpx.RequestError as erro:
    print("Erro de conexão:", erro)