from twisted.spread import pb, jelly
from twisted.internet import reactor

import random

class GameServer(pb.Root):
    def __init__(self, game_type="multi"):
        self.game_type = game_type
        self.players = []

        self._last_send_index = 0

    def remove_user(self, user):
        self.players.remove(user)
        if user.alive:
            # Check if this player currently has his turn
            # TODO replace with AI
            #print "Replaced %s with AI player" % user.name
            pass
        # Send updated player list?

    def send_to_all(self, func, *data):
        """Executes the passed function for all clients"""
        try:
            for i in self.players[self._last_send_index:]:
                d = i.client.callRemote(func, *data)
                d.addErrback(self.error)
                print "Sending to: " + i.name
        except pb.DeadReferenceError:
            print "Dropping dead reference to " + i.name
            # TODO more efficient way of finishing list?
            self._last_send_index = self.players.index(i)
            self.remove_user(i)
            self.send_to_all(func, *data)
        else:
            self._last_send_index = 0

    def remote_join(self, client, name):
        # Check for an empty slot
        # Check for a user with the same name
        for i in self.players:
            if name == i.name:
                name += str(random.randint(100, 999))
        print name, " joined the server!"
        self.players.append(CopyUser(client, name))
        # Resend the updated player list..
        self.send_to_all("send_players", self.players)

    def remote_leave(self, client):
        user = self.find_user(client)
        if user:
            self.remove_user(user)
        print user.name, "left the game"

    def remote_get_chat_msg(self, client, msg):
        user = self.find_user(client)
        print "=", user.name, msg
        self.send_to_all("send_chat_msg", user.name, msg)

    def find_user(self, remote_ref):
        for i in self.players:
            if i.client == remote_ref:
                return i

    def error(self, msg):
        print msg

class User(object):
    def __init__(self, deferred, name, color='TODO'):
        self.client = deferred
        self.name = name
        self.color = color
        self.alive = True

class CopyUser(User, pb.Copyable):
    def getStateToCopy(self):
        d = self.__dict__.copy()
        del d['client'] # Don't send deferreds to clients
        return d

from tserver import CopyUser # Can't be __main__.CopyUser for whatever reason

def listen(port=10101):
    reactor.listenTCP(port, pb.PBServerFactory(GameServer()))
    print "Waiting for players"
    reactor.run()

if __name__ == '__main__':
    listen()
