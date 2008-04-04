import net, socket

class Client(object):
    def __init__(self, username=""):
        self.username = username
        self.bad_username = False
        self.game_name = None

        self.server = None #this will be the main server eventually
        self.port = 12345
        self.my_player = None

        self.connect()

    def connect(self):
        s = self.server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((s, self.port))

        a = net.recvPacket(self.server).data
        if a == "REGECT":
            #we've been rejected -- to many users!!!
            print "too many users connected to main server - please come back later"
        else:
            a = net.request(self.server, ["USER_NAME", self.username]).data
            if a == "BAD USER NAME":
                #prompt user to pick a new username
                self.bad_username = True

    def is_my_turn(self):
        return net.request(self.server, net.Packet(["GET_WHOS_TURN", self.game_name])).data == self.my_player

    def get_who_turn(self):
        return net.request(self.server, net.Packet(["GET_WHOS_TURN", self.game_name])).data

    def update_world(self, terr1, terr2, t1_troops, t2_troops, conquer=False):
        net.request(self.server, net.Packet(["UPDATE_WORLD", self.game_name,
                                             terr1, terr2,
                                             t1_troops, t2_troop, conquer]))

    def get_messages(self):
        return net.request(self.server, net.Packet(["GET_MESSAGES", self.game_name])).data

    def send_message(self, message):
        net.request(self.server, net.Packet(["MESSAGE", self.game_name, message]))

    def start_new_game(self, gamename):
        a = net.requet(self.server, net.Packet(["NEW_GAME", gamename, self.username]))
        if a == "BAD GAME NAME":
            return "NEW NAME"

        self.game_name = gamename
        return "GOOD NAME"

    def make_map(self, mapgrid, players):
        net.request(self.server, net.Packet(["NEW_MAP", self.game_name, self.username, mapgrid, players]))
