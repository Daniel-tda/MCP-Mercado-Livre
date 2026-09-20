"""Tools: consultar_estoque, produtos_com_estoque_baixo e detalhar_produto."""

from ml_client import MercadoLivreClient


async def consultar_estoque(item_id: str | None = None) -> dict:
    """
    Retorna o estoque de um produto específico, ou de todos se item_id não for informado.
    """
    client = MercadoLivreClient()

    if item_id:
        item = await client.get_item(item_id)
        return {"produto": item["title"], "estoque": item["available_quantity"]}

    items = await client.list_items_with_stock()
    return {
        "produtos": [
            {"id": i["id"], "produto": i["title"], "estoque": i["available_quantity"]}
            for i in items
        ]
    }


async def produtos_com_estoque_baixo(limite_minimo: int = 5) -> dict:
    """
    Lista produtos com estoque abaixo do limite informado.

    Também não existe endpoint pronto — reusa a mesma base de dados
    de consultar_estoque e filtra localmente.
    """
    client = MercadoLivreClient()
    items = await client.list_items_with_stock()

    baixos = [
        {"id": i["id"], "produto": i["title"], "estoque": i["available_quantity"]}
        for i in items
        if i["available_quantity"] < limite_minimo
    ]
    return {"limite_minimo": limite_minimo, "produtos_com_estoque_baixo": baixos}


async def detalhar_produto(item_id: str) -> dict:
    """Retorna informações completas de um produto (preço, estoque, status)."""
    client = MercadoLivreClient()
    item = await client.get_item(item_id)

    return {
        "id": item["id"],
        "titulo": item["title"],
        "preco": item["price"],
        "estoque": item["available_quantity"],
        "status": item["status"],
    }
