import serial
import time

#kommunikation mit uBoard aufbauen
#baudrate = 115200 Mhz
#parity = PARITY_EVEN Art der Überprüfung
uBoard = serial.Serial('/dev/tty.usbserial-1420', 115200, timeout = 3)


#Verwaltung EIn -Ausgabe zwischen Pyboard und uBoard
try:
    anfangZeit = time.time()
    vorherigeZeit = anfangZeit

    #while Schleife damit unser Code undendlich läuft
    while True:
        #gibt es Daten im uBoard, lesen wir diese Daten
        if uBoard.in_waiting > 0:
            uBoardAusgabe = uBoard.readline()
            print('micro Board empfangene Daten : {}'.format(uBoardAusgabe.decode('utf-8').strip('\r\n')))
        
        #wir geben dem uBoard jede 2 Sekunde befehle ein 
        neueZeit = time.time()
        if neueZeit - vorherigeZeit > 2:
            vorherigeZeit = neueZeit
            print("Komputer sendet den Befehl : 'a' um : {} an der Microboard ".format(time.time()))
            uBoard.write(b'a\r\n')

        #Endet nach 50 Sekunden
        if neueZeit - anfangZeit > 50 :
            uBoard.write('\x00\r\n'.encode())
        
        time.sleep(1)

#ctrl+c für Ausprung
except KeyboardInterrupt:
    print('Tastatur Ausprung')

#alles schließen
finally:
    if uBoard.is_open:
        uBoard.close()
        print('Ende der Kommunication')            