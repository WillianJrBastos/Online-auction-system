import socket
import threading

from rich.console import Console

address = input("Digite o endereço do servidor: ")
port = int(input("Digite a porta do servidor: "))
nome = input("Digite seu nome de usuário: ")

address_server = (address, port)
cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente2.connect(address_server)

cliente2.send(nome.encode())

console = Console()

ultimo_lance = None
leilao_encerrado = False
confirmando = False


def receber():
    global leilao_encerrado

    while True:
        try:
            mensagem = cliente2.recv(1024).decode()

            if not mensagem:
                break

            if mensagem == "LEILAO_ENCERRADO":
                console.print("\n[red]Leilão encerrado! Não é mais possível enviar lances.[/red]")
                leilao_encerrado = True
                break

            if not confirmando:
                console.print(f"\n\n[green][Servidor][/green] {mensagem}")
                print("Digite seu lance: ", end="", flush=True)

        except:
            break


threading.Thread(target=receber, daemon=True).start()

while True:
    try:
        if leilao_encerrado:
            break

        lance = input("")

        if lance.lower() == "sair":
            break

        confirmando = True

        confirmar = input(f"Confirmar envio do lance R$ {lance}? (s/n): ")

        confirmando = False

        if confirmar.lower() == "s":
            cliente2.send(lance.encode())

            ultimo_lance = lance

            console.print(f"[blue]Seu último lance foi: R$ {ultimo_lance}[/blue]")

        elif confirmar.lower() == "n":
            console.print("[yellow]Lance cancelado.[/yellow]")
            print("\nDigite seu lance: ", end="", flush=True)

        else:
            console.print("[red]Digite apenas s ou n[/red]")

    except:
        break

cliente2.close()