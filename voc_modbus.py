#!/usr/bin/env python
#
#Author: Marcus Kempe, SP Swedish Technical Research Institute
#

from pymodbus.client.sync import ModbusSerialClient as Modbus
timeoutModbus = 1.0
portName = '/dev/ttyUSB0'
Voc = Modbus(method='rtu', port=portName, baudrate=9600, timeout=timeoutModbus, stopbits = 1, parity = 'E')

def s16_to_int(s16):
    if s16 > 32767:
        return s16 - 65536
    else:
        return s16

while True:
    voc_data = Voc.read_input_registers(0, 3, unit=1)
    try:
        print voc_data.registers
        print voc_data.registers[0]
        print voc_data.registers[1]
        print voc_data.registers[2]
    except:
        print "VOC on address 1 did not answer"
        break
    time.sleep(1)

