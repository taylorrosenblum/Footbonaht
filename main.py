import serial
import time
import pandas as pd
import random

# parameters
num_targets = 3
serial_port = '/dev/cu.usbmodem143101'  # Change this to match the port where your Arduino is connected
baud_rate = 9600  # Adjust baud rate as needed
scanTime = 20  # seconds
scanData = []
threshold = 10

# dataframe for game data
game_data = pd.DataFrame(columns=['round',
                                  'elapsed',
                                  'ch0',
                                  'ch1',
                                  'ch2']
                         )

def scan(round):
    # Gather data and return result of a single round
    #   Continuously request current reading of all piezo elements from Arduino
    #   If any reading exceeds threshold before scan time has elapsed, stop scanning
    #   and return ID of panel where strike was detected
    #   If no strike was detected pass a "-1" for struck panel
    #   Gather round data for testing purposes and return as pandas dataframe

    round_count = []
    readings = []
    elapsed = []
    start_time = time.time()
    scan_on = True
    struck_panel = -1

    # Initialize serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=0.01)

    while scan_on:
        ser.write(b'REQUEST\n')  # Send request command
        response = ser.readline().decode().strip()
        if response:
            t = time.time() - start_time
            values = [int(x) for x in response.split(',')]
            elapsed.append(t)
            readings.append(values)
            round_count.append(round)
            print("Elapsed Time: {:.2f} | "
                  "Ch0: {:.2f} | "
                  "Ch1: {:.2f} | "
                  "Ch2: {:.2f}".format(t, values[0], values[1], values[2]),
                  end='\r')
            if max(values) > threshold:
                scan_on = False
                struck_panel = values.index(max(values))
            if time.time() - start_time > scanTime:
                scan_on = False
                struck_panel = -1
    ser.close()  # Close serial port

    # slice data in to individual channels
    ch0 = []
    ch1 = []
    ch2 = []
    for row in readings:
        row = list(row)
        ch0.append(int(row[0]))
        ch1.append(int(row[1]))
        ch2.append(int(row[2]))
    # Process data as needed
    df = pd.DataFrame({'round': round_count,
                       'elapsed': elapsed,
                       'ch0': ch0,
                       'ch1': ch1,
                       'ch2': ch2})
    return df, struck_panel


# game setup
game_on = False
round = 0
user_input = input("Press any key and return to play...")

# allow user to initialize game
if user_input:
    game_on = True

# main game loop
while game_on:

    # Generate a random number between 0 and 2
    selected_target = random.randint(0, num_targets - 1)
    print("Strike panel {}!".format(selected_target))

    # Scan sensor elements on targets for strike
    round_data, struck_panel = scan(round)
    game_data = pd.concat([game_data, round_data], ignore_index=True)
    game_data.to_csv('game_data.csv')

    if struck_panel == -1:  # no strike registered
        print("\nNo strike detected!")
        game_on = False
    else:  # strike detected
        print("\nPanel {} was struck!".format(struck_panel))
        if struck_panel == selected_target:
            print("Target hit!")
        else:
            print("Target Missed!")

    round += 1