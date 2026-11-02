"""Servidor local que conecta a interface aos módulos do sistema."""

from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from lancamentos import adicionar_lancamento
from relatorios import resumir_mes


PAGINA = Path(__file__).resolve().parent / "index.html"


class Aplicacao(BaseHTTPRequestHandler):
    def responder(self, status, conteudo, tipo_conteudo):
        self.send_response(status)
        self.send_header("Content-Type", tipo_conteudo)
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(conteudo)

    def responder_json(self, status, objeto):
        conteudo = json.dumps(objeto, ensure_ascii=False).encode("utf-8")
        self.responder(status, conteudo, "application/json; charset=utf-8")

    def do_GET(self):
        caminho = urlparse(self.path)

        if caminho.path == "/":
            try:
                pagina = PAGINA.read_bytes()
            except OSError:
                self.responder_json(500, {"erro": "Não foi possível abrir a interface."})
                return
            self.responder(200, pagina, "text/html; charset=utf-8")
            return

        if caminho.path == "/api/dados":
            parametros = parse_qs(caminho.query)
            mes = parametros.get("mes", [date.today().strftime("%Y-%m")])[0]
            try:
                datetime.strptime(mes, "%Y-%m")
            except ValueError:
                self.responder_json(400, {"erro": "Mês inválido. Use AAAA-MM."})
                return

            try:
                resumo = resumir_mes(mes)
            except OSError as erro:
                self.responder_json(500, {"erro": str(erro)})
                return
            self.responder_json(200, resumo)
            return

        self.responder_json(404, {"erro": "Página não encontrada."})

    def do_POST(self):
        if urlparse(self.path).path != "/api/lancamentos":
            self.responder_json(404, {"erro": "Endereço não encontrado."})
            return

        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            item = json.loads(self.rfile.read(tamanho).decode("utf-8"))
            if not isinstance(item, dict):
                raise ValueError("Os dados enviados não são válidos.")
            adicionar_lancamento(item)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.responder_json(400, {"erro": "Os dados enviados não são válidos."})
            return
        except ValueError as erro:
            self.responder_json(400, {"erro": str(erro)})
            return
        except OSError as erro:
            self.responder_json(
                500,
                {"erro": f"Não foi possível salvar o lançamento: {erro}"},
            )
            return

        self.responder_json(201, {"mensagem": "Lançamento salvo."})


def main():
    endereco = ("127.0.0.1", 8000)
    servidor = HTTPServer(endereco, Aplicacao)
    print("Meu Orçamento está disponível em http://127.0.0.1:8000")
    print("Para encerrar, pressione Ctrl+C neste terminal.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
