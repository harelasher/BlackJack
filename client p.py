import socket
import game
import t


def connect(ip, port):
    """Connects to the server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    return client_socket


def build_send_recv_parse(conn, code, data):  # מחבר את שתי הפונקציה, יוצר הודעה שולח אותה ומחכה לתשובה
    build_and_send_message(conn, code, data)
    msg_code, msg = recv_message_and_parse(conn)
    return msg_code, msg


def build_and_send_message(conn, code, msg):  # פונקציה לבניית הודעה ושליחה לשרת
    full_msg = t.build_message(code, msg)  # בונה את ההודעה
    conn.send(full_msg.encode('utf-8'))  # ושולח את ההודעה


def recv_message_and_parse(conn):  # פונקציה לקבלת מידע מהשרת
    data = conn.recv(1024).decode()  # הלקוח קולט מידע
    cmd, msg = t.parse_message(data)  # מנתח את המידע
    if cmd != t.ERROR or msg != t.ERROR:  # אם המידע הוא לא שגיאה
        # print(f"The server sent: {data}")
        # print(f"Interpretation:\nCommand: {cmd}, message: {msg}")
        return cmd, msg
    else:
        return t.ERROR, t.ERROR


def main(ip, port):
    """Main function for the client"""
    client_socket = connect(ip, port)
    game.main_menu()
    client_socket.close()


if __name__ == "__main__":
    main("127.0.0.1", 5000)
