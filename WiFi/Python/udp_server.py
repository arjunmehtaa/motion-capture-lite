import socket
import time
import threading
import queue
from random import randint

sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

NUM_BEAMERS = 3
NUM_LEDS_PER_BEAMER = 4
NUM_TOTAL_LEDS = NUM_BEAMERS * NUM_LEDS_PER_BEAMER

from visualization import Visualization

vis = Visualization()

def get_region_number(sequence):
    regions = [
        "000", 
        "001", 
        "011",
        "010",
        "110", 
        "111",
        "101",
        "100", 
    ]
    regions = [
        "0000", "0001", 
        "0010", "0011",
        "0110", "0111",
        "0100", "0101",
        "1100", "1101",
        "1110", "1111",
        "1010", "1011",
        "1000", "1001"
    ]

    try:
        return regions.index(sequence)
    except ValueError:
        return f"{sequence} is not a valid region"

THRESHOLD_VALUES = [8, 9, 11, 6]
prev_four_value = 0
prev_four_state = "0"
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
    
    # 4th LED
    val4 = int(region[3])
    # print("HERE 1", val4)
    global prev_four_value
    global prev_four_state

    print("PREV VAL:", prev_four_value, val4)
    if val4 - prev_four_value < -1:
        ret += "0"
        prev_four_value = val4
    elif val4 - prev_four_value > 1:
        ret += "1"
        prev_four_value = val4
    else:
        ret += prev_four_state
    print("HERE 2")
    prev_four_state = ret[-1]
    print("HERE!")

    return ret

def parse_message(message: str):
    values = message.split()

    if len(values) != NUM_TOTAL_LEDS:
        print("did not receive NUM_TOTAL_LEDS values, got: ", len(values))
        return

    # beamer_regions = [region_to_threshold_region(values[i:i + NUM_LEDS_PER_BEAMER]) for i in range(0, len(values), NUM_LEDS_PER_BEAMER)]
    beamer_regions = [region_to_threshold_region(values[0:NUM_LEDS_PER_BEAMER])]

    x = get_region_number(beamer_regions[0][0:4])
    print("HELLO: ", x, beamer_regions[0], values[0:NUM_LEDS_PER_BEAMER])

    # print("Calling update on vis", vis)
    vis.update(x, 1, 1)

    
def receive_messages():
    # print("in receiving messages")
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
    # vis = Visualization()
    # print out my IP
