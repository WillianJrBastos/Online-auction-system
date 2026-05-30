import time
import threading

tempo = 5
lance = 10000.0
valorInicial = 1000.0

#if lance > valorInicial:
#    print("Lance aceito!")
#
#   while tempo > 0:
#       print(f"Tempo: {tempo}s", end="\r")
#       time.sleep(1)
#       tempo -= 1
#
#    print("Tempo esgotado! Fim do leilão.")*/

#def cronometro(tempo):
#
#   while tempo > 0:
#        print(f"Tempo: {tempo}s", end="\r")
#        time.sleep(1)
#
#    print("Tempo esgotado! Fim do leilão.")
#
#thead = threading.Thread(target=cronometro, args=(tempo,))
#thead.start()
#
#print("\nTeste")

def leilao(connection, cliente):
    global lance, valorInicial

    cliente = connection.recv(1024).decode()
    print(f"Cliente {cliente} entrou no leilão.")

    while True:
        try:
            lance = float(connection.recv(1024).decode())
            if lance > valorInicial:
                valorInicial = lance
                print(f"Novo lance: R${lance:.2f} por {cliente}")
            else:
                connection.send("Lance rejeitado. O valor deve ser maior que o lance atual.".encode())
        except:
            print(f"Cliente {cliente} desconectado.")
            break