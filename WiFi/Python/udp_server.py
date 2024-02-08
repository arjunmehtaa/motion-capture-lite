import socket
import time
import threading
import queue

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_hosts = ["192.168.0.11", "192.168.0.12"]
sending_udp_port = 4210
listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

message_queue = queue.Queue()

def send_messages(udp_hosts, sending_udp_port):
    counter = 0
    while counter<101:
        time.sleep(5/1000)
        try:

            msg = str(counter)
            for udp_host in udp_hosts:
                sock_send.sendto(msg.encode(), (udp_host, sending_udp_port))
            counter += 1
        except KeyboardInterrupt:
            print("Exiting send_messages thread")
            sock_send.close()
            break

def message_handler():
    message_received_counter = 0
    while True:
        if not message_queue.empty():
            print(message_received_counter)
            # Get a job from the queue
            data, addr = message_queue.get()
            try:
                # print("Received Message:", data.decode(), "from", addr)
                message_received_counter+=1
                # print("190")
            except Exception:
                continue


def receive_messages():
    counter = 0
    while True:
        try:
            data, addr = sock_listen.recvfrom(1024)
            counter+=1
            print(counter)
            # print("Received Message:", data.decode(), "from", addr)
            # message_queue.put({data, addr})

        except KeyboardInterrupt:
            print("Exiting receive_messages thread")
            sock_listen.close()
            break                
        except Exception:
            pass

# Create and start threads for sending and receiving messages
send_thread = threading.Thread(target=send_messages, args=(udp_hosts, sending_udp_port))

for i in range(10):
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

message_handler_thread = threading.Thread(target= message_handler)

try:
    # message_handler_thread.start()
    # receive_thread.start()
    message_handler_thread.start()
    send_thread.start()
finally:
    # Join threads to wait for them to finish (this won't happen as they run indefinitely)
    send_thread.join()
    # receive_thread.join()
    # message_handler_thread.join()
