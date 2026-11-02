"""Consultas mensais e relatórios calculados com pandas."""

from dados import carregar_lancamentos
from lancamentos import CATEGORIAS


def resumir_mes(mes):
    """Calcula totais, saldo, despesas por categoria e lista do mês."""
    tabela = carregar_lancamentos()
    lancamentos_do_mes = tabela[tabela["data"].dt.strftime("%Y-%m") == mes]

    receitas = lancamentos_do_mes.loc[
        lancamentos_do_mes["tipo"] == "Receita", "valor"
    ].sum()
    despesas = lancamentos_do_mes.loc[
        lancamentos_do_mes["tipo"] == "Despesa", "valor"
    ].sum()
    despesas_por_categoria = (
        lancamentos_do_mes[lancamentos_do_mes["tipo"] == "Despesa"]
        .groupby("categoria")["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    lancamentos_ordenados = lancamentos_do_mes.sort_values(
        "data", ascending=False
    )
    return {
        "mes": mes,
        "receitas": float(receitas),
        "despesas": float(despesas),
        "saldo": float(receitas - despesas),
        "categorias": [
            {"nome": str(nome), "valor": float(valor)}
            for nome, valor in despesas_por_categoria.items()
        ],
        "lancamentos": [
            {
                "data": linha["data"].strftime("%Y-%m-%d"),
                "tipo": str(linha["tipo"]),
                "descricao": str(linha["descricao"]),
                "categoria": str(linha["categoria"]),
                "valor": float(linha["valor"]),
            }
            for _, linha in lancamentos_ordenados.iterrows()
        ],
        "opcoes_categoria": CATEGORIAS,
    }
