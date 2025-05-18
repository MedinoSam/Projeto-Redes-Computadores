import socket
import threading
import sys
import os

clientsList = []
clientsNames = {}
running = True

def main():
    global running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(('localhost', 8888))
        server.listen()
        print('\nServidor iniciado com sucesso! (Digite /parar para encerrar)\n')
    except:
        return print('\nNão foi possível iniciar o servidor\n')

    threading.Thread(target=serverListenCommands, daemon=True).start()

    while running:
        try:
            server.settimeout(1.0)
            client, address = server.accept()
            clientsList.append(client)
            thread = threading.Thread(target=messagesTreatment, args=(client,))
            thread.start()
        except socket.timeout:
            continue
        except:
            break


def serverListenCommands():
    global running
    while True:
        cmd = input()
        if cmd.lower() == '/parar':
            print('\nEncerrando servidor!\n')
            running = False
            finishConections()
            break


def messagesTreatment(client):
    try:
        username = client.recv(2048).decode('utf-8')
        clientsNames[client] = username

        # Enviar mensagem para todos que o usuário entrou no chat
        entrada_msg = f'*** {username} entrou no chat. ***'
        broadcast(entrada_msg.encode('utf-8'), client)

    except:
        return

    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if not msg:
                removeClient(client)
                break

            if msg.lower() == '/lista':
                lista = ', '.join(clientsNames.values())
                client.send(f'\nUsuários conectados: {lista}\n'.encode('utf-8'))
            else:
                broadcast(f'<{username}> {msg}'.encode('utf-8'), client)

        except:
            removeClient(client)
            break


def broadcast(msg, client):
    for clientItem in clientsList:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                removeClient(clientItem)


def removeClient(client):
    if client in clientsList:
        clientsList.remove(client)

    username = clientsNames.get(client)

    if username:
        mensagemSaida = f'{username} saiu do chat.'
        broadcast(mensagemSaida.encode('utf-8'), client)

    if client in clientsNames:
        del clientsNames[client]
    try:
        client.close()
    except:
        pass


def finishConections():
    for client in clientsList:
        try:
            client.send('\nServidor encerrado.\n'.encode('utf-8'))
            client.shutdown(socket.SHUT_RDWR)
            client.close()
        except:
            print('nao deveria entrar aqui')
            pass
    clientsList.clear()
    clientsNames.clear()
    sys.exit()

main()