"""Tool: gerar_relatorio_faturamento."""

from ml_client import MercadoLivreClient


async def gerar_relatorio_faturamento(group: str = "ML") -> dict:
    """
    Retorna o resumo de faturamento do período mais recente disponível.

    Fluxo (ver documentação "Relatórios de Faturamento"):
    1. /billing/integration/monthly/periods -> pega a "key" do período
    2. /billing/integration/periods/key/{key}/summary/details -> resumo

    TODO: hoje só pega o período mais recente; considerar permitir
    escolher o período via parâmetro.
    """
    client = MercadoLivreClient()

    periods = await client.get_billing_periods()
    # TODO: confirmar o nome exato do campo que traz a "key" na resposta de /periods
    period_key = periods["results"][0]["key"]

    summary = await client.get_billing_summary(period_key, group=group)
    return {"periodo": period_key, "resumo": summary}
