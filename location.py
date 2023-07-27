from model.point import Point
from utils.constants import Mode

import argparse
import math
import serial

from typing import List


def get_tag_location(
    beamer_angles: List[float], beamer_positions: List[Point], mode: Mode = Mode.TWO_D
):
    """
    Computes the location of the tag

    beamer_angles       : list of angles of incidence of beamers (degrees)
    beamer_positions    : list of positions of beamers (List[Point])
    """

    # Check if data is valid
    if len(beamer_angles) < 2:
        print("Data from atleast 2 beamers required. Aborting...")
        return

    # Extract angles of known beamers
    angle_b1 = beamer_angles[0]
    angle_b2 = beamer_angles[1]

    # Extract positions of known beamers
    pos_b1: Point = beamer_positions[0]
    pos_b2: Point = beamer_positions[1]

    # Compute the two possible solutions
    res1 = compute_xy_coordinates(angle_b1, angle_b2, pos_b1, pos_b2)
    res2 = compute_xy_coordinates(angle_b2, angle_b1, pos_b2, pos_b1)

    # res = eliminate(res1, res2) TODO: implement error correction
    # We are getting two (or more) possible solutions.
    # We need to find the most likely correct solution.

    if mode == Mode.TWO_D:
        return [res1, res2]

    if mode == Mode.THREE_D:
        pos_b3 = beamer_positions[
            2
        ]  # TODO: right now, we only have 3 beamers. 1 and 2 are on one plane, 3 is on another.
        z1 = compute_z_coordinate(res1, pos_b3, angle_b1, True)
        z2 = compute_z_coordinate(res2, pos_b3, angle_b1, True)

        return [Point(res1[0], res1[1], z1), Point(res2[0], res2[1], z2)]


def compute_xy_coordinates(angle_b1, angle_b2, pos_b1: Point, pos_b2: Point):
    """
    Computes x and y coordinates of tag
    Refer to https://math.stackexchange.com/questions/1725790/calculate-third-point-of-triangle-from-two-points-and-angles

    angle_b1  : incidence angle of beamer 1 (degrees)
    angle_b2  : incidence angle of beamer 2 (degrees)
    pos_b1    : position of beamer 1
    pos_b2    : position of beamer 2
    """

    # Extract coordinates of known points
    x1, y1, _ = pos_b1.get()
    x2, y2, _ = pos_b2.get()

    # Compute x and y offset
    u = x2 - x1
    v = y2 - y1

    # Compute distance between given points
    distance = math.sqrt(u**2 + v**2)

    # Convert angles to radians and find 3rd angle
    a1 = math.radians(angle_b1)
    a2 = math.radians(angle_b2)
    a3 = math.pi - a1 - a2

    # Set up equations
    l = distance * (math.sin(a2) / math.sin(a3))
    eq1 = (x1 * u) + (y1 * v) + (l * distance * math.cos(a1))
    eq2 = (y2 * u) - (x2 * v) - (l * distance * math.sin(a1))

    # Calculate coordinates of third point
    x3 = (1 / distance**2) * ((u * eq1) - (v * eq2))
    y3 = (1 / distance**2) * ((v * eq1) + (u * eq2))

    return (x3, y3)


def compute_z_coordinate(
    tag_coordinates: Point, beamer_coordinates: Point, angle: float, is_tag_below: bool
):
    """
    Computes z coordinate of tag

    tag_coordinates     : coordinates of tag
    beamer_coordinates  : coordinates of beamer
    angle               : angle of inclination/declination of tag wrt beamer (degrees)
    is_tag_below        : True if tag is below beamer, False otherwise
    """

    # Extract coordinates of tag
    x, y, _ = tag_coordinates.get()

    # Extract coordinates of beamer
    x_b, y_b, z_b = beamer_coordinates.get()

    # Convert angle to radians
    a = math.radians(angle)

    # Calculate x and y offset
    u = x_b - x
    v = y_b - y

    # Calculate xy offset
    d = math.sqrt(u**2 + v**2)

    # Calculate perpendicular
    p = math.tan(a) * d

    # Calculate z offset
    if is_tag_below:
        ans = z_b - p
    else:
        ans = z_b + p

    return ans


def compute_z_axis_resolution(alpha: float, d: float, p: float):
    """
    Computes z-axis resolution of tag

    alpha   : angular resolution of projector
    d       : baseline between projectors
    p       : depth
    """

    res = alpha * (d**2 + p**2) / (d - (alpha * p))
    return res


## Testing

## Test get_tag_location() for 2D
# print(get_tag_location([30, 30], [Point(5,2), Point(2,3)]))

## Test calculate_z_coordinate()
# tag_coordinate_1 = Point(0, 1)
# beamer_coordinate_1 = Point(3, 4, 10)
# print(calculate_z_coordinate(tag_coordinate_1, beamer_coordinate_1, 30, True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read data from microcontroller.')
    parser.add_argument('--port', type=str, help='Serial port of the microcontroller (e.g., COM5 or /dev/ttyUSB1)')
    parser.add_argument('--baud_rate', type=int, default=9600, help='Baud rate for serial communication (default: 9600)')
    args = parser.parse_args()
    port = args.port
    baud_rate = args.baud_rate

    if args.port:
        try:
            # Open the serial connection
            current_input = ''
            ser = serial.Serial(port, baud_rate)

            print(f"Reading from microcontroller on {port}...")

            # Read data until user interrupts the program (Ctrl+C)
            while True:
                data = ser.readline().strip()
                try:
                    decoded_data = data.decode('utf-8').strip()
                    if decoded_data == 'x':  # terminate tag's input
                        # don't know beamer positions
                        print(get_tag_location(current_input.split(''), []))
                        current_input = ''
                    elif decoded_data is not None:
                        current_input += decoded_data
                    print(current_input)
                except UnicodeDecodeError:
                    # decoding failed
                    continue

        except KeyboardInterrupt:
            print("\nSerial communication stopped by the user.")
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        finally:
            if ser.is_open:
                ser.close()
    else:
        print("Please provide the serial port with --port argument.")