import socket
import threading
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.live import Live

address = input("Digite o endereço do servidor: ")
port = int(input("Digite a porta do servidor: "))
nomeItem = input("Digite o nome do item: ")
valorInicial = float(input("Digite o valor inicial do lance do item: R$"))
tempo = int(input("Digite o tempo que ra durar o leilão (em segundos): "))
tempoRestante = tempo
clientes = []
vencedor = "?"
nomes = {}
leilaoAtivo = False

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

    titulo = Panel(Align.center("LEILÃO ONLINE"),expand=True)
    
    tabela = Table(expand=True)
    tabela.add_column("Item", justify="center")
    tabela.add_column("Lance", justify="center")
    tabela.add_column("Maior lance de", justify="center")
    tabela.add_column("Tempo", justify="center")
    
    tabela.add_row(
        nomeItem, 
        f"R${valorInicial}", 
        vencedor, 
        f"{tempoRestante}s"
    )

    listaClientes = "\n".join(nomes.values())

    painelClientes = Panel(listaClientes if listaClientes else "Nenhum cliente conectado", title="Clientes")

    info = Panel(f"Clientes conectados: {len(clientes)}")

    layout["cabecalho"].update(titulo)
    layout["corpo"].update(tabela)
    layout["clientes"].update(painelClientes)
    layout["rodape"].update(info)

    return layout

def broadcast(mensagem):
    for cliente in clientes:
        try:
            cliente.send(mensagem.encode())
        except:
            if cliente in clientes:
                clientes.remove(cliente)

def cronometro():
    global tempoRestante, leilaoAtivo

    while tempoRestante > 0:
        time.sleep(1)
        tempoRestante -= 1

        if tempoRestante % 15 == 0 and tempoRestante > 0:
            broadcast(f"Restam {tempoRestante} segundos.")
        if tempoRestante in [3, 2, 1]:
            broadcast(f"Leilão termina em {tempoRestante} segundo(s)!")

    leilaoAtivo = False

    mensagem = (f"\n\nLeilão encerrado!\n"f"Vencedor: {vencedor}\n"f"Valor final: R${valorInicial:.2f}\n")

    broadcast(mensagem)
    broadcast("LEILÃO ENCERRADO")

    console.print(Panel(mensagem, title="Finalizado!"))

def fazerLance(connection, endereco):
    global valorInicial
    global vencedor
    global leilaoAtivo

    try:

        nome = connection.recv(1024).decode()

        with lock:
            nomes[connection] = nome
            clientes.append(connection)

        console.print(f"'{nome}' conectado")

        connection.send(
            (f"Bem-vindo ao leilão, {nome}!\n"f"Item: {nomeItem} | "f"Lance atual: R${valorInicial:.2f}").encode())

        while True:

            dados = connection.recv(1024).decode()

            if not dados:
                break

            with lock:
                if tempoRestante <= 0:
                    connection.send("LEILAO_ENCERRADO".encode())
                    break

            lance = float(dados)

            with lock:
                if lance > valorInicial:
                    valorInicial = lance
                    vencedor = nome

                    mensagem = (f"Novo lance: "f"R${valorInicial:.2f} "f"por {vencedor}")

                    console.print(Panel(mensagem, title="Novo Lance!"))

                    broadcast(mensagem)

                    if not leilaoAtivo:
                        leilaoAtivo = True

                        threading.Thread(target=cronometro, daemon=True).start()

                else:
                    connection.send(
                        "Lance rejeitado!".encode())

    except:
        console.print(f"[red]'{nome}' desconectado.[/red]")

    finally:

        with lock:

            if connection in clientes:
                clientes.remove(connection)
            if connection in nomes:
                del nomes[connection]

        connection.close()

def atualizarLayout():
    with Live(criar_layout(), refresh_per_second=4, screen=True) as live:

        while True:
            live.update(criar_layout())
            time.sleep(0.5)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen()

console.print(Panel(f"Servidor iniciado em {address}:{port}",title="Servidor"))

threading.Thread(target=atualizarLayout,daemon=True).start()

while True:

    connection, endereco = server.accept()

    threading.Thread(target=fazerLance,args=(connection, endereco),daemon=True).start()