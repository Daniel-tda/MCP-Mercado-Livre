# MCP Mercado Livre

Servidor MCP que expõe vendas, estoque e faturamento de um vendedor do
Mercado Livre, para uso por um cliente MCP (ex: Gemini Enterprise Business).

Projeto desenvolvido como teste técnico para a Voler Cloud.

## Status

Esqueleto inicial — estrutura e tools definidas, chamadas à API ainda
não testadas contra dados reais.

## Estrutura

```
src/
├── server.py       # Servidor MCP, registra as 6 tools
├── ml_client.py    # Cliente HTTP para a API do Mercado Livre
├── auth.py         # Script para rodar o fluxo OAuth 2.0 manualmente
└── tools/
    ├── vendas.py       # listar_vendas, produtos_mais_vendidos
    ├── estoque.py      # consultar_estoque, produtos_com_estoque_baixo, detalhar_produto
    └── faturamento.py  # gerar_relatorio_faturamento
```

## Setup

1. Criar ambiente virtual e instalar dependências:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copiar `.env.example` para `.env` e preencher `ML_CLIENT_ID`,
   `ML_CLIENT_SECRET` e `ML_REDIRECT_URI` (obtidos ao registrar a
   aplicação em developers.mercadolivre.com.br).

3. Rodar o fluxo de autenticação:
   ```
   python src/auth.py
   ```
   Copiar o `access_token` e `refresh_token` retornados para o `.env`.

4. Rodar o servidor:
   ```
   python src/server.py
   ```

## Tools disponíveis

| Tool | Descrição |
|---|---|
| `listar_vendas_tool` | Lista vendas de um período |
| `consultar_estoque_tool` | Estoque de um produto ou de todos |
| `gerar_relatorio_faturamento_tool` | Resumo de faturamento do período |
| `detalhar_produto_tool` | Detalhes completos de um produto |
| `produtos_mais_vendidos_tool` | Ranking dos mais vendidos |
| `produtos_com_estoque_baixo_tool` | Produtos abaixo de um limite de estoque |

## Pendências conhecidas

- Confirmar nomes exatos dos parâmetros de filtro por data em `/orders/search`
- Confirmar formato de `date_from`/`date_to`
- Testar contra usuário de teste real e ajustar nomes de campos conforme resposta real da API
- Implementar refresh automático de token quando expirar
