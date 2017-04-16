#! python3
"""
pretty_stopwatch.py - A simple, prettified, stopwatch program.
"""

import time
import pyperclip


# Display the program's instructions.
print('Press ENTER to begin. afterwards, press ENTER to "click" the stopwatch. Press Ctrl-C to quit.')
input()     # press Enter to begin
print('Started.')
startTime = time.time()     # get the first lap's start time
lastTime = startTime
lapNum = 1

# start tracking the lap times.
output_strings = []
try:
    while True:
        input()
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        time_string = 'Lap #{:02}: {:>10.2f}'.format(lapNum, totalTime) + ' ({:>.2f})'.format(lapTime).rjust(10)
        output_strings.append(time_string)
        print(time_string)
        lapNum += 1
        lastTime = time.time()  # reset the last lap time
except KeyboardInterrupt:
    # Handle the Ctrl-C exception to keep its error message from displaying.
    print('\n\nYour results!')
    for item in output_strings:
        print(item)
    pyperclip.copy('\n'.join(output_strings))
    print('\nDone.')
