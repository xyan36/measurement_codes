# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 17:09:06 2020

@author: xueti
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

graph_data = pd.read_csv('200204//200203_04_combined_P_4_power_dep.txt', sep = ' ')
graph_data.loc['2020-02-04','Time'] += 2051
fig, axs = plt.subplots(3,1, figsize = (8,10))
axs[0].scatter(graph_data.V_input, graph_data.X1, label = 'X1')
axs[0].scatter(graph_data.V_input, graph_data.Y1, label = 'Y1')
axs[0].scatter(graph_data.V_input, graph_data.X1_ref, label = 'X1_ref')
axs[0].scatter(graph_data.V_input, graph_data.Y1_ref, label = 'Y1_ref')
axs[0].set_xlabel('V_input(V)')
axs[0].set_ylabel('V1w(V)')
axs[0].legend(loc = 'upper left')

axs[1].scatter(graph_data.V_input, graph_data.X3, label = 'X3')
axs[1].scatter(graph_data.V_input, graph_data.Y3, label = 'Y3')
axs[1].scatter(graph_data.V_input, graph_data.X3_ref, label = 'X3_ref')
axs[1].scatter(graph_data.V_input, graph_data.Y3_ref, label = 'Y3_ref')
axs[1].set_ylim([-10e-5, 20e-5])
axs[1].set_xlabel('V_input(V)')
axs[1].set_ylabel('V3w(V)')
axs[1].legend(loc = 'upper left')
#axs[2].legend(loc = 'lower left')

Rref = 3.5
graph_data['I1w'] = graph_data['X1_ref']/Rref
#X = (graph_data['I1w'].values.reshape(-1,1))**3
#Y = graph_data.X3.values.reshape(-1,1)
#linear_regressor = LinearRegression()
#linear_regressor.fit(X,Y)
#Y_pred = linear_regressor.predict(X)
axs[2].scatter(graph_data['I1w']**3,graph_data.X3, label = 'X3, f = 3.4Hz')
axs[2].scatter(graph_data['I1w']**3,graph_data.Y3, label = 'Y3, f = 3.4Hz')
axs[2].plot(graph_data['I1w']**3,graph_data.X3, label = '')
axs[2].plot(graph_data['I1w']**3,graph_data.Y3, label = '')
#axs[2].plot(X,Y_pred, color = 'red', label = 'linear line')
axs[2].set_xlim([graph_data['I1w'].min()**3, (graph_data['I1w'].max()+0.001)**3])
axs[2].set_ylim([graph_data['X3'].min(), graph_data['Y3'].max()+50e-6])
axs[2].set_xlabel('I1w^3(A^3)')
axs[2].set_ylabel('V3w(V)')
axs[2].legend(loc = 'upper left')
#for i, txt in enumerate(graph_data['I1w']):
#    axs[2].annotate(str(np.around(txt,decimals=3)) + 'A',(X[i],Y[i]),
#    xytext = (X[i]+ -1e-6,Y[i] + 0.00001))

plt.tight_layout()
#plt.savefig('200203//200203_p4_power_dep_f3p4_test5_plot_X3_Y3',dpi = 300)
