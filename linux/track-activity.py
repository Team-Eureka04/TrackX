from crontab import CronTab
import click
import os
import json
import requests
import math as m
import time

def set_crontab_task():
    cron = CronTab(user=True)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'script.py')
    print(path)
    if path in cron.crons:
        print("job already present")
    else:
        cmd = f'env DISPLAY=:0 python3 {path}'
        job = cron.new(command= cmd)
        cron.write()
        print("job setup finished!")

@click.command()
@click.option('--time', default=1, help='Number of days')
@click.option('--sendmail',is_flag=True,help='Mail will be sent if the user!')
def trackx(time,sendmail):
    """Trackx is the program which tracks your"""
    if sendmail:
        click.echo("Mail will be sent!")
    if time > 1:
        click.echo(f'You have set time as {time}')
    set_crontab_task()

def send_data():
    API_ENDPOINT = "http://localhost:5000/add/data"
    post_data = {
            "process" : "script.py  Nishit Patel  Visual Studio Code",
            "timestamp": "2021, 2, 13, 14, 57, 26, 532165",
            "ip" : "219.90.100.25",
            "name" : "code, Code" ,
            "city" : "Mumbai",
            "country" : "IN",
            "key" : "23985844",
            "timespent" : "5 mins",
            "lat" : 19.0728,
            "long" : 72.8826,
            'id' : m.floor(time.time()) 
        }

    r = requests.post(url = "http://localhost:5000/add/data", json=json.dumps(post_data))
    print(r.text)

if __name__ == '__main__':
    set_crontab_task()