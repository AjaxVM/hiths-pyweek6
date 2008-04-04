import net, socket

class Game(object):
    def __init__(self, name, start_player, num_players):
        self.name = name
        self.whos_turn = 0

        self.num_players = num_players
        self.make_user_numbers()

        self.users = {start_player.name:start_player}

        self.make_map()

    def make_user_numbers(self):
        self.player_nums = range(self.num_players)
        random.shuffle(self.player_nums)

    def replace_user_with_ai(self, user):
        del self.users[user] #should really be changed to AI!!!!

    def get_player_num(self, user):
        cur = 0
        for i in self.users:
            if self.users[i] == user:
                return cur
            cur += 1
        return None

    def make_map(self):
        self.mapdata = None#this should be generated like main.py currently does
        self.players = None#as should this

class User(object):
    def __init__(self, name, sockobj):
        self.name = name
        self.sockobj = sockobj

        self.messages = []
        self.ingame = False
        self.ignore = []

class Client(object):
    def __init__(self, username=""):
        self.username = username
        self.bad_username = False
        self.gamename = "lobby"

        self.server = "localhost" #this will be the main server eventually
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
        a = net.request(self.server, net.Packet(["USER_JOIN", self.username, str(self.server.getsockname())])).data
        if a == "BAD USER NAME":
            #prompt user to pick a new username
            self.bad_username = True

    def is_my_turn(self):
        return net.request(self.server, net.Packet(["GET_WHOS_TURN",
                                                    self.gamename,
                                                    self.username])).data == self.my_player

    def get_whos_turn(self):
        return net.request(self.server, net.Packet(["GET_WHOS_TURN",
                                                    self.gamename,
                                                    self.username])).data

    def update_world(self, terr1, terr2, t1_troops, t2_troops, conquer=False):
        net.request(self.server, net.Packet(["UPDATE_WORLD", self.gamename,
                                             self.username,
                                             terr1, terr2,
                                             t1_troops, t2_troops, conquer]))

    def get_messages(self):
        return net.request(self.server, net.Packet(["GET_MESSAGES", self.gamename, self.username])).data

    def send_message(self, message):
        net.request(self.server, net.Packet(["MESSAGE", self.gamename, self.username, message]))

    def start_new_game(self, gamename, num_players):
        a = net.request(self.server, net.Packet(["NEW_GAME", gamename, self.username, num_players]))
        if a == "BAD GAME NAME":
            return False

        self.gamename = gamename
        return True

    def end_turn(self):
        net.request(self.server, net.Packet(["END_TURN", self.gamename, self.username]))

    def get_num_players(self):
        return net.request(self.server, net.Packet(["GET_NUM_PLAYERS", self.gamename, self.username])).data

    def get_players(self):
        return net.request(self.server, net.Packet(["GET_PLAYERS", self.gamename, self.username])).data

    def join_game(self, gamename): #join a pre-existing game
        a = net.request(self.server, net.Packet(["JOIN_GAME", gamename, self.username])).data
        if a == "REJECT":
            return False
        self.gamename = gamename
        return True

    def get_player_number(self):
        a = net.request(self.server, net.Packet(["GET_USER_NUMBER", self.gamename, self.username])).data
        self.my_player = a
        return a

    def begin_game(self):
        a = net.request(self.server, net.Packet(["START_GAME", self.gamename, self.username])).data
        if a == "BAD_GAME":
            return False
        return True

    def get_map(self):
        return net.request(self.server, net.Packet(["GET_MAP", self.gamename, self.username])).data

    def change_num_players(self, num):
        net.request(self.server, net.Packet(["CHANGE_NUM_PLAYERS", self.gamename, self.username, num]))

    def get_games(self):
        if self.gamename=="lobby":
            return net.request(self.server, net.Packet(["GET_GAMES", 0])).data
        return self.gamename

    def add_ai_player(self):
        net.request(self.server, net.Packet(["ADD_AI", self.gamename, self.username]))
