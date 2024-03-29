# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:05:51 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:00:10 2019

@author: Administrator
"""

from datetime import datetime
import time
import visa
import numpy as np
import os
### basic parameters ###
rm = visa.ResourceManager();
print(rm.list_resources())
lockin1 = rm.open_resource("GPIB2::8::INSTR") #sample
lockin2 = rm.open_resource("GPIB2::9::INSTR") #reference resistor
### output file initialize ###
date = '210716'
try:
    os.mkdir(date)
except FileExistsError:
    pass    
FILENAME = f"{date}//{date}_Bi2Te3_p11_2mm_3w_2.txt"
t0 = time.time()
ti = datetime.now()
header = "Date_time Time TC SENS Lockin1f Lockin2f X3 Y3 X3_ref Y3_ref\n"
with open(FILENAME, 'w') as output:
    output.write(header)

### lock in initialize ###
def lockinInit_1w():
    #set lockin1 to internal (1), lockin2 to external(0)
#    lockin1.write("FMOD 0")
#    lockin2.write("FMOD 0")
    #set lockins to measure the 1w voltage
    lockin1.write("HARM 1")
    lockin2.write("HARM 1")
#    #make phases zero
#    lockin1.write("PHAS 0")
#    lockin2.write("PHAS 0")
#    #set input configuration
#    lockin1.write("ISRC 1")
#    lockin2.write("ISRC 1")
#    #ground type
#    lockin1.write("IGND 1")
#    lockin2.write("IGND 1")
#    #input coupling ac 0 dc 1
#    lockin1.write("ICPL 1")
#    lockin2.write("ICPL 1")
    #reserve mode
#    lockin1.write("RMOD 1")
#    lockin2.write("RMOD 1")
    #sensitivity
    lockin1.write("SENS 24")
    lockin2.write("SENS 24")
    #time constant
    lockin1.write("OFLT 9")
    lockin2.write("OFLT 9")  
def lockinInit_3w():
    #set lockins to measure the 3w voltage
    lockin1.write("HARM 3")
    lockin2.write("HARM 3")
#    #reserve mode
#    lockin1.write("RMOD 1")
#    lockin2.write("RMOD 1")
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

### measurements ###
def measurement(f1,f2,sens,initWaitTime): #sens= allowed error in reading
    X3 = float(lockin1.query("OUTP?1"))
    Y3 = float(lockin1.query("OUTP?2"))
    X3_ref = float(lockin2.query("OUTP?1"))
    Y3_ref = float(lockin2.query("OUTP?2"))
    time.sleep(initWaitTime) #initial wait time
    X33 = float(lockin1.query("OUTP?1"))
#    Y11 = float(lockin1.query("OUTP?2"))
    X33_ref = float(lockin2.query("OUTP?1"))
#    Y22 = float(lockin2.query("OUTP?2"))
    #check reading to be stable
    while (np.abs(X3 - X33)> sens
        or np.abs(X3_ref - X33_ref)> sens):
        X33 = float(lockin1.query("OUTP?1"))
#        Y11 = float(lockin1.query("OUTP?2"))
        X33_ref = float(lockin2.query("OUTP?1"))
#        Y22 = float(lockin2.query("OUTP?2"))
        time.sleep(5) #additional wait time
        X3 = float(lockin1.query("OUTP?1"))
        Y3 = float(lockin1.query("OUTP?2"))
        X3_ref = float(lockin2.query("OUTP?1"))
        Y3_ref = float(lockin2.query("OUTP?2"))     
    t = float(time.time()-t0)
    timeCon = int(lockin1.query('OFLT?'))
    SENS = int(lockin1.query('SENS?'))
    line = str(datetime.now()) + " " + str(t) + " " \
    + str(timeCon) + " " + str(SENS) + " "  \
    + str(f1) + " " + str(f2) + " "  \
    + str(X3) + " " + str(Y3) + " "  \
    + str(X3_ref) + " " + str(Y3_ref)
    print(line)
    with open(FILENAME, 'a') as output:
        output.write(line + '\n')

### frequency swap ### 
#sweep n(=num_pts) equally spaced frequency points in log scale from [start, start * 10)
def freqSweep(start,num_pts,sens,initWaitTime):
    try:
        listOfFreq = np.zeros(num_pts)
        for i in np.arange(0,num_pts,1):
            listOfFreq[i] = start * 10**(1 / num_pts * i)
        for i in listOfFreq:
            lockin1.write('FREQ %f' %i)
            if (start < 1):
                error = 0.001
                sleep = 20#waiting for freq sync
            else:
                error = 1
                sleep = 5
            freq1 = float(lockin1.query('freq?'))
            freq2 = float(lockin2.query('freq?'))
            while (np.abs(i - freq1) > error or np.abs(i - freq2) > error):
                time.sleep(sleep)
                freq1 = float(lockin1.query('freq?'))
                freq2 = float(lockin2.query('freq?'))
            #print(i,freq1,freq2)
            measurement(freq1,freq2,sens,initWaitTime)
    except KeyboardInterrupt:
        print('Keyboard Interrupt.')
    finally:
        return
#single freq measurement for f > 1kHz      
def freqSweepSingle(start, sens,initWaitTime):
        lockin1.write('FREQ %f' %start)
        if (start < 1):
            error = 0.01
            sleep = 55#waiting for freq sync
        else:
            error = 1
            sleep = 5#waiting for freq sync
        freq1 = float(lockin1.query('freq?'))
        freq2 = float(lockin2.query('freq?'))
        while (np.abs(start - freq1) > error or np.abs(start - freq2) > error):
            time.sleep(sleep)
            freq1 = float(lockin1.query('freq?'))
            freq2 = float(lockin2.query('freq?'))
        #print(i,freq1,freq2)
        measurement(freq1,freq2,sens,initWaitTime)
        
def outputs_query():
    v = lockin1.query('slvl?').rstrip()
    tc = lockin1.query('oflt?').rstrip()
    s1_x3 = lockin1.query('sens?').rstrip()
    s2_x3 = lockin2.query('sens?').rstrip()
    X3 = lockin1.query('outp?1').rstrip()
    Y3 = lockin1.query('outp?2').rstrip()
    X3_ref = lockin2.query('outp?1').rstrip()
    Y3_ref = lockin2.query('outp?2').rstrip()
    header = "V_input TC SENS_X3 SENS_X1 X3 Y3 X3_ref Y3_ref"
    print(header)
    print(v, tc, s1_x3, s2_x3, X3, Y3, X3_ref, Y3_ref, sep = " ")
    
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

##3w measurement
lockinInit_3w()
lockin1.write("SLVL 0.6")

###freq sweep 0.001-0.01Hz
##timeCon = 17#
##sensitivity = 17# 18 FOR 2V; 14#100 UV;
##lockin_set_pms(timeCon,sensitivity)
##sens = 1e-7
##waitTime = 10*60#s
##freqSweep(0.1,sens,waitTime)
#
##freq sweep 0.01-0.1Hz
timeCon = 15#
sensitivity = 21# 18 FOR 2V; 14#100 UV;
lockin_set_pms(timeCon,sensitivity)
sens = 1e-6
waitTime = 30*60#s
freqSweep(0.01,5, sens,waitTime)
#
###freq sweep 0.1-1Hz
timeCon = 14#
sensitivity = 21# 18 FOR 2V; 14#100 UV;
lockin_set_pms(timeCon,sensitivity)
sens = 1e-6
waitTime = 20*60#s
freqSweep(0.1,10, sens,waitTime)
#
###freq sweep 1-10Hz
timeCon =  13#
sensitivity = 21#
lockin_set_pms(timeCon,sensitivity)
sens = 1e-6#0.1e-3V
waitTime = 20*60#s
freqSweep(1,10, sens,waitTime)
##
##freq sweep 10-100Hz
timeCon = 11#
sensitivity = 21#500uV
lockin_set_pms(timeCon,sensitivity)
sens = 1e-6#0.01e-3#V
waitTime = 10*60#s
freqSweep(10,5, sens,waitTime)

#freq sweep 100-1000Hz
#timeCon = 11#
#sensitivity = 12# 500 uV
#lockin_set_pms(timeCon, sensitivity)
##lockinsingle_set_pms(lockin2, timeCon, 25)
#sens = 1e-7#0.001e-3#V
#waitTime = 5*60#s
#freqSweep(100,sens,waitTime)
#
##freq sweep 1000-10000Hz
#timeCon = 7#0.3s
#sensitivity = 16#0.2mV
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7#V
#waitTime = 3*60#s
#freqSweep(1000,sens,waitTime)
#
##freq sweep for f>10KHz
#timeCon = 7#0.3s
#sensitivity = 16#0.2mV
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7#V
#waitTime = 3*60#s
#freqSweepSingle(10000, sens, waitTime)
#freqSweepSingle(15000, sens, waitTime)
#freqSweepSingle(20000, sens, waitTime)
#freqSweepSingle(25000, sens, waitTime)
#freqSweepSingle(30000, sens, waitTime)
#
lockin1.write('freq 17')
lockin1.write("SLVL 0.004")
lockinInit_1w()
#fg.write("OUTE0") #fg output off
#C
output.close()# may record unfinished data
tf = datetime.now()
print ("Program done! total time is: "+ str(tf-ti))
