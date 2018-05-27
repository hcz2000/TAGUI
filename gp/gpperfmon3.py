#!/usr/bin/python

import psycopg2
import time
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib import animation


fig=plt.figure()
ax=fig.add_subplot(111)

def getData(starttime):
    conn = psycopg2.connect(database="gpperfmon", user="gpmon", password="gpmon", host="192.168.3.5", port="5432")
    cur=conn.cursor()
    cur.execute("SELECT hostname,ctime,mem_total,mem_used,mem_actual_used,mem_actual_free,cpu_sys,cpu_user,cpu_idle  from system_history where hostname='TFSVR1' and  ctime >'"+starttime+"' order by ctime asc")
    data=[r for r in cur]
    frame=DataFrame(data)
    cur.close()
    conn.close()
    return frame

start_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-300))
frame=getData(start_time)
times=frame[1]
cpu_usr=frame[7]
line, =ax.plot(times,cpu_usr)

def update_data(frame):
    times=frame[1]
    cpu_usr=frame[7]
    print(times.min(),times.max())
    ax.set_xlim(times.min(), times.max())
    ax.set_ylim(0,cpu_usr.max())
    ax.figure.canvas.draw()
    line.set_data(times.tolist(),cpu_usr.tolist())
    return line,

def data_gen():
    while True:  
        start_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-300))
        frame=getData(start_time)
        yield frame
	

ani = animation.FuncAnimation(fig,update_data,data_gen,interval=5*1000) 
plt.show()
