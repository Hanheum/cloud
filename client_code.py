import socket
from threading import Thread
import getpass
from time import sleep
from sys import stdout

username = getpass.getuser()

HOST = open('C:\\Users\\{}\\Desktop\\ip.txt'.format(username), 'r').read()
PORT = 3653

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

def listener():
    while True:
        data = client_socket.recv(1024)
        data_transferred = 0
        try:
            print(data.decode())
        except:
            with open('C:\\Users\\{}\\Desktop\\'.format(username)+'recv', 'wb') as f:
                try:
                    while data:
                        f.write(data)
                        data_transferred += len(data)
                        data = client_socket.recv(1024)
                        stdout.write('\r')
                        stdout.write('file transfer:{}'.format(data_transferred))
                    f.close()
                except Exception as ex:
                    print(ex)

def speaker():
    while True:
        txt = input('message:')
        client_socket.sendall(txt.encode())
        if txt == 'quit':
            sleep(1)
            client_socket.close()
            break
        if '/upload' in txt:
            divided = txt.split('/')
            to_send = divided[2]
            data_transferred = 0
            with open(to_send, 'rb') as f:
                try:
                    data = f.read(1024)
                    while data:
                        data_transferred += client_socket.send(data)
                        data = f.read(1024)
                        stdout.write('\r')
                        stdout.write('file sending:{}'.format(data_transferred))
                except Exception as ex:
                    print(ex)

listener_thread = Thread(target=listener)
speaker_thread = Thread(target=speaker)
listener_thread.start()
speaker_thread.start()