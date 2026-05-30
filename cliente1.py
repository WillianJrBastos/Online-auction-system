import socket

# address = input("Digite o endereço do servidor: ")
address = 'localhost'
# port = int(input("Digite a porta do servidor: "))
port = 12345
# nome = input("Digite seu nome de usuário: ")
nome = "Will"
address_server = (address, port)

cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente1.connect(address_server)