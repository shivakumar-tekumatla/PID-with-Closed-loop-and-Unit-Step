"""
Time Series response of a closed loop control system with P,I, PI , PD and PID Controls under unit step signal input


Input                                                  Output
-->---(+-)--->--[Controller]--->---[Actuator+Plant]----->------
        |                                            |
        |____________________________________________| 

Give Actuator+Plant input to this program in the val_update() function.

The Values of Proportional, Integral and Differential Gains can be changed using the Sliders. 

If the input is a 1st order system , then the Time constant can also be changed using a Slider. 

If you wish to view only specific plots , please select or unselect the legends(you can click on the legend color to do this)


"""

import matplotlib.pyplot as plt
import pandas
from matplotlib.widgets import Slider
import control as ctl 
from control.matlab import step
from control.matlab.timeresp import stepinfo 
import numpy as np


def scaling_func():
    #This function automatically sets the axes ranges

    legend_logic = {"P":(p,p.get_visible()),"I":(i,i.get_visible()),"PI":(pi,pi.get_visible()),"PD":(pd,pd.get_visible()),"PID":(pid,pid.get_visible())}
    x_max=0
    y_max=0
    for key in legend_logic:
        if legend_logic[key][1]:
            x,y=legend_logic[key][0].get_data()
            # print(x)
            if x.max() > x_max:
                x_max= x.max()
            else:
                pass
            if y.max()>y_max:
                y_max=y.max()

    ax.set_xlim(0,x_max)
    ax.set_ylim(0,y_max+0.2)
    
def plant_with_controller(plant,contr_part,name,plt_id):
    contr_Plant =  ctl.feedback(contr_part*plant)
    res,t = step(contr_Plant)
    time_data = stepinfo(contr_Plant)
    time_data["Controller"] = name
    plt_id.set_ydata(res)
    plt_id.set_xdata(t)

    return time_data

def slider_gains():
    Kp = Kp_Slider.val
    Ki = Ki_Slider.val 
    Kd = Kd_Slider.val
    Tc = Tc_Slider.val
    print("_"*100)
    print("Proportonal Gain:",Kp)
    print("Integral Gain :",Ki)
    print("Differential Gain",Kd)
    print("Time Constant:",Tc)
    print("_"*100)

    return Kp,Ki,Kd,Tc

def val_update(val):
    time_res_char = pandas.DataFrame()
    Kp,Ki,Kd,Tc=slider_gains()

    P = Kp  # Controller out = Kp * Error

    I = Ki/s # Controller out = Ki * Error Ki = Kp/Ti - Ti is called Itegral Time and 1/Ti is called reset rate
    D= Kd*s # Controller out = Kd * Error Kd = Kp*Td - Td is called derivative time

    """
    Specify the plant here.
    If you are giving the 1st order system , give it in the below format.
    first order system = 1/ (Tc*s+1) . Tc is called as Time Constant. It can be varied with the Slider

    """
    plant = 0.085/(0.00225*(s**2)+0.05075*s+0.034725)  # Specify the plant input here
    # plant = 1/(Tc*s+1)

    #With PID Controller
    time_data= plant_with_controller(plant,P+I+D,"PID",pid)
    time_res_char = time_res_char.append(time_data,ignore_index=True)

    #With P controller
    time_data= plant_with_controller(plant,P,"P",p)
    time_res_char = time_res_char.append(time_data,ignore_index=True)

    #With I Controller
    time_data= plant_with_controller(plant,I,"I",i)
    time_res_char = time_res_char.append(time_data,ignore_index=True)

    #With PI Controller
    time_data= plant_with_controller(plant,P+I,"PI",pi)
    time_res_char = time_res_char.append(time_data,ignore_index=True)
    
    #With PD Controller
    time_data = plant_with_controller(plant,P+D,"PD",pd)
    time_res_char = time_res_char.append(time_data,ignore_index=True)

    time_res_char=time_res_char.set_index("Controller")
    print("Time Response Charecteristics:")
    print(time_res_char)
    print("*"*100)
    scaling_func()

    plt.draw()

#On selecting or unselecting the legend, the plot data will be updated. 
def onpick(event):
    global x
    # on the pick event, find the orig line corresponding to the
    # legend proxy line, and toggle the visibility
    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    # alpha value is to differetiate between select and unselect
    if vis:
        legline.set_alpha(1)
    else:
        legline.set_alpha(0.3)

    scaling_func()
    fig.canvas.draw()


if __name__ == "__main__":
    s = ctl.tf("s")
    
    fig,ax = plt.subplots()
    plt.subplots_adjust(left = 0.1,bottom=0.4,right=0.9)


    p,=plt.plot(0,0,color="blue",lw=2,label="P")
    i,=plt.plot(0,0,color="violet",lw=2,label="I")
    pi,=plt.plot(0,0,color="black",lw=2,label="PI")
    pd,=plt.plot(0,0,color="red",lw=2,label="PD")
    pid,=plt.plot(0,0,color="green",lw=2,label="PID")
    ref_signal = plt.axhline(y=1,color="grey",lw=3,label="Ref",linestyle="--")


    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Response')
    plt.title('Closed loop control system with various feedback controls')
    plt.grid(b=True, which='major', axis='both')
    leg = ax.legend(loc = "upper right", fancybox=True, shadow=True)
    leg.get_frame().set_alpha(0.4)

    #Sliders' Positions
    axSliderKp = plt.axes([0.1,0.3,0.8,0.05])
    axSliderKi =plt.axes([0.1,0.2,0.8,0.05])
    axSliderKd =plt.axes([0.1,0.1,0.8,0.05])
    axSliderTimeConst = plt.axes([0.95,0.4,0.04,0.5])

    #Slider Settings 
    Kp_Slider = Slider(axSliderKp,"Kp",valmin =0,valmax=200,valinit=5.5,valfmt = "%1.1f",valstep=0.1,color="cyan",closedmin=False)
    Ki_Slider = Slider(axSliderKi,"Ki",valmin =0,valmax=20,valinit=2.4,valfmt = "%1.2f",valstep=0.01,color="magenta",closedmin=False)
    Kd_Slider = Slider(axSliderKd,"Kd",valmin =0,valmax=10,valinit =8.2,valfmt = "%1.2f",valstep=0.01,color ="yellow",closedmin=False)
    Tc_Slider = Slider(axSliderTimeConst,"Tc",valmin =0.0001,valmax=100,valinit =1,valfmt = "%1.5f",valstep=0.01,color ="orange",closedmin=True,orientation='vertical')

    #This part is to enable the selecting and unselecting the graphs from the legends. By default all the graphs are enabled
    lines = [p,i,pi,pd,pid]
    lined = dict()
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(5)  
        lined[legline] = origline
        
    # Calling the onpick function once the legends are clicked
    fig.canvas.mpl_connect('pick_event', onpick) 

    # calling the val_update func if the sliders are moved
    Kp_Slider.on_changed(val_update)
    Ki_Slider.on_changed(val_update)
    Kd_Slider.on_changed(val_update)
    Tc_Slider.on_changed(val_update)
    

    plt.show()