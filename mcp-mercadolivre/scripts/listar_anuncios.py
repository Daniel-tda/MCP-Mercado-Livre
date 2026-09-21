
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Primeiro, identificamos o vendedor autenticado
url_usuario = "https://api.mercadolibre.com/users/me"

response_usuario = httpx.get(
    url_usuario,
    headers=headers,
    timeout=30
)

response_usuario.raise_for_status()

usuario = response_usuario.json()
seller_id = usuario["id"]

print("Vendedor:", seller_id)

# Depois, consultamos os anúncios
url_anuncios = (
    f"https://api.mercadolibre.com/users/"
    f"{seller_id}/items/search"
)

response_anuncios = httpx.get(
    url_anuncios,
    headers=headers,
    params={"limit": 10},
    timeout=30
)

print("Status anúncios:", response_anuncios.status_code)
print("Resposta:", response_anuncios.text)

response_anuncios.raise_for_status()

dados = response_anuncios.json()

print("\nTotal de anúncios:", dados.get("paging", {}).get("total", 0))

for item_id in dados.get("results", []):
    print("Anúncio:", item_id)