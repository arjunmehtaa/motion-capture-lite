import socket
import time
import threading

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_hosts = ["192.168.132.11", "192.168.132.12"]
sending_udp_port = 4210
listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

def send_messages(udp_hosts, sending_udp_port):
    counter = 0
    while True:
        try:

            msg = "Hello from Python: " + str(counter)
            for udp_host in udp_hosts:
                sock_send.sendto(msg.encode(), (udp_host, sending_udp_port))
            counter += 1
        except KeyboardInterrupt:
            print("Exiting send_messages thread")
            sock_send.close()
            break

def receive_messages():
    while True:
        try:
            data, addr = sock_listen.recvfrom(1024)
            print("Received Message:", data.decode(), "from", addr)
        except KeyboardInterrupt:
            print("Exiting receive_messages thread")
            sock_listen.close()
            break                
        except Exception:
            pass

# Create and start threads for sending and receiving messages
send_thread = threading.Thread(target=send_messages, args=(udp_hosts, sending_udp_port))
receive_thread = threading.Thread(target=receive_messages)

send_thread.start()
receive_thread.start()

# Join threads to wait for them to finish (this won't happen as they run indefinitely)
send_thread.join()
receive_thread.join()

# while True:
#     # Send message to all Arduinos
#     print("Waiting for client...")
#     msg = "Hello from Python: " + str(counter)
#     for udp_host in udp_hosts:
#         sock_send.sendto(msg.encode(), (udp_host, sending_udp_port))
#     counter += 1

#     time.sleep(0.1)

#     # Receive messages from Arduinos
#     for _ in range(len(udp_hosts)):
#         try:
#             data, addr = sock_listen.recvfrom(1024)
#             print("Received Messages:", data, " from", addr)
#         except socket.error as e:
#             print("Error while listening Arduino package: ", e)
