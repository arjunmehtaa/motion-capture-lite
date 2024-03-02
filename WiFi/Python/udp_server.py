import socket
import time
import threading
import queue

sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)


def receive_messages():
    print("in receiving messages")
    counter = 0
    while True:
        try:
            data, addr = sock_listen.recvfrom(1024)
            counter += 1
            print(counter)
            print("Received Message:", data.decode("utf-8"), "from", addr)
            # message_queue.put({data, addr})
        except KeyboardInterrupt:
            print("Exiting receive_messages thread")
            sock_listen.close()
            break
        except Exception:
            # print("No message received")
            pass


if __name__ == "__main__":
    print(sock_listen.getsockname())
    receive_messages()
    # print out my IP
