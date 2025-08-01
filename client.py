import socket

HOST = 'localhost'
PORT = 5555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        try:
            msg = s.recv(1024).decode()
            if not msg:
                break
            print(msg)
            if "Send your move" in msg:
                move = input("Enter your move (rock/paper/scissors): ")
                s.sendall(move.strip().encode())
        except:
            break
