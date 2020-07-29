import uasyncio #uasyncio ermöglicht eine gleichzeitige bearbeitung der Messungen und die Daten zu stören
import uarray   #uarray ist das Feld in Micropython
import pyb      #pyb ist das Modul des Pyboards die das Zugreifen der verschiedenen Pins des Pyboards ermöglich

locker = uasyncio.Lock() #schließt und öffnet Teilprogrammen
total_measurements = 20  #Anzahl der gesamten Messungen
schon_gemessen = 0       #Anzahl der schon gemessene Messungen

 async def empfanger(port):   #Verbindung mit dem Komputer
    global total_measurements
    global schon_gemessen
    swriter = uasyncio.StreamWriter(port) 
    sreader = uasyncio.StreamReader(port)

    #Unendliche Schleife, damit dem Komputer ständig mit dem Pyboard im Verbindung steht und dass mit einem Break abgebrochen wird 
    while True:
        await locker.acquire() #das Einzige Teilprogramm das läuft die anderen Teilprogrammen sind gesperrt 
        befehl = await sreader.readline() #empfangt ein Befehl von dem Komputer 
        befehl_ = str(befehl).replace("\\r\\n'", "") #Bearbeitung des Befehls
        
        if befehl_ == "b'zeigeMeasurments":
            await swriter.awrite("ShowMeasurements\r\n") #send dem Komputer ein Befehl, um ihn die förden, die gemessenen Daten zu zeigen
        
        await swriter.awrite("end\r\n")

        if schon_gemessen == total_measurements :
            await swriter.awrite("endeMessungen\r\n") #send dem Komputer ein Befehl, um ihn die förden, das Programm zu beenden
            break
        locker.release() #ermöglicht den anderen Teilprogrammen weiter zu laufen
        await uasyncio.sleep(1)        


#Empfang der Messungen des Sensors bzw Potentiometers
async def start_measurment(pin, port, Anzahl_measurments, timeout):
    global total_measurements
    global schon_gemessen
    usbwriter = uasyncio.StreamWriter(port)
    
    adc = pyb.ADC(pyb.Pin(pin))

    for i in range(Anzahl_measurments):
        await locker.acquire() #das Einzige Teilprogramm das läuft die anderen Teilprogrammen sind gesperrt 
        adc_ = adc.read() #Empfang der Messungen
        adcstr = pin+" "+str(adc_)+ "\r\n" #Bearbeitung der Messungen
        await usbwriter.awrite(adcstr)     #Sendung der Messungen an dem Komputer
        schon_gemessen += 1
        locker.release() #ermöglicht den anderen Teilprogrammen weiter zu laufen
        await uasyncio.sleep(timeout/Anzahl_measurments)   

#Haupt Function        
async def main():
    usb = pyb.USB_VCP()
    pyb.Pin("EN_3V3").on() #Aktivation der Spannungsquelle 
    

    task_ =  uasyncio.create_task(start_measurment("X3",usb,15, 10)) #Daten des ersten Pins
    task__ = uasyncio.create_task(start_measurment("Y7",usb,5, 5))   #Daten des zweiten Pins 
    befehl = uasyncio.create_task(empfanger(usb)) #Kommunikation zwischen Pyboard und Komputer

    print("Starten Haupt Threads")
    await task_
    await task__
    await befehl
    
    empfanger(usb)
    print("Ende des Programm")

uasyncio.run(main())