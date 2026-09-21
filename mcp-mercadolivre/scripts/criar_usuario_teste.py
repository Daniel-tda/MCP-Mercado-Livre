import httpx

url = "https://api.mercadopago.com/users/test"

headers = {
    "Authorization": "Bearer APP_USR-7558592198900045-092100-dec8bf2abbfd9425132d9ed55ca2ce36-1127877529",
    "Content-Type": "application/json"
}

payload = {
    "site_id": "MLB",
    "description": "Usuario de teste MCP Voler Cloud"
}

response = httpx.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())