"""Simple Python script to set an alarm for a specific time.
   When the alarm goes off, a random string will be shown.
   The possible Strings are taken from "alarm_names.txt"
   the alarm produces a sound on a Mac until the mouse is moved or clicked
   when the mouse is only moved the alarm clock goes snoozing for 10 seconds
   when the mouse is pressed the alarm stops
"""

import datetime
import os
import time
import random
from pynput import mouse

# global variables moved and pressed for mouse actions
moved = False
pressed = False

# Sets global variable moved = true if mouse has been moved
def on_mouse_move(mouse_position_x, mouse_position_y):
    global moved
    moved = True

# Sets global variable pressed = true if mouse has been clicked
def on_mouse_click(mouse_position_x, mouse_position_y, button, is_pressed):
  global pressed
  if is_pressed:
    pressed = True

# create a listener and setup call backs
mouse_listener = mouse.Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click)


# If video URL file does not exist, create one
if not os.path.isfile("alarm_names.txt"):
	print('Creating "alarm_names.txt"...')
	with open("alarm_names.txt", "w") as alarm_file:
		alarm_file.write("Sleepy Head")

def check_alarm_input(alarm_time):
	# Check for valid alarm time input
	if len(alarm_time) == 1: # [Hour] Format
		if alarm_time[0] < 24 and alarm_time[0] >= 0:
			return True
	if len(alarm_time) == 2: # [Hour:Minute] Format
		if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
		   alarm_time[1] < 60 and alarm_time[1] >= 0:
			return True
	elif len(alarm_time) == 3: # [Hour:Minute:Second] Format
		if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
		   alarm_time[1] < 60 and alarm_time[1] >= 0 and \
		   alarm_time[2] < 60 and alarm_time[2] >= 0:
			return True
	return False

# Get user input for the alarm time
print("Set a time for the alarm (Ex. 06:30 or 18:30:00)")
while True:
	alarm_input = input(">> ")
	try:
		alarm_time = [int(n) for n in alarm_input.split(":")]
		if check_alarm_input(alarm_time):
			break
		else:
			raise ValueError
	except ValueError:
		print("ERROR: Enter time in HH:MM or HH:MM:SS format")

# Convert the alarm time from [H:M] or [H:M:S] to seconds
seconds_hms = [3600, 60, 1] # Number of seconds in an Hour, Minute, and Second
alarm_seconds = sum([a*b for a,b in zip(seconds_hms[:len(alarm_time)], alarm_time)])

# Get the current time of day in seconds
now = datetime.datetime.now()
current_time_seconds = sum([a*b for a,b in zip(seconds_hms, [now.hour, now.minute, now.second])])

# Calculate the number of seconds until alarm goes off
time_diff_seconds = alarm_seconds - current_time_seconds

# If time difference is negative, set alarm for next day
if time_diff_seconds < 0:
	time_diff_seconds += 86400 # number of seconds in a day

# Display the amount of time until the alarm goes off
print("Alarm set to go off in %s" % datetime.timedelta(seconds=time_diff_seconds))

# Sleep until the alarm goes off
time.sleep(time_diff_seconds)

# Time for the alarm to go off

# Load list of possible video URLs
with open("alarm_names.txt", "r") as alarm_file:
	alarmNames = alarm_file.readlines()

snooze = 10
# Open a random string from the list
print("Wake Up! You ",random.choice(alarmNames))
print("(or move mouse for snoozing",snooze,"seconds)")
pressed = False
moved = False

mouse_listener.start()

while True:
    # command to play sound on mac
    os.system('afplay /System/Library/Sounds/Funk.aiff')
    if pressed:
        print("Good Morning!!!!")
        break
    if moved:
        print("Snoozed!")
        moved = False
        time.sleep(snooze)


mouse_listener.stop()
mouse_listener.join()

