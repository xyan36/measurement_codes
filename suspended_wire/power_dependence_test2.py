# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:05:51 2019

@author: Administrator
"""

from datetime import datetime
import time
import visa
import numpy as np
import os

########### function defitions ################################################
### lock in 1w initialize ###
def lockinInit_1w():
    lockin1.write("HARM 1")
    lockin2.write("HARM 1")

### lock in 3w initialize ###
def lockinInit_3w():
    #set lockins to measure the 3w voltage
    lockin1.write("HARM 3")
    lockin2.write("HARM 3")
    #reserve mode
    lockin1.write("RMOD 1")
    lockin2.write("RMOD 1")

def lockin_set_pms(timeCon,sensitivity):
    #time constant
    lockin1.write("OFLT %d" %timeCon)
    lockin2.write("OFLT %d" %timeCon)
    #sensitivity
    lockin1.write("SENS %d" %sensitivity)
    lockin2.write("SENS %d" %sensitivity)
    
def lockinsingle_set_pms(lockin, timeCon, sensitivity):
    #time constant
    lockin.write("OFLT %d" %timeCon)
    #sensitivity
    lockin.write("SENS %d" %sensitivity)
    
def outputs_query():
    v = lockin1.query('slvl?').rstrip()
    tc = lockin1.query('oflt?').rstrip()
    s_x3 = lockin1.query('sens?').rstrip()
    s_x1 = lockin2.query('sens?').rstrip()
    X3 = lockin1.query('outp?1').rstrip()
    Y3 = lockin1.query('outp?2').rstrip()
    X1_ref = lockin2.query('outp?1').rstrip()
    Y1_ref = lockin2.query('outp?2').rstrip()
    header = "V_input TC SENS_X3 SENS_X1 X3 Y3 X1_ref Y1_ref"
    print(header)
    print(v, tc, s_x3, s_x1, X3, Y3, X1_ref, Y1_ref, sep = " ")
    
def settings_query():
    f1 = lockin1.query('freq?').rstrip()
    f2 = lockin2.query('freq?').rstrip()
    tc1 = lockin1.query('oflt?').rstrip()
    tc2 = lockin2.query('oflt?').rstrip()
    sstvt1 = lockin1.query('sens?').rstrip()
    sstvt2 = lockin2.query('sens?').rstrip()
    header = "LOCKIN# FREQ TC SENS"
    print(header)
    print('lockin1', f1, tc1, sstvt1, sep = "\t")
    print('lockin2', f2, tc2, sstvt2, sep = "\t")
    
    
def set_V_input(lockin, voltage):
    lockin.write('slvl %f' %voltage)
    print(datetime.now(), f"Set V = {voltage}")

### measurements ###
def measurement(sens,initWaitTime, add_wait_time = 5): #sens= allowed error in reading
    X = float(lockin1.query("OUTP?1"))
    Y = float(lockin1.query("OUTP?2"))
    X_ref = float(lockin2.query("OUTP?1"))
    Y_ref = float(lockin2.query("OUTP?2"))
    time.sleep(initWaitTime) #initial wait time
#    #check reading to be stable
    while (np.abs(X - float(lockin1.query('OUTP?1')))> sens
        or np.abs(X_ref - float(lockin2.query('OUTP?1')))> sens):
        X = float(lockin1.query("OUTP?1"))
        Y = float(lockin1.query("OUTP?2"))
        X_ref = float(lockin2.query("OUTP?1"))
        Y_ref = float(lockin2.query("OUTP?2"))
        time.sleep(add_wait_time) #additional wait time
    line = str(X) + " " + str(Y) + " "  \
            + str(X_ref) + " " + str(Y_ref) + " "
    return line

### voltage swap ###
def VoltageSweep(voltages,sens1, TC1, SENS1, initWaitTime1, sens3, TC3, SENS3, initWaitTime3):
    for v in voltages:
        lockin1.write("SLVL %f" %v)
        line = str(v) + " "
        time.sleep(5) #waiting for voltage stable
        lockinInit_1w()
        lockin_set_pms(TC1,SENS1)
        line += measurement(sens1,initWaitTime1)
        lockinInit_3w()
        lockin_set_pms(TC3,SENS3)
        line += measurement(sens3,initWaitTime3).rstrip()
        t = float(time.time()-t0)
        print(str(datetime.now()) + " " + str(t) + " " + line)
        with open(FILENAME,'a') as output:
            output.write(str(datetime.now()) + " " + str(t) + " " + line +"\n")
 
def voltage_sweep_auto(voltages, initWaitTime):
    try:
        for v in voltages:
            lockin1.write('slvl %f' %v)
            time.sleep(initWaitTime)
            
            dt = str(datetime.now())
            t = round(float(time.time()-t0), 4)
            vin = str(v)
            tc = lockin1.query('oflt?').rstrip()
            sens_x3 = lockin1.query('sens?').rstrip()
            sens_x1 = lockin2.query('sens?').rstrip()
            X3 = lockin1.query('outp?1').rstrip()
            Y3 = lockin1.query('outp?2').rstrip()
            X1_ref = lockin2.query('outp?1').rstrip()
            Y1_ref = lockin2.query('outp?2').rstrip()
            
            line = f"{dt},{t},{vin},{tc},{sens_x3},{sens_x1},{X3},{Y3},{X1_ref},{Y1_ref}"
            print(line)
            with open(FILENAME,'a') as output:
                output.write(line +"\n")
    except KeyboardInterrupt:
        print('keyboardinteeruupt')
        pass
    finally:
        lockin1.write("SLVL %f" %0.004)
        lockin1.write('FREQ %f' %17)
        lockin_set_pms(timeCon=9,sensitivity=22)
        lockinInit_1w()
        tf = datetime.now()
        print ("Program done! total time is: "+ str(tf-ti))

def voltage_sweep_manual(voltages, initWaitTime):
    try:
        for v in voltages:
            lockin1.write('slvl %f' %v)
            time.sleep(initWaitTime)
            
            dt = str(datetime.now())
            t = round(float(time.time()-t0), 4)
            vin = str(v)
            tc = lockin1.query('oflt?').rstrip()
            sens_x3 = lockin1.query('sens?').rstrip()
            sens_x1 = lockin2.query('sens?').rstrip()
            X3 = lockin1.query('outp?1').rstrip()
            Y3 = lockin1.query('outp?2').rstrip()
            X1_ref = lockin2.query('outp?1').rstrip()
            Y1_ref = lockin2.query('outp?2').rstrip()
            line = f"{dt},{t},{vin},{tc},{sens_x3},{sens_x1},{X3},{Y3},{X1_ref},{Y1_ref}"
            print(line)
            
            usercheck = input('Is reading stable? Type \'y\' to record: ')
            while usercheck != 'y':
                print('Not recorded.')
                usercheck = input('Is reading stable? Type \'y\' to record: ')
            dt = str(datetime.now())
            t = round(float(time.time()-t0), 4)
            vin = str(v)
            tc = lockin1.query('oflt?').rstrip()
            sens_x3 = lockin1.query('sens?').rstrip()
            sens_x1 = lockin2.query('sens?').rstrip()
            X3 = lockin1.query('outp?1').rstrip()
            Y3 = lockin1.query('outp?2').rstrip()
            X1_ref = lockin2.query('outp?1').rstrip()
            Y1_ref = lockin2.query('outp?2').rstrip()
            line = f"{dt},{t},{vin},{tc},{sens_x3},{sens_x1},{X3},{Y3},{X1_ref},{Y1_ref}"
            print(line)
            with open(FILENAME,'a') as output:
                output.write(line +"\n")
            print('Recorded.')
    except KeyboardInterrupt:
        print('keyboardinteeruupt')
        pass
    finally:
        lockin1.write("SLVL %f" %0.004)
        #output.close()# may record unfinished data
        tf = datetime.now()
        print ("Program done! total time is: "+ str(tf-ti))
    ##############################################################################

### crate a folder with today's date and create a new file name ###
date = '210714'
try:
    os.mkdir(date)
except FileExistsError:
    pass
FILENAME = f"{date}//{date}_Bi2Te3_n10_power_dep_f3p4_1.txt"

rm = visa.ResourceManager();
print(rm.list_resources())
lockin1 = rm.open_resource("GPIB2::8::INSTR") #sample & SINE_OUT source
lockin2 = rm.open_resource("GPIB2::9::INSTR") #reference resistor

header = "Date_time,Time,V_input,TC,SENS_X3,SENS_X1,X3,Y3,X1_ref,Y1_ref\n"
print(header)
with open(FILENAME,'w') as output:
    output.write(header)

### Set the parameters ###
freq = 3.4 #Hz
timeCon = 13 #
voltages = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5])
sensitivity1 = 24# sensitivity for 1w measurement
sensitivity3 = 21# sensitivity for 3w measurement
initWaitTime = 15 * 60#s
lockin1.write('harm 3')
lockin2.write('harm 1')
##########################
lockin1.write('FREQ %f' %freq)
t0 = time.time()
ti = datetime.now()
lockinsingle_set_pms(lockin1, timeCon, sensitivity3)
lockinsingle_set_pms(lockin2, timeCon, sensitivity1)
voltage_sweep_auto(voltages, initWaitTime)
