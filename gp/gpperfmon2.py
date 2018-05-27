#!/usr/bin/python
import psycopg2
import time
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib import animation 

def getData(starttime):
    conn = psycopg2.connect(database="gpperfmon", user="gpmon", password="gpmon", host="192.168.3.5", port="5432")
    cur=conn.cursor()
    cur.execute("SELECT hostname,ctime,mem_total,mem_used,mem_actual_used,mem_actual_free,cpu_sys,cpu_user,cpu_idle  from system_history where hostname='TFSVR1' and  ctime >'"+starttime+"' order by ctime asc")
    data=[r for r in cur]
    frame=DataFrame(data)
    cur.close()
    conn.close()
    return frame

def plot(frame):
    fig=plt.figure()
    times=frame[1]
    cpu_usr=frame[7]
    plot_curve(fig,111,"CPU Curve","time","usage",times,cpu_usr)
    plt.subplots_adjust(bottom=0.13,top=0.95)
    plt.legend('daily')
    plt.grid(True)
    plt.show()

def plot_curve(figure,subno,title,xlabel,ylabel,x,y):
    ax=figure.add_subplot(subno)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax.xaxis.set_major_locator(dates.MinuteLocator(byminute=range(60), interval=10))
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    line, =ax.plot(x,y)
    ani = animation.FuncAnimation(fig=figure,func=update_data,init_func=update_data,interval=20*1000,blit=False) 


def update_data(i):
    start_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-7200))
    frame=getData(start_time)
    times=frame[1]
    cpu_usr=frame[7]
    line.set_ydata(cpu_user)
    line.set_xdata(times)
    return line
	
def main():
    start_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-7200))
    frame=getData(start_time)
    plot(frame)
