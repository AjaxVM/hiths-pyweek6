import socket, select, pickle

def gethostname():
    return socket.gethostname()

def recvPacket(sock):
    d = ""
    while 1:
        try:d = d + sock.recv(1024)
        except:
            return "BAD_SOCK"
        if d[len(d)-3:len(d)]=="END":
            break
    d=Packet(d[0:len(d)-3], False)
    d.read()
    return d

def sendPacket(sock, data):
    try:sock.send(data.data+"END")
    except:
        return "BAD_SOCK"
    return None

def request(sock, data):
    if sendPacket(sock, data)=="BAD_SOCK":
        return "BAD_SOCK"
    return recvPacket(sock)

class Packet(object):
    def __init__(self, data, do_pack=True):
        self.data=data
        if do_pack:
            self.package()

    def package(self):
        self.data=pickle.dumps(self.data)

    def read(self):
        self.data=pickle.loads(self.data)

class DefaultHandler(object):
    def __init__(self):
        self.handles={}

    def handle(self, pack):
        command = pack[0]
        del pack[0]
        if command in self.handles:
            data = self.handles[command](pack)
            return data
        else:
            return Packet("BAD REQUEST TO HANDLER "+command)

class Server(object):
    def __init__(self, host, port, listen_to=5,
                 password="", handler=DefaultHandler,
                 max_clients=5):
        self.host=host
        self.port=port
        self.listen_to=listen_to
        self.password=password
        self.max_clients=max_clients

        self.handler=handler()

        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.main_socks, self.read_socks = [], []

        self.quit=False

    def connect(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.listen_to)
        self.main_socks=[self.socket]
        self.read_socks=[self.socket]
        return None

    def stop(self):
        for sock in self.main_socks:
            sendPacket(sock, "BAD_SOCK")
            sock.close()
        for sock in self.read_socks:
            sendPacket(sock, "BAD_SOCK")
            sock.close()
        self.socket.close()
        self.main_socks, self.read_socks = [], []
        return None

    def serve(self):
        while 1:
            readables, writebles, exceptions=select.select(self.read_socks,
                                                           [], [])
            for sockobj in readables:

                if sockobj in self.main_socks:
                    if self.max_clients and \
                       len(self.read_socks) <= self.max_clients:
                        new_sock, address = sockobj.accept()
                        pckt=Packet("ACCEPT")
                        sendPacket(new_sock, pckt)
                        self.read_socks.append(new_sock)
                    else:
                        new_sock, a = sockobj.accept()
                        pckt=Packet("REGECT")
                        sendPacket(new_sock, pckt)
                        new_sock.close()

                else:
                    data=recvPacket(sockobj)
                    if data=="BAD_SOCK":
                        sockobj.close()
                        self.read_socks.remove(sockobj)
                    else:
                        data=data.data
                        data=self.handler.handle(data)
                        if data=="STOP_SERVER%s"%self.password:
                            self.stop()
                            break
                        sendPacket(sockobj, data)
        return None
