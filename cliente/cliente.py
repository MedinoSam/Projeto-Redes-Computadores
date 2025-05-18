import socket
import threading
import os

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 8888))
    except:
        return print('\nNão foi possível conectar ao servidor\n')

    username = input('Usuário: ')
    client.send(username.encode('utf-8'))
    print('\nConectado com sucesso!')

    thread1 = threading.Thread(target=receiveMessages, args=(client,))
    thread2 = threading.Thread(target=sendMessages, args=(client, username))

    thread1.start()
    thread2.start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if not msg:
                print('\nServidor desconectado.\n')
                break
            print(msg + '\n')
        except:
            print('\nVocê foi desconectado do servidor!\n')
            break

    #print('\nPressione <Enter> para sair\n') #nao faz sentido
    client.close()
    os._exit(0)


def sendMessages(client, username):
    while True:
        try:
            msg = input()
            if msg.lower() == '/sair':
                client.close()
                os._exit(0)
            client.send(msg.encode('utf-8'))
        except:
            break

main()