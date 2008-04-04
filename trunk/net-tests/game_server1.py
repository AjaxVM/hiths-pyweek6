import net
import random

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

class my_handler(net.DefaultHandler):
    def __init__(self):
        net.DefaultHandler.__init__(self)
        self.users={}
        self.messages=[]
        self.handles={"USER_JOIN":self.handleUSER_JOIN,
                      "MESSAGE":self.handleMESSAGE,
                      "GET_MESSAGES":self.handleGET_MESSAGES,
                      "END_TURN":self.handleEND_TURN,
                      "NEW_GAME":self.handleNEW_GAME,
                      "GET_MAP":self.handleGET_MAP,
                      "UPDATE_WORLD":self.handleUPDATE_WORLD,
                      "GET_WHOS_TURN":self.handleGET_WHOS_TURN,
                      "START_GAME":self.handleSTART_GAME,
                      "GET_NUM_PLAYERS":self.handleGET_NUM_PLAYERS,
                      "JOIN_GAME":self.handleJOIN_GAME,
                      "GET_USER_NUMBER":self.handleGET_USER_NUMBER,
                      "CHANGE_NUM_PLAYERS":self.handleCHANGE_NUM_PLAYERS,
                      "GET_PLAYERS":self.handleGET_PLAYERS,
                      "LOST_USER":self.handleLOST_USER,
                      "IGNORE_USER":self.handleIGNORE,
                      "GET_GAMES":self.handleGET_GAMES}

        self.games = {}

    def handleUSER_JOIN(self, data):
        if data[0] in self.users:
            return net.Packet("BAD USER NAME")
        self.users[data[0]] = User(data[0], data[1])
        return net.Packet("")

    def handleMESSAGE(self, data):
        game = data[0]
        del data[0]
        if game == "lobby":
            for i in self.users:
                i = self.users[i]
                if not i.ingame or data[0] in i.ignore:
                    i.messages.append(["MESSAGE", data])
        elif game == "!SERVER->everyone!@@":
            for i in self.users:
                self.users[i].messages.append(data)
        else:
            for i in self.games[game].users:
                i = self.games[game].users[i]
                if not data[0] in i.ignore:
                    i.messages.append(["MESSAGE", data])
        return net.Packet("")

    def handleGET_MESSAGES(self, data):
        game = data[0]
        del data[0]
        if game == "lobby":
            sending = self.users[data[0]].messages
        else:
            sending = self.games[game].users[data[0]].messages
        self.users[data[0]].messages=[]
        return net.Packet(sending)
        pass

    def handleEND_TURN(self, data):
        game = data[0]
        user = data[1]
        val = self.games[game].get_player_num(user)
        if self.games[game].whos_turn == val:
            self.games[game].whos_turn += 1
        return net.Packet("")

    def handleNEW_GAME(self, data):
        #create new game!
        game = data[0]
        user = data[1]
        players = data[2]
        if game in self.games:
            return net.Packet("BAD GAME NAME")
        self.games[game] = Game(game, self.users[user], players)
        return net.Packet("")

    def handleGET_MAP(self, data):
        game = data[0]
        user = data[1]
        game = self.games[game]
        return net.Packet([game.mapdata, game.players])

    def handleUPDATE_WORLD(self, data):
        game = data[0]
        user = data[1]
        terr1 = data[2]
        terr2 = data[3]
        t1_troops = data[4]
        t2_troops = data[5]
        conquer = data[6]
        for i in self.games[game].users:
            i = self.games[game].users[i]
            i.messages.append(["UPDATE_WORLD", terr1, terr2, t1_troops, t2_troops, conquer])
        return net.Packet("")

    def handleGET_WHOS_TURN(self, data):
        game = data[0]
        return net.Packet(self.games[game].whos_turn)

    def handleSTART_GAME(self, data):
        game = data[0]
        user = data[1]
        for i in self.games[game].users:
            i = self.games[game].users[i]
            i.messages.append(["START_GAME"])
        return net.Packet("")

    def handleGET_NUM_PLAYERS(self, data):
        game = data[0]
        return net.Packet(len(self.games[game].users))

    def handleJOIN_GAME(self, data):
        game = data[0]
        user = data[1]
        self.games[game].users[user.name] = user
        return net.Packet("")

    def handleGET_USER_NUMBER(self, data):
        game = data[0]
        user = data[1]
        return net.Packet(self.games[game].get_player_num(user))

    def handleCHANGE_NUM_PLAYERS(self, data):
        #also remake games mapdata
        game = data[0]
        user = data[1]
        num = data[2]
        self.games[game].num_players = num
        self.games[game].make_map()
        return net.Packet("")

    def handleGET_PLAYERS(self, data):
        game = data[0]
        return net.Packet(list(self.games[game].users))

    def handleLOST_USER(self, data):
        user = ""
        for i in self.users:
            if self.users[i].sockobj == data[0]:
                self.handleMESSAGE(["!SERVER->everyone!", "LOST_USER", self.users[i]])
                del self.users[i]
        for i in self.games:
            i = self.games[i]
            for x in i.users:
                if i.users[x].sockobj == data[0]:
                    i.replace_user_with_ai(x)
        return net.Packet("")

    def handleIGNORE(self, data):
        user = data[0]
        ig = data[1]
        self.users[user].ignore.append(ig)
        return net.Packet("")

    def handleGET_GAMES(self, data):
        return net.Packet(self.games)

a = net.Server("",12345, handler=my_handler)
a.connect()
a.serve()
