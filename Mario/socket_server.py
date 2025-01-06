from json import load
import socket

def server(host='localhost', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            with conn:
                while True:
                    cmd = conn.recv(1024)
                    if not cmd:
                        break

                    if cmd == b"config":
                        with open('config.json', 'r') as f:
                            conn.sendall(bytes(f.read(), 'utf-8'))
                    else:
                        error_message = bytes(f'Unrecognized command: {cmd}', 'utf-8')
                        conn.sendall(error_message)

if __name__ == "__main__":
    server()
