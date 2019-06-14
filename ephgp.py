# Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from Tkinter import *
from hcre.py import distanz


# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# tkinter Window aufrufbar ueber den namen "master"
master = Tk()

# hoehe und breite des Windows
canvas = Canvas(master, width=700, height=700)

# name des Windows
master.title("RealtimeDataVisualization")

# polygone der garage und des autos
pointscar = [300, 300, 300, 400, 500, 400, 500, 300]
pointsgarage = [100, 100, 100, 600, 500, 600, 500, 500,
                200, 500, 200, 200, 500, 200, 500, 100, 100, 100]

# pointsgarage=[x1,y1,x2,y2,...,x(n),y(n)]
# create_plygon erstellt ein objekt indem es alle angegeben punkte aus
# pointscar und pointsgarage nacheinander verbindet
car = canvas.create_polygon(pointscar, fill="green", width=2)
garage = canvas.create_polygon(pointsgarage, fill="black", width=2)
canvas.pack()

# funktion zum bewegen des "cars" indem die distanz 2 mal uebergeben wird und
# die differenz als x wert zum bewgen des cars genommen wird


def carmovex(positionx_a, distanz):
    canvas.move(car, (distanz-positionx_a), 0)

def carmovey1(positionx_a, distanz):
    canvas.move(car, 0, (distanz-positionx_a))

def carmovey2(positionx_a, distanz):
    canvas.move(car, 0, (distanz-positionx_a))
# differenz funktion um die differenz des cars vom vorherigen standpunkt zum jetzigen standpunkt zu berechenen



# vorgefertigete distanz funktion um den abstand zum sensor zu ermitteln


def distanz():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz if distanz>2 and distanz<300 else None


# main
if __name__ == '__main__':
    try:

        while True:
            carcoords = canvas.coords(car)
            distanz = distanz()
            if (distanz == None):
                continue
            else:
                carmovex(carcoords[0], (distanz+200))
                #carmovex(carcoords[1], (distanz))
                #carmovex(carcoords[3], (distanz))
                time.sleep(0.005)
            master.update()

        master.mainloop()

        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
