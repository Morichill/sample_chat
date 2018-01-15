import pytest

import server

import client





def simple_func(value):

 #отлавливаем ошибки с помощью Assert

    assert type(value) == int   

    assert value > 0



    return value*value		

def test_server_starts_tcp_server(self):

    # Start server 

    srv = server.server('127.0.0.1', 7777)

    server_thread = threading.Thread(target=srv.start_listening)

    server_thread.start()



  # test for old version chat

    time.sleep(0.000001)  



    # This is our fake test client that is just going to attempt a connect and disconnect

    fake_client = socket.socket()

    fake_client.settimeout(1)

    fake_client.connect(('127.0.0.1', 7777))

    fake_client.close()



    # Make sure server thread finishes

    server_thread.join()



def run_fake_server(self):

    # Run a server to listen for a connection and then close it

    server_sock = socket.socket()

    server_sock.bind(('127.0.0.1', 7777))

    server_sock.listen(0)

    server_sock.accept()

    server_sock.close()



def test_client_connects_and_disconnects_to_default_server(self):

    # Start fake server 

    server_thread = threading.Thread(target=self.run_fake_server)

    server_thread.start()



    # Test the clients basic connection and disconnection

    client = client.client()

    client.connect('127.0.0.1', 7777)

    client.disconnect()



    # Ensure server thread ends

    server_thread.join()
