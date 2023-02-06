import socket
import game


def connect(ip, port):
    """Connects to the server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    return client_socket


def send_message(client_socket, message):
    """Sends a message to the server"""
    client_socket.send(message.encode())


def rec_message(client_socket):
    """Receives a message from the server"""
    return client_socket.recv(1024).decode()


def main(ip, port):
    """Main function for the client"""
    client_socket = connect(ip, port)
    game.main_menu()
    client_socket.close()


if __name__ == "__main__":
    main("127.0.0.1", 5000)
