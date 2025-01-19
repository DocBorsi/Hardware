import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()

lcd.clear()
lcd.set_backlight(1)
lcd.message('Hello, World!')
time.sleep(2)
lcd.clear()
lcd.message('Raspberry Pi')
time.sleep(2)
lcd.clear()

