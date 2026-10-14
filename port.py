#!/usr/bin/env python3
import socket, random, os, struct, signal

d = open(os.devnull, 'w')
os.dup2(d.fileno(), 1)
os.dup2(d.fileno(), 2)
d.close()

def cleanup(signum, frame):
    raise SystemExit

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

while True:
    port = random.randint(1024, 1030)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(('', port))
        s.listen(100)
        s.settimeout(101)

        try:
            conn, _ = s.accept()
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                            struct.pack('ii', 1, 0))
            conn.close()
        except socket.timeout:
            pass
    except OSError:
        pass
    finally:
        s.close()   
