"""
Servidor MCP do Mercado Livre.

Expõe 6 tools para consultar vendas, estoque e faturamento de um vendedor,
para uso por um cliente MCP (ex: Gemini Enterprise Business).

Transporte: StreamableHTTP (exigido pelo Gemini Enterprise Business).

Como rodar localmente para testes via HTTP:
    python src/server.py
    (sobe em http://0.0.0.0:8080/mcp por padrão)

Como rodar no Cloud Run: o Cloud Run injeta automaticamente a variável de
ambiente PORT — o código abaixo já lê essa variável, então não precisa
configurar nada manualmente.
"""

import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from tools.vendas import listar_vendas, produtos_mais_vendidos
from tools.estoque import consultar_estoque, produtos_com_estoque_baixo, detalhar_produto
from tools.faturamento import gerar_relatorio_faturamento

load_dotenv()

# Cloud Run injeta a porta em que a aplicação deve escutar via a variável PORT.
# Localmente, se PORT não estiver definida, cai no padrão 8080.
PORT = int(os.environ.get("PORT", 8080))

mcp = FastMCP("mercado-livre", host="0.0.0.0", port=PORT)


@mcp.tool()
async def listar_vendas_tool(
    date_from: str | None = None, date_to: str | None = None, status: str | None = None
) -> dict:
    """Lista as vendas (pedidos) do vendedor em um período, opcionalmente filtradas por status."""
    return await listar_vendas(date_from, date_to, status)


@mcp.tool()
async def consultar_estoque_tool(item_id: str | None = None) -> dict:
    """Consulta o estoque de um produto específico (por ID) ou de todos os produtos."""
    return await consultar_estoque(item_id)


@mcp.tool()
async def gerar_relatorio_faturamento_tool(group: str = "ML") -> dict:
    """Gera o resumo de faturamento do período mais recente. group: 'ML' ou 'MP'."""
    return await gerar_relatorio_faturamento(group)


@mcp.tool()
async def detalhar_produto_tool(item_id: str) -> dict:
    """Retorna detalhes completos de um produto: título, preço, estoque e status."""
    return await detalhar_produto(item_id)


@mcp.tool()
async def produtos_mais_vendidos_tool(
    date_from: str | None = None, date_to: str | None = None, limite: int = 5
) -> dict:
    """Retorna o ranking dos produtos mais vendidos em um período."""
    return await produtos_mais_vendidos(date_from, date_to, limite)


@mcp.tool()
async def produtos_com_estoque_baixo_tool(limite_minimo: int = 5) -> dict:
    """Lista produtos com estoque disponível abaixo do limite informado."""
    return await produtos_com_estoque_baixo(limite_minimo)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")