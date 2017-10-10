#!/usr/bin/python3
 
from matplotlib.pylab import *
 
from numpy import arange
 
import sys, os, serial, threading
 
# example command line ./Capture.py /dev/ttyACM0 june30test1.csv
 
if (len(sys.argv) < 3):
 
    print("Usage: Capture.py serialport outputFile")
 
    sys.exit(127)
 
 
 
 
#define function to draw state of charge
 
def graph_SOC(s):
 
    fig, ax = subplots(figsize=(8,5))
 
    for x in range(0,len(s)):
 
        s[x]=int((s[x].split('%',1))[0],10)
 
     
 
    ax.bar(arange(1.5, len(s)+1.5), s, 0.5, label='state_of_charge(%)', color='k');
 
    ax.set_ylabel("state_of_charge(%)", fontsize=12)
 
    ax.legend(loc=2, frameon=False, fontsize=10)
 
    ax.set_ylim=(0,100)
 
    xlabel("numbers indicating SOC change")
 
    show()
 
 
 
 
#define function to draw capacity
 
def capcity_scratch(c,T):
 
    #c=["222 / 1091 mAh","848 / 1091 mAh","999 / 1091 mAh","1091 / 1091 mAh"]
 
    full_capacity=(c[0].split("/",1))[1].split("mAh",1)
 
    full_capacity=int(full_capacity[0],10)
 
    for x in range(0,len(c)):
 
        c[x]=int((c[x].split('/',1))[0],10)
 
    #plot data
 
    plot(T, c, linestyle="dashed", marker="o", color="green")
 
    #configure  X axes
 
    #xlim(0.5,100)
 
    xticks(T)
 
    #configure  Y axes
 
    ylim(0,full_capacity)
 
    yticks(c)
 
    #labels
 
    xlabel("time")
 
    ylabel("capacity increase out of %s mAh"%full_capacity)
 
    #title
 
    title("Capacity plot")
 
    #show plot
 
    show()
 
     
 
def Voltage_scratch(c,T):
 
    #c=["4155 mV","4155 mV","4155 mV","4155 mV"]
 
    for x in range(0,len(c)):
 
        c[x]=int((c[x].split('mV',1))[0],10)
 
    #plot data
 
    plot(T, c, linestyle="dashed", marker="o", color="green")
 
    #configure  X axes
 
    #xlim(0,100)
 
    xticks(T)
 
    #configure  Y axes
 
    ylim(3000,4500)
 
    yticks(c)
 
    #labels
 
    xlabel("time")
 
    ylabel("battery voltage (charging)/mV")
 
    #title
 
    title("Voltage plot")
 
    #show plot
 
    show() 
 
     
 
def Current_scratch(c,T):
 
    #c=["473 mA","473 mA","473 mA","473 mA"]
 
    for x in range(0,len(c)):
 
        c[x]=int((c[x].split('mV',1))[0],10)
 
    #plot data
 
    plot(T, c, linestyle="dashed", marker="o", color="green")
 
    #configure  X axes
 
    #xlim(0,100)
 
    xticks(T)
 
    #configure  Y axes
 
    ylim(0,500)
 
    yticks(c)
 
    #labels
 
    xlabel("time")
 
    ylabel("Average_current_draw (charging)/mA")
 
    #title
 
    title("Current plot")
 
    #show plot
 
    show()
 
 
 
 
def Average_power_scratch(c,T):
 
    #c=["1965 mW ","1965 mW ","1965 mW ","1965 mW "]
 
    for x in range(0,len(c)):
 
        c[x]=int((c[x].split('mW',1))[0],10)
 
    #plot data
 
    plot(T, c, linestyle="dashed", marker="o", color="green")
 
    #configure  X axes
 
    #xlim(0,100)
 
    xticks(T)
 
    #configure  Y axes
 
    #ylim(0,500)
 
    yticks(c)
 
    #labels
 
    xlabel("time")
 
    ylabel("Average_power_draw_on_the_battery/mW")
 
    #title
 
    title("Power plot")
 
    #show plot
 
    show()
 
 
 
 
#1.2 because max time between lines 1 sec
 
ser = serial.Serial(sys.argv[1], 115200, timeout=1.2)
 
filename = sys.argv[2]
 
run = True
 
if (os.path.isfile(filename)):
 
    cwd=os.getcwd()
 
    print(cwd)
 
    os.listdir(cwd)
 
    print("FILE EXISTS, APPENDING")
 
# Print a header. Should correspond to stuff printed later
 
# Print initial zeroes for data before first valid line
 
outFile = open(sys.argv[2], "a") #a for appending mode
 
header="state-of-charge (%) | battery voltage (mV) | average current draw from the battery (mA) |  remaining and full capacities (mAh) |  average power draw on the battery (mW) |  the battery state-of-health (%) | number of milliseconds/1000"
 
outFile.write(header)
 
outFile.write("\n")
 
State_of_charge=[]
 
Battery_voltage=[]
 
Average_current_draw =[]
 
Remaining_wt_full_capacities=[]
 
Average_power_draw_on_the_battery=[]
 
The_battery_state_of_health=[] 
 
time=[]
 
print(header)
 
while (run):
 
   #print("\r", end='', flush=True)
 
   line = ser.readline().decode('utf-8')
 
   try:
 
     if (line != ""):
 
         # Write raw acquired data
 
         print(line)
 
         outFile.write(line)
 
         parsedline=line.split("|",7)
 
         State_of_charge.append(parsedline[0])
 
         Battery_voltage.append(parsedline[1])
 
         Average_current_draw.append(parsedline[2])
 
         Remaining_wt_full_capacities.append(parsedline[3])    
 
         Average_power_draw_on_the_battery.append(parsedline[4])
 
         The_battery_state_of_health.append(parsedline[5])
 
         time.append(parsedline[6])
 
         # condition for the graphing
 
         a=parsedline[0]
 
         a=int((a.split('%',1))[0],10)
 
         if a>=97:
 
            graph_SOC(State_of_charge)
 
            capcity_scratch(Remaining_wt_full_capacities,time)
 
            Voltage_scratch(Battery_voltage,time)
 
            Current_scratch(Average_current_draw,time)
 
            Average_power_scratch(Average_power_draw_on_the_battery,time)
 
            initial=The_battery_state_of_health[0]
 
            final=The_battery_state_of_health[len(The_battery_state_of_health)-1]
 
            print("The_battery_state_of_health at start: "+initial)
 
            print("The_battery_state_of_health at end: "+final)
 
            continue
 
   except:
 
        # Ignore messed up lines (such as header, partial lines when connecting, etc). They still get written to the file though.
 
        pass
 
outFile.close()