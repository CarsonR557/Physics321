# Exercise 6, hw3, brute force way with declaration of vx, vy, x and y
# Common imports
import numpy as np
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import os

# Where to save the figures and data files
PROJECT_ROOT_DIR = "Results"
FIGURE_ID = "Results/FigureFiles"
DATA_ID = "DataFiles/"

if not os.path.exists(PROJECT_ROOT_DIR):
    os.mkdir(PROJECT_ROOT_DIR)

if not os.path.exists(FIGURE_ID):
    os.makedirs(FIGURE_ID)

if not os.path.exists(DATA_ID):
    os.makedirs(DATA_ID)

def image_path(fig_id):
    return os.path.join(FIGURE_ID, fig_id)

def data_path(dat_id):
    return os.path.join(DATA_ID, dat_id)

def save_fig(fig_id):
    plt.savefig(image_path(fig_id) + ".png", format='png')


from pylab import plt, mpl
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'


g = 9.80655 #m/s^2
# Note that we bake inn the mass in D
D = 0.00245 #m/s
DeltaT = 0.01
#set up arrays 
tfinal = 1.4
n = ceil(tfinal/DeltaT)
# define scaling constant vT
vT = sqrt(g/D)
# set up arrays for t, a, v, and y and we can compare our results with analytical ones
#brute force setting up of arrays for x and y
t = np.zeros(n)
ax = np.zeros(n)
ay = np.zeros(n)
vy = np.zeros(n)
y = np.zeros(n)
vx = np.zeros(n)
x = np.zeros(n)
xanalytic = np.zeros(n)
yanalytic = np.zeros(n)
# Initial conditions
vx[0] = 10.0 #m/s
vy[0] = 0.0  #m/s
y[0] = 10.0 #m
x[0] = 0.0 #m
yanalytic[0] = y[0]
xanalytic[0] = x[0]
# Start integrating using Euler's method
for i in range(n-1):
    # expression for acceleration
    ax[i] = -D*vx[i]*abs(vx[i])
    ay[i] = -g - D*vy[i]*abs(vy[i])
    # update velocity and position
    x[i+1] = x[i] + DeltaT*vx[i]
    vx[i+1] = vx[i] + DeltaT*ax[i]
    y[i+1] = y[i] + DeltaT*vy[i]
    vy[i+1] = vy[i] + DeltaT*ay[i]
    # update time to next time step and compute analytical answer
    t[i+1] = t[i] + DeltaT
    yanalytic[i+1] = y[0]-(vT*vT/g)*log(cosh(g*t[i+1]/vT))
    xanalytic[i+1] = log(1.+t[i+1]*vx[0]*D)/D
    if ( y[i+1] < 0.0):
        break
ay[n-1] = -g + D*vy[n-1]*vy[n-1]
ax[n-1] = -D*vx[n-1]*vx[n-1]
data = {'t[s]': t,
        'Relative error in y': abs((y-yanalytic)/yanalytic),
        'vy[m/s]': vy,
        'ay[m/s^2]': ay,
        'Relative error in x': abs((x-xanalytic)/xanalytic),
        'vx[m/s]': vx,
        'ax[m/s^2]': ax
}
NewData = pd.DataFrame(data)
display(NewData)


fig, axs = plt.subplots(3, 1)
axs[0].plot(t, y)
axs[0].set_xlim(0, tfinal)
axs[0].set_ylabel('y')
axs[1].plot(t, vy)
axs[1].set_ylabel('vy[m/s]')
axs[2].plot(t, ay)
axs[2].set_xlabel('time[s]')
axs[2].set_ylabel('ay[m/s^2]')
fig.tight_layout()
save_fig("YEulerIntegration")
plt.show()


fig, axs = plt.subplots(3, 1)
axs[0].plot(t, x)
axs[0].set_xlim(0, tfinal)
axs[0].set_ylabel('x')
axs[1].plot(t, vx)
axs[1].set_ylabel('vx[m/s]')
axs[2].plot(t, ax)
axs[2].set_xlabel('time[s]')
axs[2].set_ylabel('ax[m/s^2]')
fig.tight_layout()
save_fig("XEulerIntegration")
plt.show()


