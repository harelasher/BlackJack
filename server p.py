import threading
import socket
from DB_Class import *
from t import *
import time
import random

db = Database()
db.make_all_users_offline()

MAX_CONNECTIONS = 5

logged_users = {}

game_state = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        }
    ],
    "dealer": {
        "cards": [],
        "result": [None, None]
    },
    "is_game_over": True,
    "timer": [None, None, None]
}  # table 1
all_players_table1 = {}  # all the players in table 1
game_state2 = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        }
    ],
    "dealer": {
        "cards": [],
        "result": [None, None]
    },
    "is_game_over": True,
    "timer": [None, None, None]
}  # table 2
all_players_table2 = {}  # all the players in table 2
game_state3 = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": [None, None],
            "wlp": None
        }
    ],
    "dealer": {
        "cards": [],
        "result": [None, None]
    },
    "is_game_over": True,
    "timer": [None, None, None]
}  # table 3
all_players_table3 = {}  # all the players in table 3
tables = [game_state, game_state2, game_state3]  # array of the tables
all_table_players = [all_players_table1, all_players_table2, all_players_table3]  # array of the players in tables
card_names = [
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "jc", "qc", "kc", "ac",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "jd", "qd", "kd", "ad",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "jh", "qh", "kh", "ah",
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "js", "qs", "ks", "as"
]  # all the card names


