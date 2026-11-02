"""Leitura e gravação dos lançamentos no CSV local."""

from pathlib import Path

import pandas as pd


PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "dados" / "lancamentos.csv"
COLUNAS = ["data", "tipo", "descricao", "categoria", "valor"]


def tabela_vazia():
    """Cria uma tabela vazia com as mesmas colunas usadas no CSV."""
    tabela = pd.DataFrame(columns=COLUNAS)
    tabela["data"] = pd.to_datetime(tabela["data"])
    tabela["valor"] = pd.to_numeric(tabela["valor"])
    return tabela


def carregar_lancamentos():
    """Lê o CSV e converte data e valor para os tipos usados pelo pandas."""
    if not ARQUIVO.exists():
        return tabela_vazia()

    try:
        tabela = pd.read_csv(ARQUIVO)
    except pd.errors.EmptyDataError:
        return tabela_vazia()
    except pd.errors.ParserError as erro:
        raise OSError("O arquivo de lançamentos está inválido.") from erro

    colunas_ausentes = set(COLUNAS) - set(tabela.columns)
    if colunas_ausentes:
        nomes = ", ".join(sorted(colunas_ausentes))
        raise OSError(f"Faltam colunas no arquivo de lançamentos: {nomes}.")

    tabela["data"] = pd.to_datetime(tabela["data"], errors="coerce")
    tabela["valor"] = pd.to_numeric(tabela["valor"], errors="coerce")
    return tabela.dropna(subset=["data", "valor"])


def salvar_lancamentos(tabela):
    """Salva apenas as colunas previstas, criando a pasta se necessário."""
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    tabela[COLUNAS].to_csv(ARQUIVO, index=False, date_format="%Y-%m-%d")
