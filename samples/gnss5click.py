# Micropython code example for Digi International Xbee3
# cellular module interface to u-blox NEO-M8N GNSS receiver
# based Mikroelektronika GNSS 5 Click board   
#
# Wiring Diagram:
# XBee ->  GNSS 5 Click
#  11  TX  14 RX 
#   4  RX  13 TX 
# note: GNSS 5 powered by USB

from machine import I2C, UART
from time import sleep
import ustruct
# use UART interface to GNSS 5


# configure u-blox NEO-M8N uart for 9600 baud and UBX output mode
def config_M8():
  u = UART(1, 9600)
  u.init(9600, bits=8, parity=None, stop=1)
# UBX-CFG-PRT command to set UART1 output=0 (UBX output only) and 9600 baud
  buf1 = b'\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\xC0\x08\x00\x00\x80\x25\x00\x00\x07\x00\x01\x00\x00\x00\x00\x00\x90\xA9'
  u.write(buf1)
# catch ack
  while not u.any():
    if u.any():
        break
  poll = u.read()
# write UBX-CFG-PRT poll command
  buf1 = b'\xB5\x62\x06\x00\x01\x00\x01\x08\x22'
  u.write(buf1)
# catch poll response
  while not u.any():
    if u.any():
        break
  poll = u.read()
  u.deinit()  # this closes the UART
  REGISTER_FORMAT = '<i' # little endian 4 bytes
# offset for baud rate = 6 + 8
  baud = ustruct.unpack_from(REGISTER_FORMAT, poll, 14)[0]
  print ('baud rate= ', baud)
  
 
# check GNSS fix status and position in continuous loop
def chk_GNSS():
  while True:
    u = UART(1, 9600)
    u.init(9600, bits=8, parity=None, stop=1)
# UBX-NAV-STATUS hex poll command to check if position fix
    buf = b'\xB5\x62\x01\x03\x00\x00\x04\x0D'
    REGISTER_FORMAT = '>b' # one byte for nav status
    u.write(buf)
#sleep(1)
    while not u.any():
      if u.any():
          break
# read 24 bytes
    poll = u.read(24)
# offset for nav fix byte = 6 + 5
    nav_fix = ustruct.unpack_from(REGISTER_FORMAT, poll, 11)[0] 
    print ('nav fix= ', (nav_fix & 0x01))
# offset for nav status code byte = 6 + 4
    nav_stat = ustruct.unpack_from(REGISTER_FORMAT, poll, 10)[0]
    print ('nav status code= ', nav_stat)
# UBX-NAV-POSLLH hex poll command
    buf = b'\xB5\x62\x01\x02\x00\x00\x03\x0A'
# send poll command
    u.write(buf)
    while not u.any():
      if u.any():
          break
# read UBX-NAV-POSLLH poll result
    poll = u.read(36)
    u.deinit()  # this closes the UART
#print ('read nav data ',poll)
    REGISTER_FORMAT = '<i' # little endian 4 bytes
# offset for longitude status byte = 6 + 4
    lon = ustruct.unpack_from(REGISTER_FORMAT, poll, 10)[0]
    lat = ustruct.unpack_from(REGISTER_FORMAT, poll, 14)[0]
    if (nav_fix & 0x01) != 1:
        print ('no GNSS signal', (nav_fix/2))
    else:
        print ('longitude= ', (lon/1E7))
        print ('latitude= ', (lat/1E7))
    sleep(2)
    
# ######### MAIN PROGRAM #######################
  
# config GNSS 5 uart for ubx output and 9600 baud
config_M8()

# check GNSS status and location
chk_GNSS()















