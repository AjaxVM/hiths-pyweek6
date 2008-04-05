from twisted.spread import pb
from twisted.internet import reactor
from tserver import User, CopyUser

import sys, signal

player_count = 0
loop = 0
client = None
game_creator = False

class Client(pb.Referenceable):
    def __init__(self, name):
        self.name = name
        self.players = []

    def connected(self, remote_ref):
        """Connected, send information and a remote reference"""
        self.server = remote_ref
        self.server.callRemote("join", self, self.name)
        # TODO: game creator starts game here
        if game_creator:
            # generate map
            self.server.callRemote("start_game", self, map)
        main_loop()

    def remote_send_players(self, data):
        self.players = data

    def remote_send_chat_msg(self, msg):
        print msg

    def remote_server_disconnect(self, msg):
        """Server forced disconnect"""
        print "Disconnected:", msg
        # Go back to menu
        reactor.callLater(0, reactor.stop)

    def handle_connect_error(self, error):
        print error.value # TODO dialog for this
        # callLater workaround for regression in twisted 8.0.1
        reactor.callLater(0, reactor.stop())

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
        print ''
        sys.stdout.flush()
        player_count = cur_players

    #msg = input("Chat: ")
    if loop == 0:
        msg = 'Hello!'
        client.server.callRemote("get_chat_msg", client, msg)

    loop += 1
    reactor.callLater(0, main_loop)

def handle_signal(signal, frame):
    def disconnect(ref=None):
        reactor.callLater(0, reactor.stop)

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
    reactor.connectTCP(host, port, factory)
    d = factory.getRootObject()
    d.addCallback(client.connected)
    d.addErrback(client.handle_connect_error)
    reactor.run()

signal.signal(signal.SIGINT, handle_signal)

if __name__ == '__main__':
    connect('markus', 'localhost', 10101) # TODO remove
