import socket
import time
import threading
import queue
from random import randint
import math
from typing import List

sock_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listening_udp_port = 5000
counter = 1

sock_listen.bind(("", listening_udp_port))
sock_listen.setblocking(False)

NUM_BEAMERS = 5
NUM_LEDS_PER_BEAMER = 4
NUM_TOTAL_LEDS = NUM_BEAMERS * NUM_LEDS_PER_BEAMER

prev_region = [-1, -1, -1]
def get_region_number(sequence, beamer_id: int):
    regions = [
        "0000", "0001", # 0, 1
        "0010", "0011", # 2, 3
        "0110", "0111", # 4, 5
        "0100", "0101", # 6, 7
        "1100", "1101", # 8, 9
        "1110", "1111", # 10, 11
        "1010", "1011", # 12, 13
        "1000", "1001"  # 14, 15
    ]

    try:
        rnum = regions.index(sequence)
        # if rnum == 0 and prev_region[beamer_id] >= 10:
        #     rnum = 15
        # prev_region[beamer_id] = rnum
        return rnum
    except ValueError:
        return f"{sequence} is not a valid region"

THRESHOLD_VALUES = [
        [4, 6, 9, 6],
        [7, 6, 6, 6],
        [3, 6, 6, 6],
        [3, 6, 6, 6],
    ]
prev_four_value = [0, 0, 0, 0, 0]
prev_four_state = ["0", "0", "0", "0", "0"]
def adc_to_binary(region: List[str], beamer_id: int):
    """
    Converting ADC array to binary 
    (["8", "20", "8"] -> "010")
    """
    ret = ""
    for i in range(3):
        val = region[i]
        val = int(val)
        if val > THRESHOLD_VALUES[beamer_id][i]:
            ret += "1"
        else:
            ret += "0"
    
    # 4th LED
    val4 = int(region[3])
    global prev_four_value
    global prev_four_state

    if val4 - prev_four_value[beamer_id] < -1:
        ret += "0"
        prev_four_value[beamer_id] = val4
    elif val4 - prev_four_value[beamer_id] > 1:
        ret += "1"
        prev_four_value[beamer_id] = val4
    else:
        ret += prev_four_state[beamer_id]
    prev_four_state[beamer_id] = ret[-1]

    return ret

def parse_message(message: str, beamer_id: int):
    values = message.split()

    if len(values) != NUM_TOTAL_LEDS:
        print("did not receive NUM_TOTAL_LEDS values, got: ", len(values))
        return

    try: 
        beamer_values = [values[i:i + NUM_LEDS_PER_BEAMER] for i in range(0, len(values), NUM_LEDS_PER_BEAMER)]
    except Exception as e:
        print("Exception 0: ", e)

    print("Values for {}:        {}".format(beamer_id, beamer_values[beamer_id]))
    print("Threshold for {}:     {}".format(beamer_id, THRESHOLD_VALUES[beamer_id]))
    
    try:
        beamer_regions = [adc_to_binary(beamer_values[i], i) for i in range(NUM_BEAMERS)]
    except Exception as e:
        print("Exception 1: ", e)

    print("Beamer Region for {}: {}".format(beamer_id, beamer_regions[beamer_id]))

    try:

        b1 = get_region_number(beamer_regions[0][0:4], 0)
        b2 = get_region_number(beamer_regions[1][0:4], 1)
        b3 = get_region_number(beamer_regions[2][0:4], 2)
        b4 = get_region_number(beamer_regions[3][0:4], 2)

        # b2 = max(min(b2, b1 - 3), 0)

        # b1a = get_angle_from_region(b1)
        # b2a = get_angle_from_region(b2)

        # print("Regions:", b1, b2, b3)
        # print("MIN:", min(b1, b2))
        # print("MAX:", max(b1, b2))

        # x: use b1/b2 closest to 8
        x = -1
        # if abs(b1 - 8) < abs(b2 - 8):
        #     x = b1
        # else:
        #     x = b2

        s = (sum())
        print("x:", x, "-", b1, b2)

        # x: use b3/b4 closest to 8
        y = -1
        if abs(b3 - 8) < abs(b4 - 8):
            y = b3
        else:
            y = b4
        print("y:", y, "-", b3, b4)

        int_vals = [int(val) for val in values]
        print(max(int_vals))
        z = max(int_vals) // 10
        print("z:", z)

        # x, y = compute_xy_coordinates(180 - b1a, b2a, Point(0, 0, 0), Point(5, 0, 0))
        # print("Positions: ", b1, y)
        print()
        vis.update(x, y, 1)
    except Exception as e:
        print("Exception 2:", e)
        print()
        pass



    
def receive_messages(beamer_id: int):
    counter = 0
    while True:
        try:
            data, addr = sock_listen.recvfrom(1024)
            counter += 1
            # print("Received Message:", data.decode(), "from", addr)
            parse_message(data.decode(), beamer_id=beamer_id)

            # message_queue.put({data, addr})
        except KeyboardInterrupt:
            print("Exiting receive_messages thread")
            sock_listen.close()
            break
        except Exception as e:
            # print(e)
            pass


if __name__ == "__main__":
    beamer_id = input("Enter beamer id: ")

    print(sock_listen.getsockname())
    receive_messages(beamer_id=beamer_id)

