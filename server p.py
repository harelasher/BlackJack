import threading
import socket
from DB_Class import *
from t import *

db = Database()
db.make_all_users_offline()

MAX_CONNECTIONS = 5

logged_users = {}

game_state = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        }
    ],
    "dealer": {
        "cards": None,
        "is_showing": False
    },
    "is_game_over": True,
    "winner": None
}
all_players_table1 = {}
game_state2 = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        }
    ],
    "dealer": {
        "cards": None,
        "is_showing": False
    },
    "is_game_over": True,
    "winner": None
}
all_players_table2 = {}
game_state3 = {
    "seats": [
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        },
        {
            "name": None,
            "profile_picture": None,
            "cards": None,
            "bet": None
        }
    ],
    "dealer": {
        "cards": None,
        "is_showing": False
    },
    "is_game_over": True,
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
    for player in all_table_players[int(chosen_table)].values():
        build_and_send_message(player, PROTOCOL_SERVER['leaderboard_ok'], str(tables[int(chosen_table)]))


def handle_join_table(conn, data, address):
    all_table_players[int(data)][logged_users[address]] = conn
    build_and_send_message(conn, PROTOCOL_SERVER['leaderboard_ok'], str(tables[int(data)]))


def handle_leave_table(conn, data, address):
    del all_table_players[int(data)][logged_users[address]]
    build_and_send_message(conn, PROTOCOL_SERVER['leave_table_ok'], "")


def handle_leave_game(conn, data, address):
    build_and_send_message(conn, PROTOCOL_SERVER['leave_table_ok'], "")


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
                            print(tables[i]['is_game_over'] is True)
                            print(tables[i]["seats"][j]["name"])
                            print(all_table_players[i][key])
                            if tables[i]["seats"][j]["name"] == key and tables[i]['is_game_over'] is True:
                                del all_table_players[i][key]
                                handle_leave_seat(client_socket, str(i) + DATA_DELIMITER + str(j), address)
                                pass
                        del all_table_players[i][key]
                        break
            break
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
    client_socket.close()


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
