from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = '#'
PROTOCOL_CLIENT = {'login_msg': 'LOGIN',
                   'logout_msg': 'LOGOUT',
                   'register_msg': "REGISTER",
                   'change_pfp': 'CHANGE_PFP',
                   'get_leaderboard': 'LEADERBOARD',
                   'join_seat': "JOIN_SEAT",
                   "leave_seat": "LEAVE_SEAT",
                   'join_table': "JOIN_TABLE",
                   'leave_table': "LEAVE_TABLE",
                   "leave_game": "LEAVE_GAME",
                   "change_bet": "CHANGE_BET",
                   "reaction": "REACTION",
                   "check_hour": "CHECK_HOUR"}
PROTOCOL_SERVER = {'login_ok_msg': 'LOGIN_OK',
                   'login_failed_msg': 'ERROR',
                   'register_ok_msg': "REGISTER_OK",
                   'register_failed_msg': "ERROR",
                   'change_pfp_ok': 'CHANGE_OK',
                   'leaderboard_ok': 'LEADERBOARD_OK',
                   'leave_table_ok': "LEAVE_TABLE_OK",
                   "get_info_table": "GET_INFO_TABLE",
                   "update_info": "UPDATE_INFO",
                   'error_msg': 'ERROR'}
ERROR = None


def build_message(cmd, data):
    if type(data) is int:
        data = str(data)

    data_length = len(data)
    cmd_length = len(cmd)
    if data_length > MAX_DATA_LENGTH or cmd_length > CMD_FIELD_LENGTH:
        # Check if the data length and the command length exceeds the maximum allowed length
        return ERROR
    else:
        # Pad the command with spaces to the fixed length
        padded_cmd = cmd.strip().ljust(CMD_FIELD_LENGTH)
        # Convert the data length to a string and pad it with zeros to the fixed length
        padded_length = str(data_length).zfill(LENGTH_FIELD_LENGTH)
        full_msg = f"{padded_cmd}{DELIMITER}{padded_length}{DELIMITER}{data}"  # Create the full message
        print(full_msg)
        return encrypt(full_msg)
        # Encrypt the full message and return it


def parse_message(full_msg):
    if len(full_msg) == 0:
        # Check if the full message is empty
        return ERROR, ERROR
    full_msg = decrypt(full_msg).decode()
    # Decrypt the full message and decode it
    if len(full_msg) < CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1:
        return ERROR, ERROR
    cmd_str = full_msg[0:CMD_FIELD_LENGTH]
    length = full_msg[CMD_FIELD_LENGTH + 1:CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH]
    if full_msg[CMD_FIELD_LENGTH] != DELIMITER or full_msg[(CMD_FIELD_LENGTH + LENGTH_FIELD_LENGTH + 1)] != DELIMITER:
        # Check the delimiters and the length format
        return ERROR, ERROR
    elif not length.strip().isdigit():
        return ERROR, ERROR
    length = int(length)
    data_str = full_msg[MSG_HEADER_LENGTH:MSG_HEADER_LENGTH + length]
    if not len(data_str) == length:
        return ERROR, ERROR
    else:
        return cmd_str.strip(), data_str
        # Return the command and data as strings


def build_send_recv_parse(conn, code, data):  # מחבר את שתי הפונקציה, יוצר הודעה שולח אותה ומחכה לתשובה
    build_and_send_message(conn, code, data)
    msg_code, msg = recv_message_and_parse(conn)
    return msg_code, msg


def build_and_send_message(conn, code, msg):  # פונקציה לבניית הודעה ושליחה לשרת
    full_msg = build_message(code, msg)  # בונה את ההודעה
    conn.send(full_msg)  # ושולח את ההודעה


def recv_message_and_parse(conn):  # פונקציה לקבלת מידע מהשרת
    data = conn.recv(1024)  # הלקוח קולט מידע
    cmd, msg = parse_message(data)  # מנתח את המידע
    if cmd != ERROR or msg != ERROR:  # אם המידע הוא לא שגיאה
        return cmd, msg
    else:
        return ERROR, ERROR


key = b'My final project-BlackJack game!'


# Function to encrypt plaintext using AES with the CBC mode
def encrypt(reg_txt):  # Function to encrypt plaintext using AES with the CBC mode
    cipher = AES.new(key, AES.MODE_CBC)  # Create a new AES cipher object
    padded_plaintext = pad(reg_txt.encode(), AES.block_size)
    # Pad the plaintext to a multiple of AES block size (16 bytes)
    enc_txt = cipher.encrypt(padded_plaintext)  # Encrypt the padded plaintext and return the ciphertext
    return cipher.iv + enc_txt  # Return the IV (initialization vector) concatenated with the ciphertext


def decrypt(enc_txt):  # Function to decrypt ciphertext using AES with the CBC mode
    iv = enc_txt[:AES.block_size]  # Extract the IV from the first 16 bytes of the ciphertext
    enc_txt = enc_txt[AES.block_size:]   # Remove the IV from the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Create a new AES cipher object with the same key and IV used during encryption
    reg_txt = cipher.decrypt(enc_txt)  # Decrypt the ciphertext
    unpadded_plaintext = unpad(reg_txt, AES.block_size)  # Remove the padding from the plaintext
    return unpadded_plaintext  # Return the unpadded plaintext
