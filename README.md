# PID-with-Closed-loop-and-Unit-Step
This program plots the Time Series Response of Closed Loop Control System with P, I , PI , PD and PID controls and Units Step Input
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
