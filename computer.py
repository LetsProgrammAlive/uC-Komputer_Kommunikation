import serial

ser = serial.Serial("/dev/tty.usbmodem3571314C30372", 115200, timeout=3)

channelX3 = []
channelY7 = []


while ser.in_waiting==0:
    print("waiting for pyboard...")
while True:
    #ser.write(b"WeitereMessungen \r\n")
    recv = ser.readline()
    recv = str(recv)
    recvs = recv.replace("\\r\\n'","")
    recvs = recvs.replace("\\r\\n","")
    
        
    if recvs[0:4]== "b'X3":
        recv_ = recvs.replace("b'X3", "")
        recvInt = int(recv_)
        channelX3.append(recvInt)
    elif recvs[0:4] == "b'Y7":
        recv_ = recvs.replace("b'Y7", "")
        recvInt = int(recv_)
        channelY7.append(recvInt)
    elif recvs == "b'ShowMeasurements":
        print("measurements von Pin X3: ")
        print(channelX3)
        print("measurements von Pin Y7: ")
        print(channelY7)
    else:
        print(recvs)

    ser.write(b'zeigeMeasurments\r\n')
    
        
        



