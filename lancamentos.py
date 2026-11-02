"""Validação e cadastro de receitas e despesas."""

from datetime import datetime
from math import isfinite

import pandas as pd

from dados import COLUNAS, carregar_lancamentos, salvar_lancamentos


CATEGORIAS = {
    "Despesa": [
        "Moradia",
        "Alimentação",
        "Transporte",
        "Saúde",
        "Educação",
        "Lazer",
        "Contas",
        "Outros",
    ],
    "Receita": ["Salário", "Renda extra", "Benefícios", "Outros"],
}


def adicionar_lancamento(item):
    """Valida os campos recebidos e acrescenta o lançamento ao CSV."""
    tipo = item.get("tipo")
    descricao = str(item.get("descricao", "")).strip()
    categoria = item.get("categoria")

    if not isinstance(tipo, str) or tipo not in CATEGORIAS:
        raise ValueError("Escolha receita ou despesa.")
    if not descricao:
        raise ValueError("Informe uma descrição.")
    if categoria not in CATEGORIAS[tipo]:
        raise ValueError("Escolha uma categoria válida.")

    try:
        valor = float(item.get("valor"))
    except (TypeError, ValueError):
        raise ValueError("Informe um valor válido.") from None
    if not isfinite(valor) or valor <= 0:
        raise ValueError("O valor precisa ser maior que zero.")

    try:
        data = datetime.strptime(item.get("data"), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("Informe uma data válida.") from None

    tabela = carregar_lancamentos()
    novo_lancamento = pd.DataFrame(
        [[pd.Timestamp(data), tipo, descricao, categoria, valor]],
        columns=COLUNAS,
    )
    salvar_lancamentos(pd.concat([tabela, novo_lancamento], ignore_index=True))
