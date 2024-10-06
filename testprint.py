from escpos import *

p = printer.Usb(idVendor=0x0416, idProduct=0x5011, interface=0, in_ep=0x81, out_ep=0x03)
p.text("Hello World\n")
p.cut()