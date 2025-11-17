#!/usr/bin/env python3
"""
Servidor HTTP simples para hospedar a interface web do INDE MCP

Uso:
    python3 server.py [porta]

Exemplo:
    python3 server.py 8080
"""

import http.server
import socketserver
import sys
import os
from pathlib import Path

# Configurações
DEFAULT_PORT = 8000
INTERFACE_DIR = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler customizado para servir arquivos da interface"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(INTERFACE_DIR), **kwargs)

    def end_headers(self):
        # Adicionar headers CORS para permitir chamadas da interface
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Log customizado mais legível
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    # Determinar porta
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Porta inválida '{sys.argv[1]}'. Usando porta padrão {DEFAULT_PORT}")
            port = DEFAULT_PORT

    # Mudar para o diretório da interface
    os.chdir(INTERFACE_DIR)

    # Configurar servidor
    Handler = CustomHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("=" * 70)
            print("🌐 INDE MCP - Servidor de Interface Web")
            print("=" * 70)
            print(f"\n✅ Servidor rodando em: http://localhost:{port}")
            print(f"📁 Diretório: {INTERFACE_DIR}")
            print(f"\n📖 Para acessar a interface:")
            print(f"   Abra seu navegador e acesse: http://localhost:{port}")
            print(f"\n⚠️  Para parar o servidor, pressione Ctrl+C")
            print("=" * 70)
            print()

            # Iniciar servidor
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado pelo usuário")
        sys.exit(0)

    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\n❌ Erro: A porta {port} já está em uso.")
            print(f"   Tente usar outra porta: python3 server.py {port + 1}")
        else:
            print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
