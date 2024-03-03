import socket
import time
import threading
import queue

sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

NUM_BEAMERS = 3
NUM_LEDS_PER_BEAMER = 6
NUM_TOTAL_LEDS = NUM_BEAMERS * NUM_LEDS_PER_BEAMER

def get_region_number(sequence):
    regions = [
        "000", 
        "001", "011", "010", "110", 
        "111", "101", "100", 
    ]

    try:
        return regions.index(sequence)
    except ValueError:
        return f"{sequence} is not a valid region"

THRESHOLD_VALUES = [8, 9, 11]
def region_to_threshold_region(region: str):
    ret = ""
    for i in range(3):
        # print("IN FOR LOOP", i, len(region))
        val = region[i]
        val = int(val)
        # print(i, val, THRESHOLD_VALUES[i])
        if val > THRESHOLD_VALUES[i]:
            ret += "1"
        else:
            ret += "0"
    return ret

def parse_message(message: str):
    values = message.split()

    if len(values) != NUM_TOTAL_LEDS:
        print("did not receive NUM_TOTAL_LEDS values, got: ", len(values))
        return

    beamer_regions = [region_to_threshold_region(values[i:i + NUM_LEDS_PER_BEAMER]) for i in range(0, len(values), NUM_LEDS_PER_BEAMER)]

    print(get_region_number(beamer_regions[0][0:3]), beamer_regions[0], values[0:NUM_LEDS_PER_BEAMER])


    
def receive_messages():
    print("in receiving messages")
    counter = 0
    while True:
        try:
            data, addr = sock_listen.recvfrom(1024)
            counter += 1
            # print("Received Message:", data.decode(), "from", addr)
            parse_message(data.decode())

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
