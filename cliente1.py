import socket

address = input("Digite o endereço do servidor: ")
port = int(input("Digite a porta do servidor: "))
nome = input("Digite seu nome de usuário: ")
address_server = (address, port)

cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente1.connect(address_server)
