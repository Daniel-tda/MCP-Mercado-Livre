"""Tools: listar_vendas e produtos_mais_vendidos."""

from collections import defaultdict
from ml_client import MercadoLivreClient


async def listar_vendas(date_from: str | None = None, date_to: str | None = None, status: str | None = None) -> dict:
    """
    Retorna as vendas (pedidos) do vendedor em um período.

    Args:
        date_from: data inicial (formato TODO: confirmar na documentação)
        date_to: data final
        status: status do pedido (ex: "paid", "cancelled")
    """
    client = MercadoLivreClient()
    data = await client.search_orders(date_from=date_from, date_to=date_to, status=status)

    vendas = []
    for order in data.get("results", []):
        vendas.append(
            {
                "id": order["id"],
                "status": order["status"],
                "data": order["date_created"],
                "total": order["total_amount"],
                "itens": [
                    {"produto": i["item"]["title"], "quantidade": i["quantity"]}
                    for i in order.get("order_items", [])
                ],
            }
        )
    return {"total_vendas": len(vendas), "vendas": vendas}


async def produtos_mais_vendidos(date_from: str | None = None, date_to: str | None = None, limite: int = 5) -> dict:
    """
    Rankeia os produtos mais vendidos em um período.

    Não existe endpoint pronto pra isso na API — a agregação é feita aqui,
    somando as quantidades vendidas por item a partir de /orders/search.
    """
    client = MercadoLivreClient()
    data = await client.search_orders(date_from=date_from, date_to=date_to, status="paid")

    contagem = defaultdict(int)
    for order in data.get("results", []):
        for item in order.get("order_items", []):
            contagem[item["item"]["title"]] += item["quantity"]

    ranking = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:limite]
    return {"ranking": [{"produto": nome, "quantidade_vendida": qtd} for nome, qtd in ranking]}
