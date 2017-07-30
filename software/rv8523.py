#!/usr/bin/python 

import time
import datetime
import subprocess
import smbus

bus = smbus.SMBus(1)
addr = 0x68 #default: 0x68

def bin2bcd(val):
  return (val + (6 * (val / 10)))

def bcd2bin(val):
  return (val - (6 * (val >> 4)))

def print_time(dt):
  print dt.year, "-", dt.month, "-", dt.day, ' ', dt.hour, ":", dt.minute, ":", dt.second

def get_sys_time():
  dt = datetime.datetime.now()
  return dt

def set_sys_time(dt):
  second = str(dt.second)
  minute = str(dt.minute)
  hour   = str(dt.hour)
  day    = str(dt.day)
  month  = str(dt.month)
  year   = str(dt.year)
  subprocess.call("sudo date -s '" + year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second + "' > /dev/null", shell=True)

def get_rtc_time():
  bus.write_byte(addr, 0x03)
  second = bcd2bin(bus.read_byte(addr) & 0x7F)
  minute = bcd2bin(bus.read_byte(addr) & 0x7F)
  hour   = bcd2bin(bus.read_byte(addr) & 0x3F)
  day    = bcd2bin(bus.read_byte(addr) & 0x3F)
  wday   = bcd2bin(bus.read_byte(addr) & 0x07)
  month  = bcd2bin(bus.read_byte(addr) & 0x1F)
  year   = bcd2bin(bus.read_byte(addr)) + 2000
  dt = datetime.datetime(year, month, day, hour, minute, second)
  return dt

def set_rtc_time(dt):
  bus.write_byte(addr, 0x03)
  bus.write_byte(addr, bin2bcd(dt.second))
  bus.write_byte(addr, bin2bcd(dt.minute))
  bus.write_byte(addr, bin2bcd(dt.hour))
  bus.write_byte(addr, bin2bcd(dt.day))
  bus.write_byte(addr, bin2bcd(0x00))
  bus.write_byte(addr, bin2bcd(dt.month))
  bus.write_byte(addr, bin2bcd(dt.year - 2000))

def rtc_start():
  bus.write_byte(addr, 0x00) #control 1
  val = bus.read_byte(addr)
  if val & (1<<5):
    bus.write_byte(addr, 0x00) #control 1
    bus.write_byte(addr, val & ~(1<<5)) #clear STOP (bit 5)

def rtc_stop():
  bus.write_byte(addr, 0x00) #control 1
  val = bus.read_byte(addr)
  if not (val & (1<<5)):
    bus.write_byte(addr, 0x00) #control 1
    bus.write_byte(addr, val | (1<<5)) #set STOP (bit 5)

def rtc_bat_switchover():
  bus.write_byte(addr, 0x02) #control 3
  val = bus.read_byte(addr)
  if val & 0xE0:
    bus.write_byte(addr, 0x02) #control 3
    bus.write_byte(addr, val & ~0xE0) #battery switchover in standard mode


print "Start RTC"
rtc_start()
rtc_bat_switchover()

print "System Time: "
t = get_sys_time()
print_time(t)

print "Set Time to RTC"
set_rtc_time(t)

print "RTC Time: "
t = get_rtc_time()
print_time(t)

print "Set Time to System"
set_sys_time(t)

print "System Time: "
t = get_sys_time()
print_time(t)
