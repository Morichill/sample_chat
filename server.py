  
import select
import socket
import sys
import signal
import pickle
import struct
import argparse

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'


class ChatServer(object):
    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = [] # прослушиваем сокеты вывода
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print ('Server listening to port: %s ...' %port)
        self.server.listen(backlog)
        # Перехватываем прерывания клавиатуры
        signal.signal(signal.SIGINT, self.sighandler)
    
    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        # Закрываем данный сервер
        print ('Shutting down server...')
        # Закрываем имеющиеся сокеты клиента
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))
			
   def run(self):
       inputs = [self.server, sys.stdin]
       self.outputs = []

       running = True
       while running:
           try:
           readable, writeable, exceptional = select.select(inputs, self.outputs, [])
       except select.error as e:
           break

       for sock in readable:
           if sock == self.server:
               # обрабатываем сокет данного сервера
               client, address = self.server.accept()
               print ("Chat server: got connection %d from %s" %(client.fileno(), address))
               # Считываем имя регистрации
               cname = receive(client).split('NAME: ')[1]
               # Вычислем имя клиента и отправляем обратно
               self.clients += 1
               send(client, 'CLIENT: ' + str(address[0]))
               inputs.append(client)
               self.clientmap[client] = (address, cname)
               # Отправляем присоединённую информацию прочим клиентам
               msg = "\n(Connected: New client (%d) from %s)" %(self.clients, self.get_client_name(client))
               for output in self.outputs:
                   send(output, msg)
               self.outputs.append(client)

           elif sock == sys.stdin:
               # обрабатываем стандартный ввод
               junk = sys.stdin.readline()
               running = False
           else:
               # обрабатываем все прочие сокеты
               try:
                   data = receive(sock)
                   if data:
                       # Отправляем как новое сообшение клиента...
                       msg = '\n#[' + self.get_client_name(sock)
                                    + ']>>' + data
                       # Отправляем данные всем за исключением себя
                       for output in self.outputs:
                           if output != sock:
                               send(output, msg)
                           else:
                               print ("Chat server: %d hung up" % sock.fileno())
                               self.clients -= 1
                               sock.close()
                               inputs.remove(sock)
                               self.outputs.remove(sock)

                               # Отправляем оставленную клиентом иформацию остальным
                               msg = "\n(Now hung up: Client from %s)" %self.get_client_name(sock)
                               for output in self.outputs:
                                   send(output, msg)
               except socket.error as e:
                   # Удаляем
                   inputs.remove(sock)
                   self.outputs.remove(sock)
   self.server.close()			
	
