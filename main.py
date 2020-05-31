# main.py -- put your code here
import uasyncio
import uarray
import pyb

locker = uasyncio.Lock()
total_measurements = 0
schon_gemessen = 0

async def empfanger(port):
    swriter = uasyncio.StreamWriter(port)
    sreader = uasyncio.StreamReader(port)
    while True:
        await locker.acquire()
        befehl = await sreader.readline()
        befehl_ = str(befehl).replace("\\r\\n'", "")
        
        if befehl_ == "b'zeigeMeasurments":
            await swriter.awrite("ShowMeasurements\r\n")
        
        await swriter.awrite("end\r\n")
        locker.release()
        await uasyncio.sleep(1)        



async def start_measurment(pin, port, Anzahl_measurments, timeout):
    usbwriter = uasyncio.StreamWriter(port)
    
    adc = pyb.ADC(pyb.Pin(pin))

    for i in range(Anzahl_measurments):
        await locker.acquire()
        adc_ = adc.read()
        adcstr = pin+" "+str(adc_)+ "\r\n"
        await usbwriter.awrite(adcstr)
        locker.release()
        await uasyncio.sleep(timeout/Anzahl_measurments)   
        
async def main():
    usb = pyb.USB_VCP()
    pyb.Pin("EN_3V3").on()

    task_ =  uasyncio.create_task(start_measurment("X3",usb,15, 10))
    task__ = uasyncio.create_task(start_measurment("Y7",usb,5, 5))
    befehl = uasyncio.create_task(empfanger(usb))

    print("Thread principal démaré")
    await task_
    await task__
    await befehl
    
    empfanger(usb)
    print("fin du programme")

uasyncio.run(main())