import net

class my_handler(net.DefaultHandler):
    def __init__(self):
        net.DefaultHandler.__init__(self)
        self.users={}
        self.messages=[]
        self.handles={"USER_JOIN":self.handleUSER_JOIN,
                      "MESSAGE":self.handleMESSAGE,
                      "GET_MESSAGES":self.handleGET_MESSAGES}

    def handleUSER_JOIN(self, data):
        self.users[data[0]]={}
        self.users[data[0]]["messages"]=[]
        return net.Packet("")

    def handleMESSAGE(self, data):
        if "STOP_SERVER" in data[1]:
            return data[1]
        for i in self.users:
            self.users[i]['messages'].append([data[0],data[1]])
        return net.Packet("")

    def handleGET_MESSAGES(self, data):
        sending = list(self.users[data[0]]['messages'])
        self.users[data[0]]['messages']=[]
        return net.Packet(sending)
            

a = net.Server("",12345, handler=my_handler)
a.connect()
a.serve()
