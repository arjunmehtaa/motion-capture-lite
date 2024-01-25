import socket
import time

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_hosts = ["192.168.75.11", "192.168.75.12"]
sending_udp_port = 4210
listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

while True:
    # Send message to all Arduinos
    print("Waiting for client...")
    msg = "Hello from Python: " + str(counter)
    for udp_host in udp_hosts:
        sock_send.sendto(msg.encode(), (udp_host, sending_udp_port))
    counter += 1

    time.sleep(0.5)

    # Receive messages from Arduinos
    for _ in range(len(udp_hosts)):
        try:
            data, addr = sock_listen.recvfrom(1024)
            print("Received Messages:", data, " from", addr)
        except socket.error as e:
            print("Error while listening Arduino package: ", e)
