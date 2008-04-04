from game_client1 import *


def main():
    a = Client("testy")

    a.send_message("Hello World!") #to lobby
    print a.get_messages() #from lobby only right now

    print a.get_games()

    print a.start_new_game("test#1", 5)

    print a.get_games()

main()
