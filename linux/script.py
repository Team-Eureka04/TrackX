import subprocess
import csv
import datetime
import os
import time
import re
import json
import urllib.request
import requests
import math


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

    data_proc = subprocess.Popen(f"xprop -id {xid} _NET_WM_NAME WM_CLASS _NET_WM_USER_TIME _NET_WM_PID", shell=True, stdout=subprocess.PIPE).stdout
    data_str = data_proc.read().decode().split('\n')

    data_time = datetime.datetime.now().strftime("%H:%M:%S")
    data = {'date': data_time}
    for d in data_str:
        if d:
            kv = d.split('=') if '=' in d else d.split(':')
            key = "key"
            if "_NET_WM_NAME" in kv[0].strip():
                key = "process-name"
            elif "WM_CLASS" in kv[0].strip():
                key = "Name"
            elif "_NET_WM_USER_TIME" in kv[0].strip():
                key = "time"
            elif "_NET_WM_PID" in kv[0].strip():
                key = "pid"
            value = kv[1].strip()
            data[key] = value.replace('"', '')
    data.update(get_location())
    return data 


def append_row(filename, data):
    
    row = [data['date'], data['process-name'], data['Name'], data['time'], data['ip'], data['city'], data['loc'], data['pid']]
    
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    csv_dir_name = 'csv_data'
    script_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists( os.path.join( script_path, csv_dir_name) ):
        os.mkdir( os.path.join( script_path, csv_dir_name) )
    filepath = os.path.join( script_path, csv_dir_name, f'{filename}-{today}.csv' )

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(['Date', 'process-name', 'Name', 'time', 'ip', 'city','loc','pid'])

    with open(filepath, 'a') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(row)



def send_data(data):
    API_ENDPOINT = "http://localhost:5000/add/data"
    print(data)
    post_data = {
            "process" : data['process-name'],
            'process_id' : data['pid'],
            'timestamp' : data['date'],
            'ip' : data['ip'],
            'name' : data['Name'],
            'city' : data['loc'],
            'country' : data['country'],
            'timespent' : data['time'],
            'lat' : "124532",
            'long' : "1343532",
            'id' : 2
        }
    r = requests.post(url = API_ENDPOINT, json=json.dumps(post_data))
    

if __name__ == '__main__':
    data = get_current_data()
    append_row('demo', data)
    send_data(data)
    
