import argparse
import serial
import time

# CLI arguments
args = []
# Serial port connection handle
arduino = None


def main():
    global args
    args = process_cli_arguments()
    init_connection()
    run_command(args.command)
    close_connection()


def process_cli_arguments():
    parser = argparse.ArgumentParser(description='Arduino Sensors CLI')
    parser.add_argument('command', type=str, help='Command to be executed',
                        choices=['temperature', 'humidity', 'pressure', 'lighting', 'ping'])
    parser.add_argument('--port', help='Example: (Windows: "COM1"); (Linux: "/dev/ttyACM0"). Default: /dev/ttyACM0',
                        type=str, default='/dev/ttyACM0')
    parser.add_argument('--baud-rate', help='Baud rate. Default: 115200', type=int, default=115200)
    parser.add_argument('--timeout', help='Connection timeout. Default: .1', type=float, default=.1)
    return parser.parse_args()


def init_connection():
    global args, arduino
    arduino = serial.Serial(args.port, args.baud_rate, timeout=args.timeout)
    time.sleep(1)  # give the connection a second to settle


def close_connection():
    global arduino
    arduino.close()


def run_command(command):
    {
        'temperature': temperature_command,
        'humidity': humidity_command,
        'pressure': pressure_command,
        'lighting': lighting_command,
        'ping': ping_command
    }[command]()


###
# Commands section
###
def temperature_command():
    send_and_wait(b'temperature')


def humidity_command():
    send_and_wait(b'humidity')


def pressure_command():
    send_and_wait(b'pressure')


def lighting_command():
    send_and_wait(b'lighting')


def ping_command():
    send_and_wait(b'ping')


def send_and_wait(command):
    global arduino
    while True:
        arduino.write(command)
        data = arduino.readline()[:-2]  # the last bit gets rid of the new-line chars
        if data:
            print(data.decode())
            return
        time.sleep(1)


if __name__ == '__main__':
    main()
