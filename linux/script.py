import subprocess
import csv
import datetime
import os
import time
import re
import json
import urllib.request


def get_location():

    url = 'http://ipinfo.io/json'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    remove = ['region','org','postal','timezone','readme']
    for i in remove:
        data.pop(i)
    return data
    


def get_current_data():
    
    xid_proc = subprocess.Popen("xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2", shell=True, stdout=subprocess.PIPE).stdout
    xid = xid_proc.read().decode().split('\n')[0]

    data_proc = subprocess.Popen(f"xprop -id {xid} _NET_WM_NAME _NET_WM_PID WM_CLASS _NET_WM_USER_TIME", shell=True, stdout=subprocess.PIPE).stdout
    data_str = data_proc.read().decode().split('\n')

    data = {'xid': xid, 'date': datetime.datetime.now()}
    for d in data_str:
        if d:
            kv = d.split('=') if '=' in d else d.split(':')
            key = kv[0].strip()
            value = kv[1].strip()
            data[key] = value.replace('"', '')


    pid = int(data['_NET_WM_PID(CARDINAL)'])
    cmd_proc = subprocess.Popen(f"ps -p {pid} -o comm=", shell=True, stdout=subprocess.PIPE).stdout
    data['cmd'] = cmd_proc.read().decode().split('\n')[0]
    data.update(get_location())
    return data 

if __name__ == '__main__':
    data = get_current_data()
    print(data)
