#Serial ist das Modul, das uns ermöglicht mit dem Pyboard zu kommunizieren
import serial 

#wir greifen dem Pfad von dem Pyboard zu
ser = serial.Serial("/dev/tty.usbmodem3571314C30372", 115200, timeout=3)

channelX3 = [] #Feld für die Ersten Messungen
channelY7 = [] #Feld dür die Zweiten Messungen

#Wartezeit damit, sich dem Komputer mit dem Pyboard verbindet
while ser.in_waiting==0:
    print("waiting for pyboard...")


#Unendliche Schleife, damit dem Komputer ständig mit dem Pyboard im Verbindung steht und dass mit einem Break abgebrochen wird 
while True:
    #ser.write(b"WeitereMessungen \r\n")
    recv = ser.readline()                     #empfang die Daten
    recv = str(recv)                          #umwandelt die Daten in String 
    recvs = recv.replace("\\r\\n'","")        #Bearbeitung der Daten
    recvs = recvs.replace("\\r\\n","")        #weitere Bearbeitung


#Trennung der empfangenen Daten 
    if recvs[0:4]== "b'X3":                   #Daten von den ersten Messungen
        recv_ = recvs.replace("b'X3", "")     #Bearbeitung
        recvInt = int(recv_)                  #umwandlung in Integer
        channelX3.append(recvInt)             #füge im ersten Feld hinzu

    elif recvs[0:4] == "b'Y7":                #Daten von den ersten Messungen
        recv_ = recvs.replace("b'Y7", "")     #Bearbeitung
        recvInt = int(recv_)                  #umwandlung in Integer
        channelY7.append(recvInt)             #füge im ersten Feld hinzu

    elif recvs == "b'ShowMeasurements":       #Zeige anschließend die Messungen
        print("measurements von Pin X3: ")
        print(channelX3)                      #erste Messungen
        print("measurements von Pin Y7: ")
        print(channelY7)                      #zweiten Messungen
    elif recvs == "b'endeMessungen":
        break                                 #end
    else:
        print(recvs)                          #wenn nichts passiert dann ist vermutlich einen Fehler aufgetreten... wir zeigen die Meldung mit print

    ser.write(b"zeigeMeasurments\r\n")
    
        
        



