import threading
import socket
from DB_Class import *
from t import *

db = Database()


def setup_socket():
    """Creates and sets up the socket"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(5)
    return server_socket


def handle_login_message(conn, data):
    username, password = data.split("#")[0], data.split("#")[1]
    message = db.login_check(username, password)
    result, message = message[0], message[1]
    if result:
        build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], message)
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], message)


def handle_register_message(conn, data):
    username, password = data.split("#")[0], data.split("#")[1]
    message = db.create_user(username, password)
    result, message = message[0], message[1]
    if result:
        build_and_send_message(conn, PROTOCOL_SERVER["register_ok_msg"], message)
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["register_failed_msg"], message)


def handle_client_message(client_socket, address):
    """Handles messages from a single client"""
    while True:
        cmd, msg = recv_message_and_parse(client_socket)
        print(cmd, msg, address)
        if cmd == ERROR or msg == ERROR:
            print(f"~connection stopped {address}~")
            client_socket.close()
            break
        elif cmd == "LOGIN":
            handle_login_message(client_socket, msg)
        elif cmd == "REGISTER":
            handle_register_message(client_socket, msg)

    client_socket.close()


def main():
    """Main function for the server"""
    server_socket = setup_socket()
    print("Server is listening for clients...")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address}")
        client_thread = threading.Thread(target=handle_client_message, args=(client_socket, address))
        client_thread.start()


if __name__ == "__main__":
    main()
