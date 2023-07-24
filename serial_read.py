import serial
import sys

def read_from_microcontroller(port, baud_rate):
    ser = None
    try:
        # Open the serial connection
        ser = serial.Serial(port, baud_rate)
        
        print(f"Reading from microcontroller on {port}...")

        # Read data until user interrupts the program (Ctrl+C)
        while True:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")

    except KeyboardInterrupt:
        print("\nSerial communication stopped by the user.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    # Replace '/dev/ttyACM0' with the appropriate port name for your microcontroller
    # The baud rate should match the one set in the microcontroller (e.g., Arduino IDE's Serial.begin())
    # get port from paramater
    if len(sys.argv) != 3:
        print("Wrong Format!")
        sys.exit(1)

    serial_port = sys.argv[1]
    baud_rate = int(sys.argv[2])

    read_from_microcontroller(port=serial_port, baud_rate=9600)