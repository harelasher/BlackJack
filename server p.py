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
            "result": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        }
    ],
    "dealer": {
        "cards": [],
        "is_showing": False
    },
    "is_game_over": True,
    "timer": [None, None, None],
    "winner": None
}
all_players_table1 = {}
game_state2 = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        }
    ],
    "dealer": {
        "cards": [],
        "is_showing": False
    },
    "is_game_over": True,
    "timer": [None, None, None],
    "winner": None
}
all_players_table2 = {}
game_state3 = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": [],
            "bet": None,
            "reaction": None,
            "result": None
        }
    ],
    "dealer": {
        "cards": [],
        "is_showing": False
    },
    "is_game_over": True,
    "timer": [None, None, None],
    "winner": None
}
all_players_table3 = {}
tables = [game_state, game_state2, game_state3]
all_table_players = [all_players_table1, all_players_table2, all_players_table3]


def setup_socket():
    """Creates and sets up the socket"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 51235))
    server_socket.listen(MAX_CONNECTIONS)
    return server_socket


def handle_login_message(conn, data, address):
    username, password = data.split("#")[0], data.split("#")[1]
    message = db.login_check(username, password)
    result, message = message[0], message[1]
    if result:
        logged_users[address] = username
        build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], str(db.get_user_info(username)))
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], message)


def handle_logout_message(username, address):
    logged_users[address] = ""
    db.logout(username)
    del logged_users[address]
    print(f'logout username: ({username}) OK')


def handle_register_message(conn, data, address):
    username, password = data.split("#")[0], data.split("#")[1]
    message = db.create_user(username, password)
    result, message = message[0], message[1]
    if result:
        logged_users[address] = username
        build_and_send_message(conn, PROTOCOL_SERVER["register_ok_msg"], str(db.get_user_info(username)))
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["register_failed_msg"], message)


def handle_change_pfp_message(conn, data):
    username, pfp = data.split("#")[0], data.split("#")[1]
    result = db.change_pfp_pic(username, pfp)
    if result:
        build_and_send_message(conn, PROTOCOL_SERVER['change_pfp_ok'], str(db.get_user_info(username)))


def handle_leaderboard_message(conn):
    users = db.get_top_users()
    build_and_send_message(conn, PROTOCOL_SERVER['leaderboard_ok'], str(users))


def handle_join_seat(conn, data, address):
    chosen_table, chosen_seat = data.split("#")[0], data.split("#")[1]
    if tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"] is not None:
        return build_and_send_message(conn, PROTOCOL_SERVER['error_msg'], "")
    for user in logged_users:
        if user == address:
            user_info = db.get_user_info(logged_users[user])
            tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"] = user_info[1]
            tables[int(chosen_table)]["seats"][int(chosen_seat)]["profile_picture"] = user_info[4]
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'], str(tables[int(chosen_table)]))


def handle_leave_seat(conn, data, address):
    chosen_table, chosen_seat = data.split("#")[0], data.split("#")[1]
    if tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"] is None:
        return build_and_send_message(conn, PROTOCOL_SERVER['error_msg'], "")
    tables[int(chosen_table)]["seats"][int(chosen_seat)]["name"] = None
    tables[int(chosen_table)]["seats"][int(chosen_seat)]["profile_picture"] = None
    tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"] = None
    check_starting_game(chosen_table)


def handle_join_table(conn, data, address):
    all_table_players[int(data)][logged_users[address]] = conn
    tables[int(data)]["timer"][2] = time.time()
    build_and_send_message(conn, PROTOCOL_SERVER['leaderboard_ok'], str(tables[int(data)]))


def handle_leave_table(conn, data, address):
    del all_table_players[int(data)][logged_users[address]]
    build_and_send_message(conn, PROTOCOL_SERVER['leave_table_ok'], "")


def handle_leave_game(conn, data, address):
    build_and_send_message(conn, PROTOCOL_SERVER['leave_table_ok'], "")
    username, chosen_table, chosen_seat = data.split("#")[0], data.split("#")[1], data.split("#")[2]
    del all_table_players[int(chosen_table)][username]
    if chosen_seat is not None and tables[int(chosen_table)]['is_game_over'] is True:
        handle_leave_seat(conn, chosen_table + DATA_DELIMITER + chosen_seat, address)


def handle_change_bet(data):
    chosen_table, chosen_seat, bet_size = data.split("#")[0], data.split("#")[1], data.split("#")[2]
    if bet_size == "None":
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"] = None
    else:
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["bet"] = bet_size
    check_starting_game(chosen_table)


def check_starting_game(chosen_table):
    running = False
    game_thread = threading.Thread(target=handle_game_blackjack, args=(chosen_table,))
    for player in tables[int(chosen_table)]["seats"]:
        if player["bet"] is not None:
            running = True
    if running and tables[int(chosen_table)]["timer"][0] is None:
        tables[int(chosen_table)]["timer"][0] = time.time()
        tables[int(chosen_table)]["timer"][1] = time.time() + 10
        tables[int(chosen_table)]["timer"][2] = time.time()
        game_thread.start()
    elif not running:
        print("closing..")
        game_thread.join
        print("closed")
        tables[int(chosen_table)]["timer"][0] = None
        tables[int(chosen_table)]["timer"][1] = None
        tables[int(chosen_table)]["timer"][2] = None
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'], str(tables[int(chosen_table)]))


def handle_game_blackjack(chosen_table):
    a = 9223372036854775807
    while a is not None:
        a = tables[int(chosen_table)]["timer"][1]
        if time.time() >= a and not None:
            tables[int(chosen_table)]["timer"][0] = time.time()
            tables[int(chosen_table)]["timer"][1] = time.time() + 15
            tables[int(chosen_table)]["timer"][2] = time.time()
            tables[int(chosen_table)]["is_game_over"] = False
            for player in tables[int(chosen_table)]["seats"]:
                if player["bet"] is None:
                    player["name"] = None
                    player["profile_picture"] = None
                elif player["name"] is not None:
                    player["cards"] = [str(random.randint(1, 10)), str(random.randint(1, 10))]
                    calculate_card_result(player)
            for player in all_table_players[int(chosen_table)].values():
                build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'], str(tables[int(chosen_table)]))
            a = None
    a = 9223372036854775807
    while a is not None:
        a = tables[int(chosen_table)]["timer"][1]
        if time.time() < a and not None:
            for player in tables[int(chosen_table)]["seats"]:
                if player["name"] is not None and player["reaction"] is not None:
                    if player["reaction"] == "hit":
                        calculate_card_result(player)
                        player["reaction"] = None
                        for player in all_table_players[int(chosen_table)].values():
                            build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'],
                                                   str(tables[int(chosen_table)]))
                    elif player["reaction"] == "stand":
                        player["result"] = "stand"
                        player["reaction"] = None
                        for player in all_table_players[int(chosen_table)].values():
                            build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'],
                                                   str(tables[int(chosen_table)]))
                    elif player["reaction"] == "double_down":
                        calculate_card_result(player)
                        player["reaction"] = None
                        for player in all_table_players[int(chosen_table)].values():
                            build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'],
                                                   str(tables[int(chosen_table)]))
        else:
            a = None
    tables[int(chosen_table)]["timer"][0] = None
    tables[int(chosen_table)]["timer"][1] = None
    tables[int(chosen_table)]["timer"][2] = None
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'],
                               str(tables[int(chosen_table)]))



def calculate_card_result(player):
    player["cards"].append(str(random.randint(1, 10)))
    if sum(list(map(int, player["cards"]))) == 21:
        player["result"] = "blackjack"
    else:
        player["result"] = "busted"


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
            if address in logged_users:
                handle_logout_message(logged_users[address], address)
            print(f"~connection stopped {address}~")
            client_socket.close()
            for i in range(len(all_table_players)):
                for key in all_table_players[i]:
                    if all_table_players[i][key] == client_socket:
                        for j in range(len(tables[i]["seats"])):
                            if tables[i]["seats"][j]["name"] == key and tables[i]['is_game_over'] is True:
                                del all_table_players[i][key]
                                handle_leave_seat(client_socket, str(i) + DATA_DELIMITER + str(j), address)
                                return
                        del all_table_players[i][key]
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
            handle_join_seat(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT['leave_seat']:
            handle_leave_seat(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT["join_table"]:
            handle_join_table(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT["leave_table"]:
            handle_leave_table(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT["leave_game"]:
            handle_leave_game(client_socket, msg, address)
        elif cmd == PROTOCOL_CLIENT["change_bet"]:
            handle_change_bet(msg)
        elif cmd == PROTOCOL_CLIENT["reaction"]:
            handle_reaction(client_socket, msg, address)

    client_socket.close()


def handle_reaction(conn, data, address):
    chosen_table, chosen_seat, reaction = data.split("#")[0], data.split("#")[1], data.split("#")[2]
    if reaction == "hit":
        tables[int(chosen_table)]["seats"][int(chosen_seat)]["reaction"] = reaction


def handle_server_message():
    while True:
        value = input(f"\033[95m ~~~~~~enter a command for the server~~~~~~ \033[0m \n")
        if value == "users":
            print(f"\033[94m {str(logged_users)} \033[0m")
        elif value == "add":
            username = input(f"\033[95m ~~~~~~input username~~~~~~ \033[0m \n")
            amount = input(f"\033[95m ~~~~~~input amount~~~~~~ \033[0m \n")
            print(f"\033[94m {db.update_user_score(username, amount)} \033[0m")
        elif value == "tables":
            print(f"\033[94m {game_state} \033[0m")
        elif value == "players":
            print(f"\033[94m {all_players_table1} \033[0m")


def main():
    """Main function for the server"""
    server_socket = setup_socket()
    print("Server is listening for clients...")
    server_thread = threading.Thread(target=handle_server_message, args=())
    server_thread.start()

    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address}")
        client_thread = threading.Thread(target=handle_client_message, args=(client_socket, address))
        client_thread.start()


if __name__ == "__main__":
    main()
