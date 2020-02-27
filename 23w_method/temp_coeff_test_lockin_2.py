# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 12:09:07 2018

@author: Administrator
"""

import datetime as dt
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import visa
import os

rm = visa.ResourceManager()
rm.list_resources()
rtd = rm.open_resource('GPIB2::2::INSTR')
samp1 = rm.open_resource('GPIB2::9::INSTR')
samp2 = rm.open_resource('GPIB2::18::INSTR')

date = '200227'
try:
    os.mkdir(date)
except FileExistsError:
    pass    

FILENAME = date + '//' + date + '_' +"23w_glass_R1718_R1516_temp_coeff_1.txt"
#output = open(FILENAME,"w");
with open(FILENAME, "w") as output:
    output.write("Date_Time,RTD,Vsamp1(R1718),Vsamp2(R1516)\n")

#init();
##use fg to give a 5V DC heating
#fg.write("FUNC 0")
#fg.write('ampl0vr')
#fg.write('offs 5')
#fg.write("OUTE1") # fg output on

ti = dt.datetime.now()

#constants
#samp.write('SLVL2.276')
#V = 2.276 #lockin voltage
#Rref = 310.9e3 #large resistor to convert to current source
#I = V/Rref

try:
    while True:
        ans1 = float( rtd.query(":sens:data:fres?"))
        #ans2 = float( rtdr.query(":sens:data:fres?"))
        ans2 = float( samp1.query("OUTP?1"))
        ans3 = float( samp2.query("OUTP?1"))
        line = str(dt.datetime.now()) + "," \
                     + str(ans1) + ","  \
                     + str(ans2) +  ","  \
                     + str(ans3) #+  " "  \
#                     + str(ans4)
        with open(FILENAME, "a") as output:             
            output.write(line + "\n")
        print(line)
        time.sleep(0.5)
except KeyboardInterrupt:  
    pass
finally:
    tf = dt.datetime.now()
    print ("Program done! total time is: "+ str(tf-ti))


