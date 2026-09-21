"""
Cliente para a API do Mercado Livre.

Centraliza todas as chamadas HTTP, para que as tools do servidor MCP
(em src/tools/) não precisem lidar com URLs, headers ou tokens diretamente.

Endpoints mapeados durante o estudo da documentação:
- Pedidos:  GET /orders/search?seller=$SELLER_ID
- Itens:    GET /users/$USER_ID/items/search  (lista IDs)
            GET /items/$ITEM_ID               (detalhe, incl. available_quantity)
- Faturamento: GET /billing/integration/monthly/periods
               GET /billing/integration/periods/key/{key}/documents
               GET /billing/integration/periods/key/{key}/summary/details
"""

import os
from tokenize import group
import httpx

BASE_URL = "https://api.mercadolibre.com"


class MercadoLivreClient:
    def __init__(self):
        self.access_token = os.getenv("ML_ACCESS_TOKEN")
        self.seller_id = os.getenv("ML_SELLER_ID", "").strip()

        if not self.access_token:
            raise RuntimeError(
                "ML_ACCESS_TOKEN não configurado. Rode o fluxo OAuth primeiro (ver auth.py)."
            )

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    async def _get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}{path}", headers=self._headers(), params=params
            )
            response.raise_for_status()
            return response.json()

    # --- Pedidos / vendas ---

    async def search_orders(
        self, date_from: str | None = None, date_to: str | None = None, status: str | None = None
    ) -> dict:
        
        seller_id = str(self.seller_id).strip()

        if not seller_id.isdigit():
            raise ValueError("ML_SELLER_ID deve conter apenas números.")

        params = {"seller": seller_id}
        
        if status:
            params["order.status"] = status
        # TODO: confirmar na documentação os nomes exatos dos parâmetros de filtro por data
        # (ex: order.date_created.from / order.date_created.to)
        return await self._get("/orders/search", params=params)

    # --- Itens / estoque ---

    async def list_item_ids(self) -> list[str]:
        data = await self._get(f"/users/{self.seller_id}/items/search")
        return data.get("results", [])

    async def get_item(self, item_id: str) -> dict:
        return await self._get(f"/items/{item_id}")

    async def list_items_with_stock(self) -> list[dict]:
        """Combina list_item_ids + get_item para retornar itens com available_quantity."""
        item_ids = await self.list_item_ids()
        items = []
        for item_id in item_ids:
            item = await self.get_item(item_id)
            items.append(item)
        return items

    # --- Faturamento ---

    
    async def get_billing_periods(
        self,
        group: str = "ML",
        document_type: str = "BILL",
    ) -> dict:
        if group not in {"ML", "MP"}:
            raise ValueError("group deve ser 'ML' ou 'MP'.")

        if document_type not in {"BILL", "CREDIT_NOTE"}:
            raise ValueError(
                "document_type deve ser 'BILL' ou 'CREDIT_NOTE'."
        )

        return await self._get(
            "/billing/integration/monthly/periods",
            params={
                "group": group,
                "document_type": document_type,
                "offset": 0,
                "limit": 6,
            },
        )

    async def get_billing_summary(self, period_key: str, group: str = "ML") -> dict:
        return await self._get(
            f"/billing/integration/periods/key/{period_key}/summary/details",
            params={"group": group},
        )
