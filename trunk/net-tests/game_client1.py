import net, socket

class Client(object):
    def __init__(self, username=""):
        self.username = username
        self.bad_username = False
        self.game_name = "lobby"

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
            raise SystemExit()
        else:
            a = net.request(self.server, ["USER_JOIN", self.username, self.server]).data
            if a == "BAD USER NAME":
                #prompt user to pick a new username
                self.bad_username = True

    def is_my_turn(self):
        return net.request(self.server, net.Packet(["GET_WHOS_TURN",
                                                    self.game_name,
                                                    self.username])).data == self.my_player

    def get_who_turn(self):
        return net.request(self.server, net.Packet(["GET_WHOS_TURN",
                                                    self.game_name,
                                                    self.username])).data

    def update_world(self, terr1, terr2, t1_troops, t2_troops, conquer=False):
        net.request(self.server, net.Packet(["UPDATE_WORLD", self.game_name,
                                             self.username,
                                             terr1, terr2,
                                             t1_troops, t2_troop, conquer]))

    def get_messages(self):
        return net.request(self.server, net.Packet(["GET_MESSAGES", self.username])).data

    def send_message(self, message):
        net.request(self.server, net.Packet(["MESSAGE", self.game_name, self.username, message]))

    def start_new_game(self, gamename, num_players):
        a = net.requet(self.server, net.Packet(["NEW_GAME", gamename, self.username, num_players]))
        if a == "BAD GAME NAME":
            return False

        self.game_name = gamename
        return True

    def end_turn(self):
        net.request(self.server, net.Packet(["END_TURN", self.gamename, self.username])

    def get_num_players(self):
        return net.request(self.server, net.Packet(["GET_NUM_PLAYERS", self.gamename, self.username])).data

    def get_players(self):
        return net.request(self.server, net.Packet(["GET_PLAYERS", self.gamename, self.username])).data

    def join_game(self, gamename): #join a pre-existing game
        a = net.request(self.server, net.Packet(["JOIN_GAME", gamename, self.username])).data
        if a == "REJECT":
            return False
        return True

    def get_player_number(self):
        return net.request(self.server, net.Packet["GET_USER_NUMBER", self.gamename, self.username])).data

    def begin_game(self):
        a = net.request(self.server, net.Packet(["START_GAME", gamename, self.username])).data
        if a == "BAD_GAME":
            return False
        return True

    def make_map(self, mapgrid, players):
        net.request(self.server, net.Packet(["NEW_MAP", self.game_name, self.username, mapgrid, players]))

    def change_num_players(self, num):
        net.request(self.server, net.Packet(["CHANGE_NUM_PLAYERS", self.gamename, self.username, num]))
