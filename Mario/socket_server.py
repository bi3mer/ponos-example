from computational_metrics import percent_linearity, percent_leniency
from summerville_agent import percent_playable
from grid_tools import rows_into_columns

from json import load, loads, dumps
import logging
import socket
import os

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
                    elif cmd == b'levels':
                        lvls = []
                        for file_name in os.listdir('levels'):
                            with open(os.path.join('levels', file_name), 'r') as f:
                                lvls.append(rows_into_columns(f.readlines()))

                        conn.sendall((dumps(lvls)+'EOF').encode())
                    elif cmd[:6] == b'assess':
                        lvl = loads(cmd[6:].decode('utf-8'))
                        return_data = {
                            'completability': percent_playable(lvl),
                            'linearity': percent_linearity(lvl),
                            'leniency': percent_leniency(lvl),
                        }

                        conn.sendall(dumps(return_data).encode('utf-8'))
                    else:
                        print(f'Unrecognized command: {cmd}')
                        error_message = bytes(f'Unrecognized command: {cmd}', 'utf-8')
                        conn.sendall(error_message)

if __name__ == "__main__":
    server()
