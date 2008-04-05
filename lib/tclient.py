from twisted.spread import pb
from twisted.internet import reactor
from tserver import User, CopyUser

player_count = 0
connect = None
client = None

class Client(pb.Referenceable):
    def __init__(self, name):
        self.name = name
        self.players = []

    def connected(self, obj):
        """Connected, send information and a remote reference"""
        self.server = obj
        self.server.callRemote("join", self, self.name)
        main_loop()

    def remote_send_players(self, data):
        self.players = data

    def handle_connect_error(self, error):
        print "Error connecting: " + str(error.value)
        connect.disconnect()
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
        print '' # Flush
        player_count = cur_players

    reactor.callLater(0, main_loop)

def connect(name, host, port):
    global client

    client = Client(name)
    factory = pb.PBClientFactory()
    myd = reactor.connectTCP(host, port, factory)
    d = factory.getRootObject()
    d.addCallback(client.connected)
    d.addErrback(client.handle_connect_error)
    reactor.run()

if __name__ == '__main__':
    connect('markus', 'localhost', 10101) # TODO remove
