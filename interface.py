#Pinler:
#   Led        --> 22
#   Fener      --> 23
#   Buzzer     --> 24
#   Sicaklik   --> CH0
#   Nem        --> CH1
#   Gaz        --> CH2

#Moduller
from tkinter import *
import time
from threading import Thread
import keyboard
from gpiozero import MCP3008, LED, Buzzer
import pigpio

#Arayuz
def interface():
    global temperatureLabel
    global humidityLabel
    global gasLabel
    global flashlightButton

    root = Tk()
    root.geometry("500x{}+1500+0".format(root.winfo_screenheight()))

    projectNameLabel = Label(root, text="HORUS KONTROL\nARAYÜZÜ", font=("Helvetica 35 bold"), height=3)
    projectNameLabel.pack()
    temperatureLabel = Label(root, text="Sıcaklık: Veriler Toplanıyor...", font=("Helvetica", 25))
    temperatureLabel.pack()
    humidityLabel = Label(root, text="Nem: Veriler Toplanıyor...", font=("Helvetica", 25))
    humidityLabel.pack()
    gasLabel = Label(root, text="Gaz: Veriler Toplanıyor...", font=("Helvetica", 25))
    gasLabel.pack()
    
    Frame(root, height=20).pack()
    
    Label(root, text="Hız", font=("Helvetica 35 bold"), height=1).pack()

    velocityScale = Scale(root, orient=HORIZONTAL, tickinterval=10, width=20, length=400, activebackground="white", bg="gray")
    velocityScale.pack()
    
    Frame(root, height=20).pack()
    
    flashlightButton = Button(root, text="Fener", font=("Helvetica 35 bold"), height=2, width=15, bg="gray", relief="raised", command=ononffFlashlight)
    flashlightButton.pack()

    mainloop()

#Sensorlerden gelen verileri aninda arayuze yazdirma
def updateSensorData():
    while True:
        temperatureLabel.configure(text=("Sıcaklık:", temperatureSensorInput.value))
        humidityLabel.configure(text=("Nem:", humiditySensorInput.value))
        gasLabel.configure(text=("Gaz:", gasSensorInput.value))

#Feneri kapama acma fonksiyonu
def ononffFlashlight():
    if flashlightButton["relief"] == "raised":
        flashlightButton.configure(relief="sunken")
        flashlight.on()
    else:
        flashlightButton.configure(relief="raised")
        flashlight.off()

#W,A,S,D ve yon tuslarina tanimlanan gorev fonksiyonu
def onPressedKey(key):
    print(key+"'a basıldı.")

#Klavye tuslari tanimlamalari
def keyboardActions():
    keyboard.add_hotkey("w", lambda: onPressedKey("w"))
    keyboard.add_hotkey("a", lambda: onPressedKey("a"))
    keyboard.add_hotkey("s", lambda: onPressedKey("s"))
    keyboard.add_hotkey("d", lambda: onPressedKey("d"))
    keyboard.add_hotkey("up", lambda: onPressedKey("yukari yon tusuna"))
    keyboard.add_hotkey("right", lambda: onPressedKey("sag yon tusuna"))
    keyboard.add_hotkey("down", lambda: onPressedKey("asagi yon tusuna"))
    keyboard.add_hotkey("left", lambda: onPressedKey("sol yon tusuna"))
        
#Anormal deger aldiginda arayuze isleme
def abnormalValueInspector():
    abnormalTemperatureValueLowerBound = 0
    abnormalHumidityValueLowerBound = 0
    abnormalGasValueLowerBound = 0
    if temperatureSensorInput.value >= abnormalTemperatureValueLowerBound:
        temperatureLabel.configure(font=("Helvetica 25 bold"), fg=("red"))
    if humiditySensorInput.value >= abnormalHumidityValueLowerBound:
        humidityLabel.configure(font=("Helvetica 25 bold"), fg=("red"))
    if gasSensorInput.value >= abnormalGasValueLowerBound:
        gasLabel.configure(font=("Helvetica 25 bold"), fg=("red"))
    if temperatureSensorInput.value < abnormalTemperatureValueLowerBound:
        temperatureLabel.configure(font=("Helvetica 25"), fg=("black"))
    if humiditySensorInput.value < abnormalHumidityValueLowerBound:
        humidityLabel.configure(font=("Helvetica 25"), fg=("black"))
    if gasSensorInput.value < abnormalGasValueLowerBound:
        gasLabel.configure(font=("Helvetica 25"), fg=("black"))

#Insan yuzu gordugunda calisan fonksiyon
def on_person_face():
    led.on()
    buzzer.on()

#Threadleri baslatan fonksiyon
def startThreads():
    keyboardActionsThread = Thread(target=keyboardActions)
    sensorDataUpdaterThread = Thread(target=updateSensorData)
    
    sensorDataUpdaterThread.start()
    keyboardActionsThread.start()

#Elektroniklerin pin numaralari, INPUT-OUTPUT durumlarinin ayarlari
def defineElectronics():
    global led
    global flashlight
    global buzzer
    global temperatureSensorInput
    global humiditySensorInput
    global gasSensorInput
    global pi
    global INA
    global INB
    global INC
    global IND
    pi = pigpio.pi()
    led = LED(22)
    flashlight = LED(23)
    buzzer = Buzzer(24)
    temperatureSensorInput = MCP3008(channel=0)
    humiditySensorInput = MCP3008(channel=1)
    gasSensorInput = MCP3008(channel=2)
    INA = 13
    INB = 19
    INC = 26
    IND = 12
    for i in [INA, INB, INC, IND]:
        pi.set_mode(i, pigpio.OUTPUT)

#Ana kisim
if __name__=="__main__":
    defineElectronics()
    startThreads()
    interface()