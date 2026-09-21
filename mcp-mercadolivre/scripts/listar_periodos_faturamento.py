import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

BASE_URL = "https://api.mercadolibre.com"


def listar_periodos_faturamento():
    if not ACCESS_TOKEN:
        print("Erro: ML_ACCESS_TOKEN não encontrado no .env")
        return

    url = f"{BASE_URL}/billing/integration/monthly/periods"

    params = {
        "group": "ML",
        "document_type": "BILL",
        "offset": 0,
        "limit": 6,
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = httpx.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        print(f"Status HTTP: {response.status_code}")

        response.raise_for_status()

        dados = response.json()

        print("\nResposta completa da API:")
        print(dados)

        resultados = dados.get("results", [])

        if not resultados:
            print("\nNenhum período de faturamento retornado.")
            return

        print("\nPeríodos de faturamento:\n")

        for periodo in dados.get("results", []):
            print(f"Chave: {periodo.get('key')}")
            print(f"Início: {periodo.get('period', {}).get('date_from')}")
            print(f"Fim: {periodo.get('period', {}).get('date_to')}")
            print(f"Status: {periodo.get('period_status')}")
            print(f"Valor: {periodo.get('amount')}")
            print(f"Pendente: {periodo.get('unpaid_amount')}")
            print("-" * 40)

    except httpx.HTTPStatusError as erro:
        status = erro.response.status_code

        if status == 429:
            print("Limite de requisições atingido (HTTP 429).")
            print("Aguarde antes de tentar novamente.")
            print("Resposta:", erro.response.text)
        else:
            print("Erro HTTP:", status)
            print(erro.response.text)

    except httpx.RequestError as erro:
        print("Erro de conexão:", erro)


if __name__ == "__main__":
    listar_periodos_faturamento()