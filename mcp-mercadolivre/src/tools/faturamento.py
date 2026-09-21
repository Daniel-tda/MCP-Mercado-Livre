
"""Tool: gerar_relatorio_faturamento."""

import httpx
from ml_client import MercadoLivreClient


async def gerar_relatorio_faturamento(group: str = "ML") -> dict:
    if group not in {"ML", "MP"}:
        return {
            "erro": "Grupo inválido. Utilize 'ML' ou 'MP'."
        }

    client = MercadoLivreClient()

    try:
        periods = await client.get_billing_periods(group=group)

        resultados = periods.get("results", [])

        if not resultados:
            return {
                "periodo": None,
                "grupo": group,
                "disponivel": False,
                "mensagem": (
                    "Nenhum período de faturamento disponível "
                    "para este grupo."
                ),
                "faturamento_bruto": None,
                "faturamento_liquido": None,
            }

        period_key = resultados[0].get("key")

        if not period_key:
            return {
                "erro": "A API não retornou a chave do período."
            }

        summary = await client.get_billing_summary(
            period_key,
            group=group,
        )

        return {
            "periodo": period_key,
            "grupo": group,
            "disponivel": True,
            "resumo": summary,
        }

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 429:
            return {
                "erro": "Limite de requisições da API do Mercado Livre atingido.",
                "status_code": 429,
                "mensagem": (
                    "Aguarde antes de tentar novamente. "
                    "Nenhum resultado de faturamento foi confirmado."
                ),
            }

        return {
            "erro": "A API do Mercado Livre retornou um erro HTTP.",
            "status_code": status_code,
        }