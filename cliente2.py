import socket
import threading

from rich.console import Console

# address = input("Digite o endereço do servidor: ")
address = 'localhost'
# port = int(input("Digite a porta do servidor: "))
port = 12345
# nome = input("Digite seu nome de usuário: ")
nome = "Will 2"
address_server = (address, port)

cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente2.connect(address_server)

cliente2.send(nome.encode())

console = Console()

def receber():
    while True:
        try:
            mensagem = cliente2.recv(1024).decode()

            if not mensagem:
                break

            if mensagem == "LEILAO_ENCERRADO":
                console.print(
                    "\n[bold red]Leilão encerrado! Não é mais possível enviar lances.[/bold red]"
                )
                cliente2.close()
                break

            console.print(
                f"\n[green][Servidor][/green] {mensagem}"
            )

            print("Digite seu lance: ", end="", flush=True)

        except:
            break

threading.Thread(target=receber, daemon=True).start()

while True:
    try:
        lance = input("")

        if lance.lower() == "sair":
            break

        cliente2.send(lance.encode())

    except:
        break

cliente2.close()