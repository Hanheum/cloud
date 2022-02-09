import socket
from threading import Thread
from os.path import exists
import getpass
from os import listdir

username = getpass.getuser()

HOST = ''
PORT = 3653

clients = []
addrs = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

def accept_client():
    while True:
        client_socket, addr = server_socket.accept()
        addrs.append(addr)
        clients.append(client_socket)
        print('connected by,', addr)
        def recv_client_signal():
            own_addr = addr
            try:
                while True:
                    data = client_socket.recv(1024)
                    if type(data.decode()) == str:
                        print(data.decode())
                        if data.decode() == 'quit':
                            addrs.remove(own_addr)
                            clients.remove(client_socket)
                            client_socket.close()
                            break
                        elif data.decode() == '/clients':
                            clients[addrs.index(own_addr)].send('{}'.format(addrs).encode())
                        elif '/dm' in data.decode():
                            divided = data.decode().split('/')
                            to_who = int(divided[2])
                            what = divided[3]
                            to_who_socket = clients[to_who]
                            to_who_socket.sendall(what.encode())
                        elif '/download/' in data.decode():
                            divided = data.decode().split('/')
                            which_file = 'C:\\Users\\{}\\Desktop\\server_folder\\'.format(username)+divided[2]
                            if not exists(which_file):
                                print('no file')
                                continue
                            data_transferred = 0
                            with open(which_file, 'rb') as f:
                                try:
                                    data = f.read(1024)
                                    while data:
                                        data_transferred += clients[addrs.index(own_addr)].send(data)
                                        data = f.read(1024)
                                except Exception as ex:
                                    print(ex)
                        elif '/upload/' in data.decode():
                            try:
                                divided = data.decode().split('/')
                                location = divided[3]
                                data_transferred = 0
                                data = clients[addrs.index(own_addr)].recv(1024)
                                with open('C:\\Users\\{}\\Desktop\\server_folder\\'.format(username) + location,
                                          'wb') as f:
                                    try:
                                        while data:
                                            f.write(data)
                                            data_transferred += len(data)
                                            data = clients[addrs.index(own_addr)].recv(1024)
                                        f.close()
                                    except Exception as ex:
                                        print(ex)
                            except:
                                pass
                        elif '/dir/' in data.decode():
                            divided = data.decode().split('/')
                            which_dir = divided[2]
                            dirs = str(listdir('C:\\Users\\{}\\Desktop\\server_folder\\'.format(username) + which_dir))
                            clients[addrs.index(own_addr)].send(dirs.encode())
            except:
                self_index = addrs.index(own_addr)
                addrs.remove(own_addr)
                clients.remove(clients[self_index])

        client_socket_thread = Thread(target=recv_client_signal)
        client_socket_thread.start()

accept_client_thread = Thread(target=accept_client)
accept_client_thread.start()