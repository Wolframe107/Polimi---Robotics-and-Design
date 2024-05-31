import pigpio
import time
import subprocess
import runningAverage


subprocess.run(["sudo", "pigpiod"], check=True)
time.sleep(1)
pi = pigpio.pi()

mic1_pin = 23
mic2_pin = 24

mic1_avg = runningAverage.RunningAverage()
mic2_avg = runningAverage.RunningAverage()

if not pi.connected:
	print("not connected")
else:
	print("connected!")

pi.set_mode(mic1_pin, pigpio.INPUT)
pi.set_pull_up_down(mic1_pin, pigpio.PUD_DOWN)

pi.set_mode(mic2_pin, pigpio.INPUT)
pi.set_pull_up_down(mic2_pin, pigpio.PUD_DOWN)

test_avg = True
try:
	while(True):
		if test_avg:
			mic1_avg.add_value(pi.read(mic1_pin))
			mic2_avg.add_value(pi.read(mic2_pin))
			print("Mic 1: " + str(mic1_avg.get_average()) + "      Mic 2: " +  str(mic2_avg.get_average()))
		else:
			print("Mic 1: " + str(pi.read(mic1_pin)) + "      Mic 2: " +  str(pi.read(mic2_pin)))
		time.sleep(0.01)

except KeyboardInterrupt:
	print("DONE")
	subprocess.run(["sudo", "killall", "pigpiod"], check=True)
