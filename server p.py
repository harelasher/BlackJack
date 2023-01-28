import threading
import socket


def rec_message(client_socket):
    data = client_socket.recv(1024).decode()
    if len(data) == 0:
        return ""
    return data


def handle_client_message(client_socket, address):
    """Handles messages from a single client"""
    while True:
        message = rec_message(client_socket)
        print(message)
        if len(message) == 0:
            print("~connection stopped~")
            client_socket.close()
            break
        if message == "bye":
            client_socket.send("bye".encode())
            client_socket.close()
            break

        client_socket.send(f"You sent: {message}".encode())
    client_socket.close()


def setup_socket():
    """Creates and sets up the socket"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(5)
    return server_socket


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
