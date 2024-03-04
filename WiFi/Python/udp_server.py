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

NUM_BEAMERS = 4
NUM_LEDS_PER_BEAMER = 4
NUM_TOTAL_LEDS = NUM_BEAMERS * NUM_LEDS_PER_BEAMER

from visualization import Visualization
vis = Visualization()

prev_region = [-1] * NUM_BEAMERS
def get_region_number(sequence, beamer_id: int):
    regions = {
    "0000": 0, "0001": 1,
    "0010": 2, "0011": 3,
    "0110": 4, "0111": 5,
    "0100": 6, "0101": 7,
    "1100": 8, "1101": 9,
    "1110": 10, "1111": 11,
    "1010": 12, "1011": 13,
    "1000": 14, "1001": 15
    }

    try:
        rnum = regions[sequence]
        if rnum == 0 and prev_region[beamer_id] >= 10:
            rnum = 15
        else:
            prev_region[beamer_id] = rnum
        return rnum
    except ValueError:
        return f"{sequence} is not a valid region"

THRESHOLD_VALUES = [
        [7, 7, 10, 6], #b0
        [7, 7, 12, 6], #b1
        [7, 7, 12, 6], #b2
        [7, 7, 10, 6], #b3
        [3, 6, 6, 6],
    ]

prev_four_value = [0] * NUM_BEAMERS
prev_four_state = ["0"] * NUM_BEAMERS
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
    global prev_four_value
    global prev_four_state
    
    val4 = int(region[3])
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

def parse_message(message: str):
    values = message.split()
    values = [int(val) for val in values]

    if len(values) != NUM_TOTAL_LEDS:
        print("did not receive NUM_TOTAL_LEDS values, got: ", len(values))
        return

    try:
        beamer_values = [values[i:i + NUM_LEDS_PER_BEAMER] for i in range(0, len(values), NUM_LEDS_PER_BEAMER)]
    except Exception as e:
        print("Exception 0: ", e)

    beamer_regions = []
    for i in range(0, NUM_BEAMERS):
        try:
            beamer_regions.append(adc_to_binary(beamer_values[i], i))
        except Exception as e:
            print("Exception 1: ", e, i, i + NUM_LEDS_PER_BEAMER, len(values))
    
    try:
        beamer_rnum = [get_region_number(beamer_regions[i], i) for i in range(NUM_BEAMERS)]
    except Exception as e:
        print("Exception 2: ", e)


    #### x ####
    x_beamers = [1, 2]
    x = -1
    # print("x_beamers:", x_beamers)
    # for i in x_beamers:
    #     print(f"B{i} Threshold:     ", THRESHOLD_VALUES[i])
    #     print(f"B{i} Values:        ", beamer_values[i])
    #     print(f"B{i} Region Number: ", beamer_rnum[i])
    #     print()

    x = -1
    if sum(beamer_values[1]) > sum(beamer_values[2]):
        x = beamer_rnum[1]
    else:
        x = beamer_rnum[2]
    # print("x:", y)
    print()
    

    y_beamers = [0, 3]
    # print("y_beamers:", y_beamers)
    # for i in y_beamers:
    #     print(f"B{i} Threshold:     ", THRESHOLD_VALUES[i])
    #     print(f"B{i} Values:        ", beamer_values[i])
    #     print(f"B{i} Region Number: ", beamer_rnum[i])
    #     print()

    # set y to whichever beamer region number has highest beamer_values
    y = -1
    if sum(beamer_values[0]) > sum(beamer_values[3]):
        y = beamer_rnum[0]
    else:
        y = beamer_rnum[3]
    # print("y:", y)

    int_vals = [int(val) for val in values]
    z = max(int_vals) // 10
    # print("z:", z)
    print("(x, y, z): ", x, y, z, time.time())

    # x, y = compute_xy_coordinates(180 - b1a, b2a, Point(0, 0, 0), Point(5, 0, 0))
    # print("Positions: ", b1, y)
    print()
    vis.update(x, y, 1)

def receive_messages():
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
        except Exception as e:
            # print(e)
            pass


if __name__ == "__main__":
    print(sock_listen.getsockname())
    receive_messages()

    # for i in range(0, 16):
    #     for j in range(0, 16):
    #         if j >= i:
    #             continue
    #         print(f"{i} - {j}: {compute_xy_coordinates(180 - get_angle_from_region(i), get_angle_from_region(j), Point(0, 0, 0), Point(15, 0, 0))}")
    #         print()
