import threading
import socket
from DB_Class import *
from t import *

db = Database()
db.make_all_users_offline()

logged_users = {}


def setup_socket():
    """Creates and sets up the socket"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 51235))
    server_socket.listen(5)
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


def handle_client_message(client_socket, address):
    """Handles messages from a single client"""
    logged_users.update({address: ""})
    while True:
        cmd, msg = recv_message_and_parse(client_socket)
        print(cmd, msg, address)
        if cmd == ERROR or msg == ERROR:
            handle_logout_message(logged_users[address], address)
            del logged_users[address]
            print(f"~connection stopped {address}~")
            client_socket.close()
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
