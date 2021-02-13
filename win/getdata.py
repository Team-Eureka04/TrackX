from win32gui import GetWindowText, GetForegroundWindow
import datetime
import csv
import os
from time import sleep

#to get current data
def get_current_data():
    open_win = GetWindowText(GetForegroundWindow())
    data={
        "date" : datetime.datetime.now(),
        "open_window" : open_win
    }
    # data["open_window"] = data["open_window"].split("-")
    return data

#to append the row in the csv file
def append_row(data,filename="peek"):
    row = [data["date"],data["open_window"],None]
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    csv_dir_name = "csv_data"
    script_path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists( os.path.join(script_path,csv_dir_name) ):
        os.mkdir( os.path.join(script_path,csv_dir_name) )
    filepath = os.path.join(script_path,csv_dir_name,f'{filename}--{today}.csv')
    if not os.path.exists(filepath):
        with open(filepath,'w') as file:
            csv_writer = csv.writer(file,delimiter=',')
            csv_writer.writerow(['Date','Process','Timeactive'])
    with open(filepath,'a') as file:
        csv_writer = csv.writer(file,delimiter=',')
        csv_writer.writerow(row)

if __name__ == "__main__":
    data = get_current_data()
    append_row(data)