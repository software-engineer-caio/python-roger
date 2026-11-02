# Meu Orçamento

Protótipo local com uma interface HTML simples. O servidor usa recursos que já vêm com Python, e pandas é a única dependência externa. Os lançamentos são salvos em um CSV local.

## Funções

- Cadastrar receitas e despesas por categoria.
- Consultar receitas, despesas e saldo do mês.
- Ver despesas agrupadas por categoria.
- Consultar lançamentos do mês.

## Executar no Windows

No PowerShell, entre na pasta do projeto e rode:

```powershell
cd C:\Users\caio\Desktop\python\python-roger
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

O comando inicia o servidor Python no terminal. Com ele em execução, abra `http://127.0.0.1:8000` no navegador para usar a interface HTML; o terminal não é a interface do sistema. Para encerrar o servidor, pressione Ctrl+C no terminal. Nas próximas vezes, basta ativar o ambiente virtual e executar `python app.py`.

## Organização do código

- `index.html`: interface para cadastrar e consultar lançamentos.
- `app.py`: servidor local e comunicação entre a interface e os módulos.
- `lancamentos.py`: categorias, validação e cadastro de receitas e despesas.
- `dados.py`: leitura e gravação do arquivo `dados/lancamentos.csv` com pandas.
- `relatorios.py`: resumo mensal e despesas agrupadas por categoria com pandas.

Divisão atual da squad: Arthur cuida de `lancamentos.py`; Gustavo cuida de `relatorios.py`, `dados.py` e `app.py`; Caio cuida da qualidade e documentação. O pandas é a única dependência externa; o servidor usa recursos que já vêm com Python.

O protótipo é de uso local e não inclui integração bancária ou Pix, múltiplos usuários, notificações ou previsão de investimentos.
