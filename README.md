
## Funções

- Cadastrar receitas e despesas por categoria.
- Ver receitas, despesas e saldo de um mês.
- Ver despesas agrupadas por categoria.
- Consultar os lançamentos do mês.

## Executar no Windows

No PowerShell:

```powershell
cd local do projeto
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Os lançamentos ficam em `dados/lancamentos.csv`. Para iniciar o programa novamente, entre na pasta do projeto e execute `.\.venv\Scripts\python.exe app.py`.


