
import httpx

CATEGORY_ID = "MLB1000"

url = (
    f"https://api.mercadolibre.com/categories/"
    f"{CATEGORY_ID}/attributes"
)

response = httpx.get(url, timeout=30)

print("Status:", response.status_code)
response.raise_for_status()

atributos = response.json()

for atributo in atributos:
    print(
        atributo["id"],
        "-",
        atributo["name"],
        "- Obrigatório:",
        atributo.get("tags", {}).get("required", False)
    )