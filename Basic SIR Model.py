
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from matplotlib.widgets import Slider

#plt.style.use(["science", "notebook"])

inf = 0.15 #infection rate
rem = 0.02 #removal rate

Time_limit = 150

S_0 = 0.99   #initial percentage of susceptable
I_0 = 0.01   #initial percentage of infected
R_0 = 0      #initial percentage of removed

T_0 = (S_0, I_0, R_0)

#==========================================================================================================================

def dTdx(T, x):
    S, I, R = T
    return [-inf * I * S, #1st eq   
            inf * I * S - rem * I, #2nd eq
            rem * I] #3rd eq

x = np.linspace(0, Time_limit, 1000) #domain

sol = odeint(dTdx, T_0, x) #solves all 3 equations given the damin and intial conditions

#===-plots-=======================================================================================================================

fig, ax = plt.subplots(figsize = (8,5)) #figsize just sets the aspect ratio; messing with this is recommended

plt.subplots_adjust(left=0.162, bottom=0.188,
                    right = 0.905, top = 0.907) #this just adjusts the sliders so that it doesnt intersect with the plot.

S = sol.T[0] #data for susceptable
I = sol.T[1] #data for infected
R = sol.T[2] #data for removed

sus, = ax.plot(x, S, color = "b", label = "Suscptable")

infec, = ax.plot(x, I, color = "r", label = "Infectious")

remov, = ax.plot(x, R, color = "g", label = "Removed") #we need to name each graph so that we can properly change its values later

plt.xlabel("Time[days]"
           , fontsize = "medium")

plt.ylabel("Percent of population[%]"
           , fontsize = "medium")

plt.title("Basic SIR Model")
plt.grid()
plt.legend(loc = "center right", fancybox = True,
           framealpha=0.50, fontsize = "medium") #loc locks the legend inn a specific location;
                                                 #this is so that it doesnt move when the plot moves

#===-sliders-=======================================================================================================================

ax_slide1 = plt.axes( [0.25, 0.05,
                      0.65, 0.035] )

ax_slide2 = plt.axes( [0.05, 0.25,  #these two can be used to control the slider's position
                      0.025, 0.65] )


infection = Slider(ax_slide1,
                  label = 'infection rate',
                  valmin = 0,
                  valmax = 1,
                  valinit = inf,
                  valstep = 0.001
                  )


removal = Slider(ax_slide2,  #values defining its position, length, and width
              label = 'Removal rate',  #label
              valmin = 0,  #minimum value
              valmax = 0.05,  #maximum value
              valinit = rem,  #name of the variable being changed
              valstep = 0.0001,  #step when moving the slider
              orientation = "vertical"  #orientation; default is horizontal
              )


def update(val): #this is the function that updates the plot with the new values
    
    inf = infection.val
    rem = removal.val #the new value of the variable is the slider's current value
    
    def dTdx(T, x):
        S, I, R = T
        return [-inf * I * S,
                inf * I * S - rem * I,
                rem * I]

    x = np.linspace(0,150,1000)
    sol = odeint(dTdx, T_0, x)

    sus.set_ydata(sol.T[0])
    
    infec.set_ydata(sol.T[1])
    
    remov.set_ydata(sol.T[2]) # this part replaces the data of the y-axis in each graph with the new, updated values
    
    fig.canvas.draw() #no idea what this does; probably implemments all the new values. maybe something to do with Tkinter?


 
infection.on_changed(update)
removal.on_changed(update) #slider doesn't work without this. calls update(val) whenever the slider is changed (I think)

#==========================================================================================================================

plt.show()
