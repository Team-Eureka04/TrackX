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

    time.sleep(5)
    
    xid_proc = subprocess.Popen("xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2", shell=True, stdout=subprocess.PIPE).stdout
    xid = xid_proc.read().decode().split('\n')[0]

    data_proc = subprocess.Popen(f"xprop -id {xid} _NET_WM_NAME WM_CLASS _NET_WM_USER_TIME", shell=True, stdout=subprocess.PIPE).stdout
    data_str = data_proc.read().decode().split('\n')

    data = {'date': datetime.datetime.now()}
    for d in data_str:
        if d:
            kv = d.split('=') if '=' in d else d.split(':')
            key = "key"
            if "_NET_WM_NAME" in kv[0].strip():
                key = "process-name"
            elif "WM_CLASS" in kv[0].strip():
                key = "Name"
            elif kv[0].strip() == "_NET_WM_USER_TIME":
                key = "time"
            value = kv[1].strip()
            data[key] = value.replace('"', '')

    data.update(get_location())
    return data 

def send_data(data):
    print(data)

    

if __name__ == '__main__':
    data = get_current_data()
    send_data(data)
