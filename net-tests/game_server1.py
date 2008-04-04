import net

class Game(object):
    def __init__(self):
        self.name = ""
        self.whos_turn = 0

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
                      "NEW_MAP":self.handleNEW_MAP,
                      "UPDATE_WORLD":self.handleUPDATE_WORLD,
                      "MAKE_PLAYERS":self.handleMAKE_PLAYERS,
                      "GET_WHOS_TURN":self.handleGET_WHOS_TURN}

        self.games = {}

    def handleUSER_JOIN(self, data):
##        self.users[data[0]]={}
##        self.users[data[0]]["messages"]=[]
##        return net.Packet("")
        pass

    def handleMESSAGE(self, data):
##        if "STOP_SERVER" in data[1]:
##            return data[1]
##        for i in self.users:
##            self.users[i]['messages'].append([data[0],data[1]])
##        return net.Packet("")
        pass

    def handleGET_MESSAGES(self, data):
##        sending = list(self.users[data[0]]['messages'])
##        self.users[data[0]]['messages']=[]
##        return net.Packet(sending)
        pass

    def handleEND_TURN(self, data):
        pass

    def handleNEW_GAME(self, data):
        pass

    def handleNEW_MAP(self, data):
        pass

    def handleUPDATE_WORLD(self, data):
        pass

    def handleMAKE_PLAYERS(self, data):
        pass

    def handleGET_WHOS_TURN(self, data):
        pass

a = net.Server("",12345, handler=my_handler)
a.connect()
a.serve()
