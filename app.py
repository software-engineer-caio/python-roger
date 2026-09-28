from datetime import date
from pathlib import Path

import pandas as pd


ARQUIVO = Path(__file__).parent / "dados" / "lancamentos.csv"
CATEGORIAS_DESPESA = [
    "Moradia",
    "Alimentação",
    "Transporte",
    "Saúde",
    "Educação",
    "Lazer",
    "Contas",
    "Outros",
]
CATEGORIAS_RECEITA = ["Salário", "Renda extra", "Benefícios", "Outros"]
COLUNAS = ["data", "tipo", "descricao", "categoria", "valor"]


def carregar_lancamentos():
    if ARQUIVO.exists():
        dados = pd.read_csv(ARQUIVO)
        dados["data"] = pd.to_datetime(dados["data"])
        return dados
    dados = pd.DataFrame(columns=COLUNAS)
    dados["data"] = pd.to_datetime(dados["data"])
    return dados


def salvar_lancamentos(dados):
    ARQUIVO.parent.mkdir(exist_ok=True)
    dados.to_csv(ARQUIVO, index=False, date_format="%Y-%m-%d")


def escolher_categoria(categorias):
    for numero, categoria in enumerate(categorias, start=1):
        print(f"{numero}. {categoria}")
    escolha = int(input("Categoria: "))
    return categorias[escolha - 1]


def cadastrar(dados, tipo):
    categorias = CATEGORIAS_DESPESA if tipo == "Despesa" else CATEGORIAS_RECEITA
    descricao = input("Descrição: ")
    valor = input("Valor (R$): ").strip().replace("R$", "").strip()
    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")
    valor = float(valor)

    print("Categorias:")
    categoria = escolher_categoria(categorias)
    hoje = date.today().isoformat()
    data_lancamento = input(f"Data (AAAA-MM-DD) [{hoje}]: ").strip() or hoje

    novo_lancamento = pd.DataFrame(
        [[pd.Timestamp(data_lancamento), tipo, descricao, categoria, valor]],
        columns=COLUNAS,
    )
    dados = pd.concat([dados, novo_lancamento], ignore_index=True)
    salvar_lancamentos(dados)
    print("Lançamento salvo.\n")
    return dados


def mes_selecionado():
    mes_atual = date.today().strftime("%Y-%m")
    return input(f"Mês (AAAA-MM) [{mes_atual}]: ").strip() or mes_atual


def consultar_mes(dados, mes):
    return dados[dados["data"].dt.strftime("%Y-%m") == mes]


def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar_resumo(dados):
    mes = mes_selecionado()
    lancamentos = consultar_mes(dados, mes)
    receitas = lancamentos.loc[lancamentos["tipo"] == "Receita", "valor"].sum()
    despesas = lancamentos.loc[lancamentos["tipo"] == "Despesa", "valor"].sum()

    print(f"\nResumo de {mes}")
    print(f"Receitas: {formatar_reais(receitas)}")
    print(f"Despesas: {formatar_reais(despesas)}")
    print(f"Saldo:    {formatar_reais(receitas - despesas)}\n")


def mostrar_relatorio(dados):
    mes = mes_selecionado()
    despesas = consultar_mes(dados, mes)
    despesas = despesas[despesas["tipo"] == "Despesa"]

    if despesas.empty:
        print("Não há despesas neste mês.\n")
        return

    totais = despesas.groupby("categoria")["valor"].sum().sort_values(ascending=False)
    print(f"\nDespesas por categoria — {mes}")
    for categoria, total in totais.items():
        print(f"{categoria}: {formatar_reais(total)}")
    print()


def mostrar_lancamentos(dados):
    mes = mes_selecionado()
    lancamentos = consultar_mes(dados, mes).sort_values("data")

    if lancamentos.empty:
        print("Não há lançamentos neste mês.\n")
        return

    print(f"\nLançamentos de {mes}")
    for _, lancamento in lancamentos.iterrows():
        data = lancamento["data"].strftime("%d/%m/%Y")
        valor = formatar_reais(lancamento["valor"])
        print(
            f"{data} | {lancamento['tipo']} | {lancamento['descricao']} | "
            f"{lancamento['categoria']} | {valor}"
        )
    print()


def main():
    dados = carregar_lancamentos()

    while True:
        print("MEU ORÇAMENTO")
        print("1. Cadastrar receita")
        print("2. Cadastrar despesa")
        print("3. Ver saldo do mês")
        print("4. Ver despesas por categoria")
        print("5. Ver lançamentos do mês")
        print("0. Sair")

        opcao = input("Escolha: ").strip()
        if opcao == "1":
            dados = cadastrar(dados, "Receita")
        elif opcao == "2":
            dados = cadastrar(dados, "Despesa")
        elif opcao == "3":
            mostrar_resumo(dados)
        elif opcao == "4":
            mostrar_relatorio(dados)
        elif opcao == "5":
            mostrar_lancamentos(dados)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    main()
