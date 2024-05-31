import serial
import time

# Open grbl serial port ==> CHANGE THIS BELOW TO MATCH YOUR USB LOCATION
s = serial.Serial('/dev/ttyUSB0',115200) # GRBL operates at 115200 baud. Leave that part alone.
      
# Open g-code file
#f = open('rectangleTest.gcode','r');
f = open('gcode/home.gcode','r');
#f = open('homing.gcode','r');
#f = open('change_setting.gcode','r');


# Wake up grb5

settings = False;
if settings:
    f = open('gcode/grbl_config.gcode','r');

s.write(("\r\n\r\n").encode('utf-8'))
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

def wait_for_idle(s):
    """Wait until the GRBL controller is idle."""
    while True:
        s.write(b'?')
        status = s.readline().strip().decode('utf-8')
        if 'Idle' in status:
            return
        time.sleep(0.1)  # Wait a bit before checking again

# Stream g-code to grbl
for line in f:
	l = line.strip() # Strip all EOL characters for consistency
	print('Sending: ' + l)
	s.write((l + '\n').encode('utf-8')) # Send g-code block to grbl
	grbl_out = s.readline() # Wait for grbl response with carriage return
	print(' : ' + str(grbl_out.strip()))
	
	if not settings:
	    wait_for_idle(s)

# Close file and serial port
print("DONE")
f.close()
s.close()
