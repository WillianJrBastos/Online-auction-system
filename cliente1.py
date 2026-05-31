import socket
import threading

from rich.console import Console

# address = input("Digite o endereço do servidor: ")
address = 'localhost'
# port = int(input("Digite a porta do servidor: "))
port = 12345
# nome = input("Digite seu nome de usuário: ")
nome = "Will"
address_server = (address, port)

cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente1.connect(address_server)

cliente1.send(nome.encode())

console = Console()

def receber():
    while True:
        try:
            mensagem = cliente1.recv(1024).decode()

            if not mensagem:
                break

            console.print(f"\n[green][Servidor][/green] {mensagem}")
            print("Digite seu lance: ", end="", flush=True)

        except:
            break

threading.Thread(target=receber, daemon=True).start()

while True:
    try:
        lance = input("")

        if lance.lower() == "sair":
            break

        cliente1.send(lance.encode())

    except:
        break

cliente1.close()