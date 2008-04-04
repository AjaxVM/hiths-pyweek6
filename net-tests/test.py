import socket, thread, sys
import net


##host = "localhost"
##port = 12345
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((host, port))
##
##a = net.recvPacket(s).data
##print a

global finished
finished=False
def send(s, user_name):
    global finished
    while 1:
        #send message
        d=raw_input("")
        if not finished:
            net.request(s, net.Packet(["MESSAGE",user_name,d]))
        else:
            return


def recv(s, user_name):
    global finished
    while 1:
        #get messages...
        pckt = net.request(s, net.Packet(["GET_MESSAGES",user_name]))
        if pckt=="BAD_SOCK":
            print "##Server Connection Lost!##\npress any key to continue"
            finished=True
            raise SystemExit()
            return
        for i in pckt.data:
            if not i[0]==user_name:
                print "\t"+i[0]+": "+i[1]


def main():
    host="localhost"
    port=12345
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    #see if we were accepted or not...
    a=net.recvPacket(s).data

    user_name=raw_input('user_name: ')
    net.request(s, net.Packet(["USER_JOIN", user_name]))
    
    thread.start_new(recv, (s,user_name))
    global finished
    while not finished:
        if a=="REGECT":
            return

        send(s, user_name)
    return

main()

