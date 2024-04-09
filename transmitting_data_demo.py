import serial
def readserial(comport, baudrate):
    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    while True:
        data = ser.readline().decode().strip()
        if data:
            print(data)

        sendImage('COM5', 9600, ser)

def sendImage(comport, baudrate,ser):
    #ser = serial.Serial(comport, baudrate)
    ser.write("\n".encode())

if __name__ == '__main__':
    #sendImage('COM5', 9600)

    readserial('COM5', 9600)
    
    


# Send image data
