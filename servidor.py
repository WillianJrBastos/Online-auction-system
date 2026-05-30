import socket
import threading

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.live import Live

# address = input("Digite o endereço do servidor: ")
address = 'localhost'
# port = int(input("Digite a porta do servidor: "))
port = 12345
# nomeItem = input("Digite o nome do item: ")
nomeItem = "Moto"
# valorInicial = float(input("Digite o valor inicial do lance do item: R$"))
valorInicial = 10000.0
# tempo = int(input("Digite o tempo que ra durar o leilão (em segundos): "))
tempo = 30
clientes = []
vencedor = "?"
nomes = {}
leilao_ativo = False

server_address = (address, port)

lock = threading.Lock()

console = Console()

def criar_layout():
    layout = Layout()

    layout.split(
        Layout(name="cabecalho", size=3),
        Layout(name="corpo", ratio=1),
        Layout(name="clientes", size=5),
        Layout(name="rodape", size=5)
    )

    titulo = Panel(Align.center("Leilão online"), style="bold", expand=True)
    
    tabela = Table(expand=True)
    tabela.add_column("Item", justify="center")
    tabela.add_column("Lance", justify="center")
    tabela.add_column("Maior lance de", justify="center")
    tabela.add_column("Tempo", justify="center")
    tabela.add_row(nomeItem, f"R${valorInicial}", vencedor, f"{tempo}s")

    clientes = "\n".join(nomes.values()) if nomes else "Nenhum cliente conectado"
    painel_clientes = Panel(clientes,title="Clientes")
    info = Panel("Esperando lances...")

    layout["cabecalho"].update(titulo)
    layout["corpo"].update(tabela)
    layout["clientes"].update(painel_clientes)
    layout["rodape"].update(info)

    return layout

def broadcast(mensagem):
    for cliente in clientes:
        try:
            cliente.send(mensagem.encode())
        except:
            clientes.remove(cliente)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen()

layout = criar_layout()

console.print(layout)

while True:

    connection, cliente_adress = server.accept()