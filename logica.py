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

def cronometro(tempo):

    while tempo > 0:
        print(f"Tempo: {tempo}s", end="\r")
        time.sleep(1)
        tempo -= 1

    print("Tempo esgotado! Fim do leilão.")

thead = threading.Thread(target=cronometro, args=(tempo,))
thead.start()

print("\nTeste")