def setup_socket():
    """creates and sets up the socket"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 51235))
    server_socket.listen(MAX_CONNECTIONS)
    return server_socket


def handle_login_message(conn, data, address):
    """Function to handle login messages from clients"""
    username, password = data.split("#")[0], data.split("#")[1]
    message = db.login_check(username, password)
    result, message = message[0], message[1]
    if result:
        logged_users[address] = username
        build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], str(db.get_user_info(username)))
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], message)


def handle_logout_message(username, address):
    """Function to handle logout messages from clients"""
    logged_users[address] = ""
    db.logout(username)
    del logged_users[address]
    print(f'logout username: ({username}) OK')


def handle_register_message(conn, data, address):
    """Function to handle register messages from clients"""
    username, password = data.split("#")[0], data.split("#")[1]
    message = db.create_user(username, password)
    result, message = message[0], message[1]
    if result:
        logged_users[address] = username
        build_and_send_message(conn, PROTOCOL_SERVER["register_ok_msg"], str(db.get_user_info(username)))
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["register_failed_msg"], message)


def handle_change_pfp_message(conn, data):
    """Function to handle change profile picture messages from clients"""
    username, pfp = data.split("#")[0], data.split("#")[1]
    result = db.change_pfp_pic(username, pfp)
    if result:
        build_and_send_message(conn, PROTOCOL_SERVER['change_pfp_ok'], str(db.get_user_info(username)))


def handle_leaderboard_message(conn):
    """Function to handle leaderboard messages from clients"""
    users = db.get_top_users()
    build_and_send_message(conn, PROTOCOL_SERVER['leaderboard_ok'], str(users))


def handle_join_seat(conn, data):
    """Function to handle joining a seat at a table"""
    pfp, username, chosen_table, seat = data.split("#")[0], data.split("#")[1], data.split("#")[2], data.split("#")[3]
    if tables[int(chosen_table)]["seats"][int(seat)]["name"] is not None:
        # Check if the seat is already occupied by another player
        return build_and_send_message(conn, PROTOCOL_SERVER['error_msg'], "")
    tables[int(chosen_table)]["seats"][int(seat)]["name"] = username
    tables[int(chosen_table)]["seats"][int(seat)]["profile_picture"] = pfp
    db.update_in_table(username, chosen_table)
    for player in all_table_players[int(chosen_table)].values():
        # send all the players at the table the updated table
        build_and_send_message(player, PROTOCOL_SERVER['get_info_table'], str(tables[int(chosen_table)]))


def handle_leave_seat(conn, data):
    """Function to handle leaving a seat at a table"""
    chosen_table, chosen_seat = data.split("#")[0], data.split("#")[1]
    if tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"] is None:
        return build_and_send_message(conn, PROTOCOL_SERVER['error_msg'], "")
    db.update_in_table(tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"], "n")
    tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"] = None
    tables[int(chosen_table)]["seats"][int(chosen_seat)]["profile_picture"] = None
    tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"] = None
    check_starting_game(chosen_table)  # Check if the game needs to stop


def handle_join_table(conn, data, address):
    """Function to handle joining a table"""
    username, chosen_table = data.split("#")[0], data.split("#")[1]
    TableStatus = db.get_in_table(username)
    if TableStatus != chosen_table and TableStatus != "n":
        # Check if the player is already at a different table or if the status is not "n" (not at a table)
        return build_and_send_message(conn, PROTOCOL_SERVER['error_msg'], "")
    all_table_players[int(chosen_table)][logged_users[address]] = conn
    tables[int(chosen_table)]["timer"][2] = time.time()  # Add the player's connection time
    build_and_send_message(conn, PROTOCOL_SERVER['get_info_table'], str(tables[int(chosen_table)]))
    # Send the table information to the player


def handle_leave_table(conn, data, address):
    """Function to handle leaving a table"""
    del all_table_players[int(data)][logged_users[address]]
    build_and_send_message(conn, PROTOCOL_SERVER['get_info_table'], "")


def handle_leave_game(conn, data):
    """Function to handle leaving a game(unexpected exit)"""
    build_and_send_message(conn, PROTOCOL_SERVER['leave_table_ok'], "")
    username, chosen_table, chosen_seat = data.split("#")[0], data.split("#")[1], data.split("#")[2]
    del all_table_players[int(chosen_table)][username]
    if chosen_seat != "None" and tables[int(chosen_table)]['is_game_over'] is True:
        # Check if the chosen seat is not "None" and if the game at the chosen table is over
        handle_leave_seat(conn, chosen_table + DATA_DELIMITER + chosen_seat)


def handle_change_bet(data):
    """Function to handle the betting size"""
    chosen_table, chosen_seat, bet_size = data.split("#")[0], data.split("#")[1], data.split("#")[2]
    if tables[int(chosen_table)]["is_game_over"] is True:
        # Check if the game at the chosen table is over
        if bet_size == "None":
            tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"] = None
        else:
            tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"] = bet_size
        check_starting_game(chosen_table)  # Check if the game needs to stop


def check_starting_game(chosen_table):
    """Function to check if the game can start at the chosen table"""
    running = False
    game_thread = threading.Thread(target=handle_game_blackjack, args=(chosen_table,))
    for player in tables[int(chosen_table)]["seats"]:
        if player["bet"] is not None:
            # If a player has placed a bet, set the running flag to True
            running = True
    if running and tables[int(chosen_table)]["timer"][0] is None:
        # Check if the game should start and a timer is not already running
        print("strating new table thread...")
        tables[int(chosen_table)]["timer"][0] = time.time()
        tables[int(chosen_table)]["timer"][1] = time.time() + 10
        tables[int(chosen_table)]["timer"][2] = time.time()
        game_thread.start()
        # Start the game thread
    elif not running:
        # game_thread.join
        tables[int(chosen_table)]["timer"][0] = None
        tables[int(chosen_table)]["timer"][1] = None
        tables[int(chosen_table)]["timer"][2] = None
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['get_info_table'], str(tables[int(chosen_table)]))


def handle_game_blackjack(chosen_table):
    """Function to handle the blackjack game at the chosen table"""
    time1 = tables[int(chosen_table)]["timer"][1]  # Get the end time for the game from the table timer

    if time1 is None:  # Check if the game should be closed (end time is None)
        print("closing thread")
        return
    time.sleep(tables[int(chosen_table)]["timer"][1] - time.time())  # Sleep until the end time is reached
    if tables[int(chosen_table)]["timer"][1] != time1 or tables[int(chosen_table)]["timer"][1] is None or \
            not tables[int(chosen_table)]["is_game_over"]:
        # Check if the end time has changed or is None, or if the game is already over
        print("closing thread")
        return
    # Start a timer - getting the players reactions
    tables[int(chosen_table)]["timer"][0] = time.time()
    tables[int(chosen_table)]["timer"][1] = time.time() + 13
    tables[int(chosen_table)]["timer"][2] = time.time()
    tables[int(chosen_table)]["is_game_over"] = False
    # Send updated table information to all players at the chosen table
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['get_info_table'], str(tables[int(chosen_table)]))
    tables[int(chosen_table)]["dealer"]["cards"] = [random.choice(card_names)]  # Deal cards to the dealer
    calculate_card_result(tables[int(chosen_table)]["dealer"])
    # Deal cards to the players and calculate their card results
    for player in tables[int(chosen_table)]["seats"]:
        if player["bet"] is None:
            player["name"] = None
            player["profile_picture"] = None
        elif player["name"] is not None:
            player["cards"] = [random.choice(card_names), random.choice(card_names)]
            calculate_card_result(player)
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['get_info_table'], str(tables[int(chosen_table)]))
    time.sleep(tables[int(chosen_table)]["timer"][1] - time.time())
    # Sleep until the end time is reached for the player actions
    while int(tables[int(chosen_table)]["dealer"]["result"][0]) < 17:
        # Dealer's turn: Draw cards until the dealer's hand value reaches 17 or more
        tables[int(chosen_table)]["dealer"]["cards"].append(random.choice(card_names))
        calculate_card_result(tables[int(chosen_table)]["dealer"])

    for player in tables[int(chosen_table)]["seats"]:
        # Determine the game results for each player
        if player["name"] is not None:
            if int(player["result"][0]) > 21:
                player["wlp"] = "loss"
                db.update_user_score(player["name"], "-" + player["bet"])
                db.update_win_loss_push(player["name"], player["wlp"])
            elif int(tables[int(chosen_table)]["dealer"]["result"][0]) > 21 or\
                    int(player["result"][0]) > int(tables[int(chosen_table)]["dealer"]["result"][0]):
                player["wlp"] = "win"
                if int(player["result"][0]) == 21 and len(player["cards"]) == 2:

                    db.update_user_score(player["name"], str(round(int(player["bet"])*3/2)))
                    db.update_win_loss_push(player["name"], player["wlp"])
                else:
                    db.update_user_score(player["name"], player["bet"])
                    db.update_win_loss_push(player["name"], player["wlp"])
            elif int(player["result"][0]) == int(tables[int(chosen_table)]["dealer"]["result"][0]):
                player["wlp"] = "push"
                db.update_win_loss_push(player["name"], player["wlp"])
            else:
                player["wlp"] = "loss"
                db.update_user_score(player["name"], "-" + player["bet"])
                db.update_win_loss_push(player["name"], player["wlp"])
            if player["name"] in all_table_players[int(chosen_table)]:
                build_and_send_message(all_table_players[int(chosen_table)][player["name"]],
                                       PROTOCOL_SERVER['update_info'], str(db.get_user_info(player["name"])))
    # Reset timer values
    tables[int(chosen_table)]["timer"][0] = None
    tables[int(chosen_table)]["timer"][1] = None
    tables[int(chosen_table)]["timer"][2] = None
    # Send updated table information to all players at the chosen table
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['get_info_table'],
                               str(tables[int(chosen_table)]))
    time.sleep(5)
    # Reset timer values and set the game status to over
    tables[int(chosen_table)]["timer"][0] = None
    tables[int(chosen_table)]["timer"][1] = None
    tables[int(chosen_table)]["timer"][2] = None
    tables[int(chosen_table)]["is_game_over"] = True
    tables[int(chosen_table)]["dealer"]["cards"] = []
    tables[int(chosen_table)]["dealer"]["result"] = [None, None]
    for player in tables[int(chosen_table)]["seats"]:
        # Reset player data and update their in_table status
        if player["name"] not in all_table_players[int(chosen_table)]:
            db.update_in_table(player["name"], "n")
            player["name"] = None
            player["profile_picture"] = None

        player["bet"] = None
        player["cards"] = []
        player["reaction"] = None
        player["result"] = [None, None]
        player["wlp"] = None
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['get_info_table'],
                               str(tables[int(chosen_table)]))


def calculate_card_result(player):
    """calculate card point funtion"""
    total = 0
    num_aces = 0

    for card in player["cards"]:
        if card[0] == 'a':
            num_aces += 1
            total += 11
        elif card[0] in ["j", "q", "k", "1"]:
            total += 10
        else:
            total += int(card[0])

    while total > 21 and num_aces > 0:
        total -= 10
        num_aces -= 1

    if total == 21:
        player["result"] = [str(total), "blackjack"]
    elif total > 21:
        player["result"] = [str(total), "busted"]
    else:
        player["result"] = [str(total), None]


def handle_client_message(client_socket, address):
    """Handles messages from a single client"""
    logged_users.update({address: ""})
    while True:
        try:
            cmd, msg = recv_message_and_parse(client_socket)
        except ConnectionResetError or OSError:
            cmd, msg = ERROR, ERROR
        print(cmd, msg, address)
        if cmd == ERROR or msg == ERROR:
            # handle unexpected logout
            if address in logged_users:
                handle_logout_message(logged_users[address], address)
            print(f"~connection stopped {address}~")
            client_socket.close()
            for i in range(len(all_table_players)):
                for key1 in all_table_players[i]:
                    if all_table_players[i][key1] == client_socket:
                        for j in range(len(tables[i]["seats"])):
                            if tables[i]["seats"][j]["name"] == key1 and tables[i]['is_game_over'] is True:
                                del all_table_players[i][key1]
                                handle_leave_seat(client_socket, str(i) + DATA_DELIMITER + str(j))
                                return
                        del all_table_players[i][key1]
                        return
            return
        elif cmd == PROTOCOL_CLIENT['login_msg']:
            handle_login_message(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT['register_msg']:
            handle_register_message(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT['logout_msg']:
            handle_logout_message(msg, address)
        elif cmd == PROTOCOL_CLIENT['change_pfp']:
            handle_change_pfp_message(client_socket, msg)
        elif cmd == PROTOCOL_CLIENT['get_leaderboard']:
            handle_leaderboard_message(client_socket)
        elif cmd == PROTOCOL_CLIENT['join_seat']:
            handle_join_seat(client_socket, msg)
        elif cmd == PROTOCOL_CLIENT['leave_seat']:
            handle_leave_seat(client_socket, msg)
        elif cmd == PROTOCOL_CLIENT["join_table"]:
            handle_join_table(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT["leave_table"]:
            handle_leave_table(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT["leave_game"]:
            handle_leave_game(client_socket, msg)
        elif cmd == PROTOCOL_CLIENT["change_bet"]:
            handle_change_bet(msg)
        elif cmd == PROTOCOL_CLIENT["reaction"]:
            handle_reaction(msg)
        elif cmd == PROTOCOL_CLIENT["check_hour"]:
            check_hourly_pay(client_socket, msg)


def handle_reaction(data):
    """Handles the reaction of the player while sitting in the table"""
    chosen_table, chosen_seat, reaction = data.split("#")[0], data.split("#")[1], data.split("#")[2]
    print(f"table:{chosen_table}-seat:{chosen_seat}-chose:{reaction} ")
    if len(tables[int(chosen_table)]["dealer"]["cards"]) > 1:
        # if the dealer already has more than 1 card, the function returns with nothing
        return
    if reaction == "hit":  # player hits and requests another card
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["cards"].append(random.choice(card_names))
        calculate_card_result(tables[int(chosen_table)]["seats"][int(chosen_seat)])  # calculate points of the cards
        for player in all_table_players[int(chosen_table)].values():
            # sends every player in the table the state of the board
            build_and_send_message(player, PROTOCOL_SERVER['get_info_table'],
                                   str(tables[int(chosen_table)]))
    elif reaction == "stand":  # player stands
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["reaction"] = reaction
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["result"][1] = "stand"
        for player in all_table_players[int(chosen_table)].values():
            # sends every player in the table the state of the board
            build_and_send_message(player, PROTOCOL_SERVER['get_info_table'],
                                   str(tables[int(chosen_table)]))
    elif reaction == "double_down":  # player Double down- double bet and gets only ONE card
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["reaction"] = reaction
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"]\
            = str(2 * int(tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"]))  # makes his bed times 2

        tables[int(chosen_table)]["seats"][int(chosen_seat)]["cards"].append(random.choice(card_names))
        # gets random card
        calculate_card_result(tables[int(chosen_table)]["seats"][int(chosen_seat)])
        # calculate points of the cards
        for player in all_table_players[int(chosen_table)].values():
            build_and_send_message(player, PROTOCOL_SERVER['get_info_table'],
                                   str(tables[int(chosen_table)]))


def check_hourly_pay(conn, username):
    """The client send their username in order to know if they are eligible for the hourly pay"""
    result = db.has_passed_one_hour(username)  # checks with the database
    build_and_send_message(conn, PROTOCOL_SERVER["update_info"], str([db.get_user_info(username), result]))
    # sends the client a response


def main():
    """Main function for the server
    The server waits for any connection with a client, and then it makes it a thread which handles it requests."""
    server_socket = setup_socket()
    print("Server is listening for clients...")

    while True:
        client_socket, address = server_socket.accept()  # accepts client connection, and makes a thread for it.
        print(f"Client connected from {address}")
        client_thread = threading.Thread(target=handle_client_message, args=(client_socket, address))
        client_thread.start()


if __name__ == "__main__":
    main()
