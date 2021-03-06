# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:30:51 2019

@author: CRYOGENIC
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
from IPython import get_ipython
mgc = get_ipython().magic
mgc(u'%matplotlib qt')

font = {'size'   : 7}
matplotlib.rc('font', **font)
style.use('fivethirtyeight')
colors = ['b', 'g']
interval = 1000

#fnames = ['results/GaGdN-300K-190809_001.dat',
#          'results/GaGdN-300K-190809_002.dat']
fname = '200224//200224_23w_glass_R78_temp_coeff_5.txt'
#Rref = 12.64

#x_column = 'B_digital'
#y_column = 'V_real_12'
#x_columns = ['B_digital', 'B_digital']#, 'B_digital']
#y_columns = ['V_real_8', 'V_real_12']#, 'V_real_11']



#def animate(i, ax, fname, x_column, y_column):
#    graph_data = pd.read_csv(fname, skipinitialspace=True)
#    x = graph_data[x_column]
#    y = graph_data[y_column]
#    ax.clear()
#    ax.plot(x,y)
#    plt.xlabel(x_column)
#    plt.ylabel(y_column)
#    plt.tight_layout()
    
def animate_multi(i, axs, fname, color=None):
    for ax in axs:
        ax.clear()
    graph_data = pd.read_csv(fname, sep = ' ', header = 0)
    
    graph_data['TimeDur'] = (pd.to_timedelta(graph_data.Time)-pd.to_timedelta(graph_data.Time[0])).astype('timedelta64[s]');

    graph_data['T'] = 9.91684E-6*graph_data['RTD']**2+0.23605*graph_data['RTD']-245.96823
    #graph_data['Tr'] = 9.91684E-6*graph_data['RTDr']**2+0.23605*graph_data['RTDr']-245.96823
    #graph_data['T_average'] = (graph_data.Tl+graph_data.Tr)/2
  
    axs[0].plot(graph_data['TimeDur'], graph_data['T'], label = 'T')
    #axs[0].plot(graph_data.TimeDur, graph_data.Tr, label = 'Tr')
#    axs[0] = graph_data['RTD'].plot(label = 'T')
    axs[0].set_xlabel('times(s)')
    axs[0].set_ylabel('T(C)')
    axs[0].legend(loc = 'upper right')
    
    axs[1].plot(graph_data['TimeDur'], graph_data['Vsamp'], label = 'Vsamp')
    axs[1].set_xlabel('times(s)')
    axs[1].set_ylabel('V(V)')
    axs[1].legend(loc = 'upper left')
    
    axs[2].plot(graph_data['T'], graph_data['Vsamp'], label = 'alpha')
    axs[2].set_xlabel('Tavg(C)')
    axs[2].set_ylabel('V(V)')
    axs[2].legend(loc = 'lower left')
    
    plt.tight_layout()
  
    '''
def animate_multi_files(i, axs, fnames, x_columns, y_columns, colors=None):
    for ax in axs.flatten():
        ax.clear()
    for fname, color in zip(fnames, colors):
        graph_data = pd.read_csv(fname, skipinitialspace=True)
        for x_column, y_column, ax in zip(x_columns, y_columns, axs[0]):
            x = graph_data[x_column]
            y = graph_data[y_column]
#            ax.clear()
            ax.plot(x,y, color=color)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
        graph_data = graph_data[graph_data['flag'] != 0]
        for x_column, y_column, ax in zip(x_columns, y_columns, axs[1]):
            x = graph_data[x_column]
            y = graph_data[y_column]
#            ax.clear()
            ax.plot(x,y,'x', color=color)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
    plt.tight_layout()
    '''
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#ani = animation.FuncAnimation(fig, animate, fargs=[ax, fname, x_column, y_column], interval=1000)
fig, axs = plt.subplots(3,1, figsize=(8,6))
ani = animation.FuncAnimation(fig, animate_multi, fargs=[axs, fname, colors], interval=interval)
#animate_multi(1,axs,fname,colors)
plt.show()