import serial

def read_from_microcontroller(port, baud_rate):
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
        if ser.is_open:
            ser.close()

if __name__ == "__main__":
    # Replace '/dev/ttyACM0' with the appropriate port name for your microcontroller
    # The baud rate should match the one set in the microcontroller (e.g., Arduino IDE's Serial.begin())
    read_from_microcontroller(port='/dev/ttyUSB1', baud_rate=9600)