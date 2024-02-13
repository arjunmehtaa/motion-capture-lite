import socket
import time
import threading
import queue

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_hosts = ["192.168.0.11", "192.168.0.12"]
sending_udp_port = 4210
counter = 1

message_queue = queue.Queue()

counter = 0
while counter<101:
    time.sleep(500/1000)
    try:

        msg = str(counter)
        for udp_host in udp_hosts:
            sock_send.sendto(msg.encode(), (udp_host, sending_udp_port))
        counter += 1
    except KeyboardInterrupt:
        print("Exiting send_messages thread")
        sock_send.close()
        break