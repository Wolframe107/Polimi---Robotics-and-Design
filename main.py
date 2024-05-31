
import serial
import time
import screen_controller
import pigpio
import subprocess
import runningAverage
import random
import os

os.chdir('/home/pi/Desktop/RobRoss')

####### Startup #######
# Turn on screen
screen_controller.screen_controller_start()

# Turn on microphone
""" Uncomment to turn on pigpiod daemon automatically
try:
	pi = pigpio.pi()
	subprocess.run(["sudo", "pigpiod"], check=True)
	time.sleep(2)
	
except subprocess.CalledProcessError as e:
	exit()
"""
try:
	# Set up microphones
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

	mic1_avg = runningAverage.RunningAverage()
	mic2_avg = runningAverage.RunningAverage()

	# Variables for head servo
	servo_pin = 12  # Replace with the correct GPIO pin
	min_pulsewidth = 500  # Minimum pulsewidth (in microseconds)
	max_pulsewidth = 2500  # Maximum pulsewidth (in microseconds)

	# Connect to MKS board
	s = serial.Serial('/dev/ttyUSB0',115200) # GRBL operates at 115200 baud. Leave that part alone.
	s.write(("\r\n\r\n").encode('utf-8'))
	time.sleep(2)   # Wait for grbl to initialize
	s.flushInput()  # Flush startup text in serial input

####### Homing #######
	def set_servo_angle(angle):
		# Moves the head to the specified angle
		pulsewidth = min_pulsewidth + (angle / 180.0) * (max_pulsewidth - min_pulsewidth)
		pi.set_servo_pulsewidth(12, pulsewidth)

	set_servo_angle(90) # Make sure head is facing the center
	screen_controller.set_face("homing")
	homing = open('gcode/homing.gcode', 'r')
	for line in homing:
		l = line.strip() # Strip all EOL characters for consistency
		print('Sending: ' + l)
		s.write((l + '\n').encode('utf-8')) # Send g-code block to grbl
		grbl_out = s.readline() # Wait for grbl response with carriage return
		print(' : ' + str(grbl_out.strip()))
	time.sleep(3)

####### Main loop #######
	def read_mic():
		# Read the microphones
		# Set the mode according to running average
		# Set which direction the robot should move its head
		
		mic1_avg.add_value(pi.read(mic1_pin))
		mic2_avg.add_value(pi.read(mic2_pin))
		
		mic1_avg_get = mic1_avg.get_average()
		mic2_avg_get = mic2_avg.get_average()

		#print("Mic 1: " + str(mic1_avg.get_average()) + "      Mic 2: " +  str(mic2_avg.get_average()))
		
		if(mic1_avg_get < 0.9 or mic2_avg_get < 0.9):
			robot_mode = "angry"
			
			if mic1_avg_get == mic2_avg_get:
				noise_dir = 90
			elif mic1_avg_get > mic2_avg_get:
				noise_dir = 45
			else:
				noise_dir = 135
				
		else:
			noise_dir = None
			robot_mode = "working"
		
		return robot_mode, noise_dir
			
	def play_angry_robot(frame, head):
		# Stops working and plays a little animation

		print(frame)
		still_angry = True
			
		if frame == 0:
			s.flushInput() 
			s.write(("M5" + '\n').encode('utf-8'))
			s.readline() 
			time.sleep(0.1)
			s.write(b'!')	
			
			if head:
				if head == 45:
					for angle in range(90,  45, -1):  # Sweep from 0 to 180 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
				else:
					for angle in range(90,  135, 1):  # Sweep from 0 to 180 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
				
		if frame == 250:
			if head:
				if head == 45:
					for angle in range(45,  135, 1):  # Sweep from 0 to 180 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
				elif head == 135:
					for angle in range(135, 45, -1):  # Sweep from 180 to 0 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
		
		if frame == 400:
			if head:
				if head == 45:
					for angle in range(135, 45, -1):  # Sweep from 180 to 0 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
				elif head == 135:
					for angle in range(45,  135, 1):  # Sweep from 0 to 180 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
		
		if frame == 500:
			if head:
				if head == 45:
					for angle in range(45,  90, 1):  # Sweep from 0 to 180 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
				elif head == 133:
					for angle in range(135, 90, -1):  # Sweep from 180 to 0 degrees
						set_servo_angle(angle)
						time.sleep(0.01)
			
			still_angry = False
			screen_controller.set_face("working")
			frame = -1
			s.write(b'~')
			time.sleep(0.3)
			set_servo_angle(90)
			s.write(("M3 S180" + '\n').encode('utf-8'))

		frame += 1
		return frame, still_angry
	
	def wait_for_idle(s):
		# Wait for the robot to be idle before sendning next command
		s.write(b'?')
		status = s.readline().strip().decode('utf-8')
		if 'Idle' in status:
			return True
		else:
			return False
	
	def erase_board():
		# Sends commands to erase the board
		gcode = open("gcode/erase.gcode", 'r')
		for line in gcode:
			l = line.strip() # Strip all EOL characters for consistency
			print('Sending: ' + l)
			s.write((l + '\n').encode('utf-8')) # Send g-code block to grbl
			grbl_out = s.readline() # Wait for grbl response with carriage return
			print(' : ' + str(grbl_out.strip()))
	
	# Some variables and pre-work settings
	s.write(b'~')
	keep_working = True
	screen_controller.set_face("working")
	head_direction = 90
	mode = "working"
	angry_frame = 0
	still_angry = False
	old_noise_dir = None
	current_gcode = 1
	gcode_path = "gcode/drawings/"
	gcode = open(gcode_path + "1.gcode", 'r')
	
	erase_board()
	
	# Main while loop
	while keep_working:
		new_mode, noise_dir = read_mic() # Sets current working mode
		
		if new_mode != mode: # When mode has changed
			if not still_angry:
				screen_controller.set_face(new_mode)
			if new_mode == "angry":
				still_angry = True
				
			mode = new_mode
		
		if still_angry:
			if noise_dir:
				old_noise_dir = noise_dir
				
			angry_frame, still_angry = play_angry_robot(angry_frame, old_noise_dir)
		else:
			# Continue working
			head_direction = 90

			if wait_for_idle(s):
				line = gcode.readline()
				
				if line == "": # End of gcode, pick a new thing to draw
					random_pick = random.randint(1,6)
					while random_pick == current_gcode:
						random_pick = random.randint(1,6)
					current_gcode = random_pick
					print("DRAWING " + str(current_gcode))
					gcode = open(gcode_path + str(current_gcode) + ".gcode", 'r')
					erase_board();
				else:
					l = line.strip()
					print('Sending: ' + l)
					s.write((l + '\n').encode('utf-8'))
					grbl_out = s.readline()
					print(' : ' + str(grbl_out.strip()))
					
		time.sleep(0.01)
		

### Shutting down
except KeyboardInterrupt:
	print("Shutting down")
	s.write(b'!')
	s.write(b'Ctrl-x')
	screen_controller.screen_shutdown()
	subprocess.run(["sudo", "killall", "pigpiod"], check=True)
	gcode.close()
	s.close()
	time.sleep(2)  # Wait a bit for the daemon to shut down
	print("DONE")
