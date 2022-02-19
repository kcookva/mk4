#!/usr/bin/env python
# K1rBy
''' Monitoring Software for MK4 GTI Project Car (Europäische Gruppe?) '''

# import libraries
from serial import serial
import obd
import time
# import termchart
import os
from art import *
import datetime

# graph = termchart.Graph([])
print("\n")
aprint("hal")
print(datetime.datetime.now())
tprint('\n\n        MK4  SYSTEM  START   ', font="doom")

print('''
         つ ╹ ╹ つ

        ''')
print('\n')

# scan device ports
ports = obd.scan_serial()
print(ports)

print("\n")
# print("To die is fate, to live is luck\n")
aprint("playing cards waterfall")
print("\n")
connection = obd.Async() # async connect (use obd.OBD() for auto connect)

'''
if connection.status() == OBDStatus.CAR_CONNECTED:
    continue
else:
    print "ERR: Connection Status NULL"
    break
'''

# retreive ECU data
def fuel_specs():

    # fuel level
    vw_fuel_level = obd.commands.FUEL_LEVEL # pid 2F
    res_fuel_level = connection.query(vw_fuel_level) # res is response (not result)
    print(res_fuel_level.value) # should be as percentage


    # fuel type
    vw_fuel_type = obd.commands.FUEL_TYPE # pid 51
    res_fuel_type = connection.query(vw_fuel_type)
    print(res_fuel_type.value) # string format

    # ethanol %
    ethanol_perc = obd.commands.ETHANOL_PERCENT # pid 52
    res_ethanol_perc = connection.query(ethanol_perc)
    print(res_ethanol_perc.value)

    # fuel injection timing (degrees)
    vw_inj_time = obd.commands.FUEL_INJECT_TIMING # pid 5D
    res_inj_time = connection.query(vw_inj_time)
    print(res_inj_time.value) # should be in degrees



def intake_press():
    vw_intake = obd.commands.INTAKE_MANIFOLD_PRESSURE # pid 0B
    res_vw_intake = connection.query(vw_intake)
    print(float(res_vw_intake.value)) # string format (kPs to float)

    #print("\n------ " + p.value + " ------")


def cool_temp(c):

    print("\n------ " + c.value + " ------")



def eng_load(e):
    
    print("\n------ " + e.value + " ------")

    '''
    vw_load = obd.commands.ENGINE_LOAD # pid 04
    res_load = connection.query(vw_load)
    print(res_load.value) # should be % format
    '''

def intake_temp(i):
    
    print("\n------ " + i.value + " ------")

    '''
    vw_itemp = obd.commands.INTAKE_TEMP # pid 0F
    res_itemp = connection.query(vw_itemp)
    print(res_itemp.value.to("celsius")) # hopefully will convert to celius from kilopascals :)
    '''

# Misfire monitoring is from Mode 6 and is still in development (has not been fully tested on cars)
def misfire_monitor():

    # Cylinder 1
    misfire_one_res = connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_1)
    result_one = misfire_one_res.value.MISFIRE_COUNT

    if not result_one.is_null():
        print(result_one.value)
    else:
        print("Misfire count for cylinder 1 wasn't reported\n")


    # Cylinder 2
    misfire_two_res = connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_2)
    result_two = misfire_two_res.value.MISFIRE_COUNT

    if not result_two.is_null():
        print(result_two.value)
    else:
        print("Misfire count for cylinder 2 wasn't reported\n")

    # Cylinder 3
    misfire_three_res = connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_3)
    result_three = misfire_three_res.value.MISFIRE_COUNT

    if not result_three.is_null():
        print(result_three.value)
    else:
        print("Misfire count for cylinder 3 wasn't reported\n")

    # Cylinder 4 (thank god i only have 4 of these :P)
    misfire_four_res = connection.query(obd.commands.MONITOR_MISFIRE_CYLINDER_4)
    result_four = misfire_four_res.value.MISFIRE_COUNT

    if not result_four.is_null():
        print(result_four.value)
    else:
        print("Misfire count for cylinder 4 wasn't reported\n")


def maf(m):
    
    print("\n------ " + m.value + " ------")

    '''
    vw_maf = obd.commands.MAF # pid 10
    vw_maf_res = connection.query(vw_maf)
    print(vw_maf_res.value) # Unit.grams / second
    '''

def oil_temp(o):
    
    print("\n------ " + o.value + " ------")

    '''
    vw_otemp = obd.commands.OIL_TEMP # pid 5C
    vw_otemp_res = connection.query(vw_otemp)
    print(vw_otemp_res.value) # this should be in celsius by default
    '''

def control_mod_volt():

    vw_mod_volt = obd.commands.CONTROL_MODULE_VOLTAGE # pid 42
    modvolt_res = connection.query(vw_mod_volt)
    print(modvolt_res.value) # in volts


print("\n")
# non-async functions
# misfire_monitor() -- in development x_x
control_mod_volt()

print("\n")

# asynchronous loop for live data feed every 5 seconds
def live_feed():

    try:
        while True:
        
            # lil dance
            aprint("kirby dance")
            print("\n")

            '''
            # start live graph
            graph.addData(intake_press())
            graph.draw()
            time.sleep(1)
            '''

            connection.watch(obd.commands.INTAKE_PRESSURE, callback=intake_press)
            print("\n")
            connection.watch(obd.commands.COOLANT_TEMP, callback=cool_temp)
            print("\n")
            connection.watch(obd.commands.ENGINE_LOAD, callback=eng_load)
            print("\n")
            connection.watch(obd.commands.INTAKE_TEMP, callback=intake_temp)
            print("\n")
            connection.watch(obd.commands.MAF, callback=maf)
            print("\n")
            connection.watch(obd.commands.OIL_TEMP, callback=oil_temp)
            print("\n\n")
        
            print("========================================================================")
            print("\n\n")
            connection.start()

            # callback is fired upon receipt of new data
            time.sleep(5) # note in seconds not ms
            connection.close()

    except KeyboardInterrupt:
        pass

choice = int(input(" 1. Live Feed | 2. Misfire Check | 3. Fuel Specs\n\n"))

if choice == 1:
    live_feed()

elif choice == 2:
    print("\n")
    misfire_monitor()

elif choice == 3:
    print("\n")
    fuel_specs()

else:
    print("Auf Wiedersehen")

# tbc





