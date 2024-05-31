import pigpio
import time

# Connect to the pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    exit()

# Define the GPIO pin connected to the servo
servo_pin = 12  # Replace with the correct GPIO pin

# Define the pulsewidths for the servo
min_pulsewidth = 500  # Minimum pulsewidth (in microseconds)
max_pulsewidth = 2500  # Maximum pulsewidth (in microseconds)

# Function to set servo angle
def set_servo_angle(angle):
    # Convert the angle to a pulsewidth
    pulsewidth = min_pulsewidth + (angle / 180.0) * (max_pulsewidth - min_pulsewidth)
    pi.set_servo_pulsewidth(servo_pin, pulsewidth)

try:
    print("start")
    num = 0
    while(num < 5):
        for angle in range(45,  135, 1):  # Sweep from 0 to 180 degrees
            set_servo_angle(angle)
            time.sleep(0.01)
        
        for angle in range(135, 45, -1):  # Sweep from 180 to 0 degrees
            set_servo_angle(angle)
            time.sleep(0.01)
            
        num += 1
    pi.stop()

        
except KeyboardInterrupt:
    # Stop the servo
    set_servo_angle(88)
    pi.stop()
    # Disconnect from the pigpio daemon
    
