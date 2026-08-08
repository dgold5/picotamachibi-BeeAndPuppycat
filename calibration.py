from machine import I2C, Pin
import time
pinsLeftOfAGNDPin = [1,5,9,13,17,21,27]
pinsRightOfAGNDPin = [2,6,10,14,18,22,28]
shortedPins = []
Pin(27,Pin.IN,Pin.PULL_UP)

def checkForShort(GPIONumber):
    pin = Pin(GPIONumber, Pin.IN, Pin.PULL_UP)
    time.sleep(0.0625)
    print(GPIONumber," ", pin.value())
    if pin.value() == 0:
        if GPIONumber in pinsLeftOfAGNDPin:
            shortedPins.append(GPIONumber)
            shortedPins.append("GND")
        elif GPIONumber in pinsRightOfAGNDPin:
            shortedPins.append("GND")
            shortedPins.append(GPIONumber)
        else:
            shortedPins.append(GPIONumber)
    else:#didn't short to a GND pin, test other neighbors
        pinNPlusOne = Pin(GPIONumber+1, Pin.OUT)
        pinNPlusOne.value(0)
        if pin.value() == 0:
            shortedPins.append(GPIONumber)
            shortedPins.append(GPIONumber+1)
        
    

pinsUnderTest = list(range(0,22))
pinsUnderTest.append(26) #TODO: Do more pythonic
pinsUnderTest.append(27)
pinsUnderTest.append(28)
for pin in pinsUnderTest:
    checkForShort(pin)
if len(shortedPins) == 0:
    print("Congrats!  No shorts detected!")
elif len(shortedPins) == 2 and (shortedPins  == [1, 'GND'] or shortedPins  == ['GND', 6] or shortedPins  == [3, 4]):
    print("If testing 21 through 40, Congrats!  No atypical shorts detected!")
    print("If testing 1-20, short on:")
    print(shortedPins)
elif len(shortedPins) == 4 and (shortedPins == [1, 'GND', 'GND',6] or shortedPins == [1, 'GND', 3, 4]):
    print("If testing 21 through 40, Congrats!  No atypical shorts detected!")
    print("If testing 1-20, short on:")
    print(shortedPins)
elif len(shortedPins) == 6 and shortedPins == [1, 'GND', 3, 4, 'GND',6]:
    print("If testing 21 through 40, Congrats!  No atypical shorts detected!")
    print("If testing 1-20, short on:")
    print(shortedPins)
else:
    print("Atypical connection found, check the following solder connections:")
    print(shortedPins)
