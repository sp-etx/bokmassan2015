# -*- coding: utf-8 -*-
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import paho.mqtt.client as client
import paho.mqtt.publish as publish
import json

modbus = ModbusClient('192.168.0.99')

#tsense_arr = [10,11,12,13,14,15,16,17,18,19]
tsense_arr = [11]
ppm = 0
temp = 0
hum = 0

def readModbus():
	for idx,addr in enumerate(tsense_arr):
		rr = modbus.read_input_registers(3,3, unit=addr)
		#print "%s\t Unit: %d\tCO2: %.0f ppm\tTemp: %.2f C\t Hum: %.2f RH" % (time.asctime(time.localtime()),addr,rr.registers[0],rr.registers[1]/100.0,rr.registers[2]/100.0)
		tup = (time.time(),rr.registers[0],rr.registers[1]/100.0,rr.registers[2]/100.0)

		ppm = str(rr.registers[0])
		temp = str(rr.registers[1]/100.0)
		hum = str(rr.registers[2]/100.0)

		d1 = {}
		d1["ppm"] = ppm
		d1["temp"] = temp
		d1["hum"] = hum
		print d1
		return json.dumps(d1)

def sendToMQTT(data):
	publish.single("/bokmassa/tsense1", data, hostname="localhost", qos=1, retain=False)

if __name__ == '__main__':
	while True:
		try:
			data = readModbus()
			sendToMQTT(data)
		except KeyboardInterrupt:
			raise
		except:
			raise
		time.sleep(1)