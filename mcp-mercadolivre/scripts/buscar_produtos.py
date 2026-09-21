
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

url = "https://api.mercadolibre.com/users/me"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = httpx.get(
    url,
    headers=headers,
    timeout=30
)

print("Status:", response.status_code)
print("Request ID:", response.headers.get("x-request-id"))
print("Resposta:", response.text)

if response.status_code == 200:
    usuario = response.json()

    print("\nID do vendedor:", usuario["id"])
    print("Nickname:", usuario.get("nickname"))