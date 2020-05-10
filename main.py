#uBoard main Code
import machine
import time

led = machine.Pin(2, machine.Pin.OUT) #pyb.LED(2) on Pyboard

#print("start")

def main():
    #Aufbau Asynchron Kommunikation
    #Kanal 0 für USB kommunikation
    uart = machine.UART(0)
    uart.init(115200, timeout = 3000)
    
    #Zeit in milliSekunde
    vorherigeZeit = time.ticks_ms()
    
    #while Schleife, damit das Programm unendlich läuft
    while True:
        #empfangt die Befehlen des Komputers
        if uart.any():
            pcBefehl = uart.readline()
            if pcBefehl is not None:
                strPcBefehl = str(pcBefehl.decode('utf-8'))
                uart.write("Der Komputer hat den Befehl ' " + strPcBefehl.strip("\r\n") + " ' gesendet" )
        
        #Actuelle Zeit in ms() 
        neueZeit = time.ticks_ms()
        
        #jede Sekunde etwas schreiben
        if time.ticks_diff(neueZeit, vorherigeZeit) > 1000:
            vorherigeZeit = neueZeit
            uart.write("es ist " + str(neueZeit) + " on the micro Board"+ "\r\n")
            led.value(not led.value()) #led.toggle() on Pyboard
        
main()  
