import unittest
import test_support

import socket
import os
import time

PORT = 50007
HOST = 'localhost'

class SocketTest(unittest.TestCase):

    def setUp(self):
        canfork = hasattr (os, 'fork')
        if not canfork:
            raise test_support.TestSkipped, \
                  "Platform does not support forking."

        # Use this to figure out who we are in the tests
        self.parent = os.fork()

        if self.parent:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((HOST, PORT))
            self.s.listen(1)
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1) # So we can catch up

    def tearDown(self):
        self.s.close ()
        self.s = None

class SocketConnectedTest(SocketTest):

    SYNCH_MSG = 'Michael Gilfix was here'

    def setUp(self):
        SocketTest.setUp(self)
        if self.parent:
            conn, addr = self.s.accept()
            self.conn = conn
        else:
            self.s.connect((HOST, PORT))
            self.conn = self.s

    def tearDown(self):
        if self.parent:
            self.conn.close()
        self.conn = None
        SocketTest.tearDown(self)

    def synchronize(self):
        time.sleep(1)
        if self.parent:
            msg = self.conn.recv(len(self.SYNCH_MSG))
            self.assertEqual(msg, self.SYNCH_MSG, "Parent synchronization error")
            self.conn.send(msg)
        else:
            self.conn.send(msg)
            msg = self.conn.recv(len(self.SYNCH_MSG))
            self.assertEqual(msg, self.SYNCH_MSG, "Child synchronization error")
        time.sleep(1)

class FileObjectClassTestCase(SocketConnectedTest):

    def setUp(self):
        SocketConnectedTest.setUp(self)
        # Create a file object for both the parent/client processes
        self.f = socket._fileobject(self.conn, 'rb', 8192)

    def tearDown(self):
        self.f.close()
        SocketConnectedTest.tearDown(self)

    def testSmallRead(self):
        """Performing small read test."""
        if self.parent:
            first_seg = self.f.read(7)
            second_seg = self.f.read(25)
            msg = ''.join((first_seg, second_seg))
            self.assertEqual(msg, self.SYNCH_MSG, "Error performing small read.")
        else:
            self.f.write(self.SYNCH_MSG)
            self.f.flush()

    def testUnbufferedRead(self):
        """Performing unbuffered read test."""
        if self.parent:
            buf = ''
            while 1:
                char = self.f.read(1)
                self.failIf(not char, "Error performing unbuffered read.")
                buf += char
                if buf == self.SYNCH_MSG:
                    break
        else:
            self.f.write(self.SYNCH_MSG)
            self.f.flush()

    def testReadline(self):
        """Performing readline test."""
        if self.parent:
            line = self.f.readline()
            self.assertEqual(line, self.SYNCH_MSG, "Error performing readline.")
        else:
            self.f.write(self.SYNCH_MSG)
            self.f.flush()

def suite():
    suite = unitest.TestSuite()
    suite.addTest(unittest.makeSuite(FileObjectClassTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
