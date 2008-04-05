from twisted.spread import pb
from twisted.internet import reactor
from tserver import User, CopyUser

import sys, signal

player_count = 0
loop = 0
connection = None
client = None

class Client(pb.Referenceable):
    def __init__(self, name):
        self.name = name
        self.players = []

    def connected(self, remote_ref):
        """Connected, send information and a remote reference"""
        self.server = remote_ref
        self.server.callRemote("join", self, self.name)
        main_loop()

    def remote_send_players(self, data):
        self.players = data

    def remote_send_chat_msg(self, name, msg):
        print name, "said:", msg

    def handle_connect_error(self, error):
        print "Error connecting: " + str(error.value)
        #connection.disconnect()
        reactor.stop()

class RemoteUser(User, pb.RemoteCopy):
    pass

pb.setUnjellyableForClass(CopyUser, RemoteUser)

def main_loop():
    global player_count, loop

    cur_players = len(client.players)
    if cur_players > player_count:
        print "Got new player data:", cur_players, "players"
        print "Names ",
        for i in client.players:
            print i.name,
        sys.stdout.flush()
        #print '' # Flush
        player_count = cur_players

    #msg = input("Chat: ")
    if loop == 0:
        msg = 'Hello!'
        client.server.callRemote("get_chat_msg", client, msg)

    loop += 1
    reactor.callLater(0, main_loop)

def handle_signal(signal, frame):
    def disconnect(ref=None):
        reactor.stop()

    # We haven't made a connection yet
    if not 'server' in client.__dict__:
        disconnect()

    try:
        d = client.server.callRemote("leave", client)
        d.addCallback(disconnect)
    except pb.DeadReferenceError:
        disconnect()

def connect(name, host, port):
    global client

    client = Client(name)
    factory = pb.PBClientFactory()
    connection = reactor.connectTCP(host, port, factory)
    d = factory.getRootObject()
    d.addCallback(client.connected)
    d.addErrback(client.handle_connect_error)
    reactor.run()

signal.signal(signal.SIGINT, handle_signal)

if __name__ == '__main__':
    connect('markus', 'localhost', 10101) # TODO remove