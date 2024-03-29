# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:27:47 2020

@author: xueti
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


fname = "201218//201218_glass_R87_R1516_2w_measurement_dry_ice.txt"
graph_data = pd.read_csv(fname, sep = ' ', header = 0,
                         names = ['Date_time','Time','TC','SENS','Lockin1f','Lockin2f','X1','Y1','X2','Y2'])
V1w = np.average(graph_data['X1'].head())
X = graph_data.X2
Y = graph_data.Y2
R = np.sqrt(X**2 + Y**2)
theta = np.arctan(Y/ X)
theta2 = theta.copy()
i = 0;
for i in range(1,len(theta2),1):
    if np.abs(theta2.iloc[i] - theta2.iloc[i - 1]) > np.pi / 2:
        break 
theta2.iloc[i:] = theta2.iloc[i:] - np.pi

result = pd.DataFrame({'freq': graph_data.Lockin1f, 'X2': X, 'Y2' : Y, 'R' : R, 
                       'theta' : theta, 'theta_smooth': theta2,
                       'modified X2' : R * np.cos(theta2  - 90 / 180 * np.pi), 
                       'modified Y2' : R * np.sin(theta2  - 90 / 180 * np.pi)})
result.to_csv(fname[:len(fname)-4] + ".csv", index = False)
#fig, axs = plt.subplots(1,2, figsize=(8,4))
#axs[0].scatter(graph_data.Lockin1f, R * np.cos(theta2  - 90 / 180 * np.pi), label = 'X2')
#axs[0].scatter(graph_data.Lockin2f, R * np.sin(theta2  - 90 / 180 * np.pi), label = 'Y2')
#axs[0].scatter(graph_data.Lockin1f, X, label = 'X2')
#axs[0].scatter(graph_data.Lockin2f, Y, label = 'Y2')

#axs[0].plot(graph_data.Lockin1f, graph_data.X2)
#axs[0].plot(graph_data.Lockin2f, graph_data.Y2)
#axs[0].set_xlabel('f(Hz)')
#axs[0].set_ylabel('V2w(V)')
#axs[0].set_xscale('log')
#axs[0].set_ylim([-300e-6, 300e-6])
##    axs[0].set_xscale('log')
#axs[0].legend(loc = 'upper right')
#
#axs[1].scatter(graph_data.Lockin1f, graph_data.X1, label = 'X1')
#axs[1].scatter(graph_data.Lockin2f, graph_data.Y1, label = 'Y1')
#axs[1].plot(graph_data.Lockin1f, graph_data.X1)
#axs[1].plot(graph_data.Lockin2f, graph_data.Y1)
#
#axs[1].set_xlabel('f(Hz)')
#axs[1].set_ylabel('V1w(V)')
##    axs[1].set_xscale('log')
#axs[1].legend(loc = 'upper right')
#
#plt.tight_layout()

#plt.savefig(fname[:len(fname)-4] + "_phase_-90", dpi = 300)


fig2, axs = plt.subplots(1,2, figsize = (14,6))
fz = 24
axs[0].scatter(graph_data.Lockin1f, graph_data.X2, label = 'X2')
axs[0].scatter(graph_data.Lockin2f, graph_data.Y2, label = 'Y2')
axs[0].set_xlabel('f(Hz)', fontsize = fz)
axs[0].set_ylabel('V(V)', fontsize = fz)
axs[0].set_xscale('log')
axs[0].set_ylim([-300e-6, 300e-6])
axs[0].tick_params(labelsize = 20)
axs[0].legend(loc = 'upper right', fontsize = 20)

axs[1].scatter(graph_data.Lockin1f, R * np.cos(theta2  - 90 / 180 * np.pi), label = 'converted X2')
axs[1].scatter(graph_data.Lockin2f, R * np.sin(theta2  - 90 / 180 * np.pi), label = 'converted Y2')
axs[1].set_xlabel('f(Hz)', fontsize = fz)
axs[1].set_ylabel('V(V)', fontsize = fz)
axs[1].set_xscale('log')
axs[1].set_ylim([-300e-6, 300e-6])
axs[1].tick_params(labelsize = 20)
axs[1].legend(loc = 'upper right', fontsize = 20)

plt.tight_layout()
fig2.savefig(fname[:len(fname)-4] + 'converted.png', dpi = 100)