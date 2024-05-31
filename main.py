# This is the main python script that controls Rob Ross
# It should control the screen, microphone and send the Gcode

import serial
import time
import screen_controller
import pigpio
import subprocess

class RunningAverage:
	def __init__(self, buffer_size=100, initial_value=1):
		self.buffer_size = buffer_size
		self.buffer = [initial_value] * buffer_size  # Fixed-size buffer initialized with 1s
		self.index = 0  # Current index in the buffer
		self.total = initial_value * buffer_size  # Initial total sum of the buffer

	def add_value(self, value):
		# Subtract the oldest value from the total and add the new value
		self.total -= self.buffer[self.index]
		self.total += value
		# Replace the oldest value with the new value in the buffer
		self.buffer[self.index] = value
		# Move to the next index, wrapping around if necessary
		self.index = (self.index + 1) % self.buffer_size

	def get_average(self):
		# Compute and return the running average
		return self.total / self.buffer_size

### Startup
# Turn on screen
screen_controller.screen_controller_start()

# Turn on microphone
try:
	subprocess.run(["sudo", "pigpiod"], check=True)
	time.sleep(2)
except subprocess.CalledProcessError as e:
	print(f"Failed to start pigpiod: {e}")
	exit()

mic1_pin = 23
mic2_pin = 24

pi = pigpio.pi()

pi.set_mode(mic1_pin, pigpio.INPUT)
pi.set_pull_up_down(mic1_pin, pigpio.PUD_DOWN)

pi.set_mode(mic2_pin, pigpio.INPUT)
pi.set_pull_up_down(mic2_pin, pigpio.PUD_DOWN)

if not pi.connected:
	print("Mic not connected :(")
else:
	print("Mic is connected! :)")

mic1_avg = RunningAverage()
mic2_avg = RunningAverage()

# Turn on drawingbot
s = serial.Serial('/dev/ttyUSB0',115200) # GRBL operates at 115200 baud. Leave that part alone.
gcode = open('home.gcode', 'r')

s.write(("\r\n\r\n").encode('utf-8'))
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

time.sleep(3)

### Main loop

"""
while true:
	read mic
		running average	

	change face
		animation?
		multiple faces?

	check too loud
		move servo?
		change face

	send g code if not idle
"""
head_direction = 90 # ToDo
current_face = 1
mode = "working"
g_code_line = 0

def read_mic():
	# Read the microphones
	# Set the mode according to running average
	# Set which direction the robot should move its head

	mic1_avg.add_value(pi.read(mic1_pin))
	mic2_avg.add_value(pi.read(mic2_pin))
	
	print("Mic 1: " + str(mic1_avg.get_average()) + "      Mic 2: " +  str(mic2_avg.get_average()))

	"""
	if(mic1_avg.get_average() < 0.9 or mic1_avg.get_average() < 0.9):
		print("Helo")
	"""
	

	robot_mode = "working"
	head_dir = 90

	return robot_mode, head_dir

def control_face(mode):
	# Set the face according to mode
	
	current_face = screen_controller.set_face(current_face, mode)
	
	return current_face

def play_angry_robot():
	# Pauses robross
	# Changes the face to angry
	# Moves the servo
	# Waits a bit (5 seconds)
	# Continue robross
	# Done
	
    pass

def wait_for_idle(s):
	"""Wait until the GRBL controller is idle."""
	s.write(b'?')
	status = s.readline().strip().decode('utf-8')
	if 'Idle' in status:
		return True
	else:
		return False

keep_working = True
while keep_working:
	mode, head_direction = read_mic() # Sets current working mode
	
	current_face = control_face(mode) # Controls face
	
	if mode == "loud":
		# Robot gets angry and stops working
		play_angry_robot()
	else:
		# Continue working
		if wait_for_idle(s):
			line = gcode[g_code_line]

			l = line.strip() # Strip all EOL characters for consistency
			print('Sending: ' + l)
			s.write((l + '\n').encode('utf-8')) # Send g-code block to grbl
			grbl_out = s.readline() # Wait for grbl response with carriage return
			print(' : ' + str(grbl_out.strip()))
			
			g_code_line += 1
	
	time.sleep(0.01)

### Shutting down
print("Shutting down")
screen_controller.screen_shutdown()
subprocess.run(["sudo", "killall", "pigpiod"], check=True)
gcode.close()
s.close()
time.sleep(2)  # Wait a bit for the daemon to shut down
