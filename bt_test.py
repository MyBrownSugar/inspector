import serial
ser = serial.Serial('/dev/cu.HC-06-DevB')  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'1')     # write a string
ser.close()             # close port