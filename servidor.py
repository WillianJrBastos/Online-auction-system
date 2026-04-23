import socket
import threading

address = input("Digite o endereço do servidor: ")
port = int(input("Digite a porta do servidor: "))
nomeItem = input("Digite o nome do item: ")
valorInicial = float(input("Digite o valor inicial do lance do item: R$"))
tempo = int(input("Digite o tempo que ra durar o leilão (em segundos): "))
clientes = []
server_address = (address, port)

def broadcast(mensagem):
    for cliente in clientes:
        try:
            cliente.send(mensagem.encode())
        except:
            clientes.remove(cliente)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen()
print(f"Esperando clientes entrarem no servidor... \n{address}:{port}")

while True:

    connection, cliente_adress = server.accept()
