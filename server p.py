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
    result = db.login_check(username, password)
    if result:
        build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], "fails")


def handle_client_message(client_socket):
    """Handles messages from a single client"""
    while True:
        cmd, msg = recv_message_and_parse(client_socket)
        if len(cmd) == 0 or len(msg) == 0:
            print("~connection stopped~")
            client_socket.close()
            break
        elif cmd == "LOGIN":
            handle_login_message(client_socket, msg)
    client_socket.close()


def main():
    """Main function for the server"""
    server_socket = setup_socket()
    print("Server is listening for clients...")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address}")
        client_thread = threading.Thread(target=handle_client_message, args=(client_socket, ))
        client_thread.start()


if __name__ == "__main__":
    main()
