import socket
import time
import threading
import queue

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_hosts = ["192.168.0.11", "192.168.0.12"]
listening_udp_port = 5001
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

message_queue = queue.Queue()

counter = 0
while True:
    try:
        data, addr = sock_listen.recvfrom(1024)
        counter+=1
        print(counter)

    except KeyboardInterrupt:
        print("Exiting receive_messages thread")
        sock_listen.close()
        break                
    except Exception:
        pass