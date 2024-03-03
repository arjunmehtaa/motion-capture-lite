import socket
import time
import threading
import queue
from random import randint
import math

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

class Point:
    def __init__(self, x = None, y = None, z = None):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return (self.x, self.y, self.z)
    
def compute_xy_coordinates(angle_b1, angle_b2, pos_b1: Point, pos_b2: Point):
    """
    Computes x and y coordinates of tag
    Refer to https://math.stackexchange.com/questions/1725790/calculate-third-point-of-triangle-from-two-points-and-angles

    angle_b1  : incidence angle of beamer 1 (degrees)
    angle_b2  : incidence angle of beamer 2 (degrees)
    pos_b1    : position of beamer 1 
    pos_b2    : position of beamer 2
    """
    print("Angles: ", angle_b1, angle_b2)

    # Extract coordinates of known points
    x1, y1, _ = pos_b1.get()
    x2, y2, _ = pos_b2.get()

    # Compute x and y offset
    u = x2 - x1
    v = y2 - y1

    # Compute distance between given points
    distance = math.sqrt(u**2 + v**2)
    print("Distance:", distance)

    # Convert angles to radians and find 3rd angle
    a1 = math.radians(angle_b1)
    a2 = math.radians(angle_b2)
    a3 = math.pi - a1 - a2
    print("Third Angle:", a3*57.2974693618)

    # Set up equations
    l = distance * (math.sin(a2) / math.sin(a3))
    eq1 = (x1 * u) + (y1 * v) + (l * distance * math.cos(a1))
    eq2 = (y2 * u) - (x2 * v) - (l * distance * math.sin(a1))

    # Calculate coordinates of third point
    x3 = (1 / distance**2) * ((u * eq1) - (v * eq2))
    y3 = (1 / distance**2) * ((v * eq1) + (u * eq2))

    return (x3, y3)


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

THRESHOLD_VALUES = [
        [8, 9, 11, 6],
        [6, 6, 6 , 6],
        [0, 0, 0, 0]
    ]
prev_four_value = [0, 0, 0]
prev_four_state = ["0", "0", "0"]
def adc_to_binary(region: str, beamer_id: int):
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

TOTAL_REGIONS = 2 ** NUM_LEDS_PER_BEAMER
def get_angle_from_region(region_num: int):
    if not (region_num >= 0 and region_num < TOTAL_REGIONS):
        print("WRONG REGION NUM", region_num)
    return (130 / TOTAL_REGIONS) * region_num + 4

def parse_message(message: str):
    values = message.split()

    if len(values) != NUM_TOTAL_LEDS:
        print("did not receive NUM_TOTAL_LEDS values, got: ", len(values))
        return

    beamer_regions = []
    for i in range(0, len(values), NUM_LEDS_PER_BEAMER):
        try:
            beamer_regions.append(adc_to_binary(values[i:i + NUM_LEDS_PER_BEAMER], i // NUM_LEDS_PER_BEAMER))
        except Exception as e:
            print("Exception 1: ", e)
    print("Beamer 1:", values[0:4])
    print("Beamer 2:", values[4:8])

    try:

        b1 = get_region_number(beamer_regions[0][0:4])
        b2 = get_region_number(beamer_regions[1][0:4])

        b1a = get_angle_from_region(b1)
        b2a = get_angle_from_region(b2)

        print("Regions:", b1, b2)

        x, y = compute_xy_coordinates(180 - (b1a + 25), (b2a + 25), Point(0, 0, 0), Point(5, 0, 0))
        print("Positions: ", x, y)
    except Exception as e:
        print("Exception 2:", e)
        pass

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
    # vis = Visualization()
    # print out my IP
