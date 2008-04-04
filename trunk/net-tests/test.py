from game_client1 import *


def main():
    a = Client("testy")
    b = Client("testy2")

    a.send_message("Hello World!") #to lobby
    print a.get_messages() #from lobby only right now
    print b.get_messages()

    print "--------------------"

    print a.get_games()

    print a.start_new_game("test#1", 5)

    print "--------------------"

    print a.get_games()
    print b.get_games()

    print "--------------------"

    b.join_game("test#1")
    print b.get_games()

    print "--------------------"

    a.send_message("hey again") #to game now
    print a.get_messages() #should be from game ;)
    print b.get_messages()

    print "--------------------"

    print a.get_num_players()
    print b.get_num_players()

    print a.get_player_number()
    print b.get_player_number()

    print "--------------------"

    a.change_num_players(3)
    print a.get_num_players()
    print a.get_player_number()

    print "--------------------"

    print a.get_map()

    print "--------------------"

    a.add_ai_player()
    print a.get_players()
    print b.get_players()

    print "--------------------"

    a.begin_game()
    print a.get_messages()
    print b.get_messages()

    print "--------------------"

    print a.get_whos_turn()
    print b.get_whos_turn()
    print a.is_my_turn()
    print b.is_my_turn()

    print "--------------------"
    print "--------------------"

    if a.is_my_turn():
        a.update_world("t1", "t2", 5, 10, "Yes!")
    if b.is_my_turn():
        b.update_world("t1", "t2", 5, 10, "No!")

    if a.is_my_turn():
        a.end_turn()
    if b.is_my_turn():
        b.end_turn()

    print a.get_whos_turn()

    print "--------------------"

    print a.get_messages()
    print b.get_messages()

main()
