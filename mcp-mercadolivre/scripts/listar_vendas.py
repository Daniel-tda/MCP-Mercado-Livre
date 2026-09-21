
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Identificar o vendedor autenticado
url_usuario = "https://api.mercadolibre.com/users/me"

response_usuario = httpx.get(
    url_usuario,
    headers=headers,
    timeout=30
)

response_usuario.raise_for_status()

seller_id = response_usuario.json()["id"]

print("Vendedor:", seller_id)

# Consultar pedidos de venda
url_vendas = (
    f"https://api.mercadolibre.com/orders/search"
)

params = {
    "seller": seller_id,
    "sort": "date_desc",
    "limit": 10
}

response_vendas = httpx.get(
    url_vendas,
    headers=headers,
    params=params,
    timeout=30
)

print("Status vendas:", response_vendas.status_code)
print("Resposta:", response_vendas.text)

response_vendas.raise_for_status()

dados = response_vendas.json()

print("\nTotal de vendas:", dados.get("paging", {}).get("total", 0))

for venda in dados.get("results", []):
    print("\nPedido:", venda.get("id"))
    print("Status:", venda.get("status"))
    print("Valor:", venda.get("total_amount"))