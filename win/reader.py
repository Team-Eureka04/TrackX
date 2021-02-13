import csv
import json

#to get the data from the csv files
def get_csv_data(path):
    data = []
    with open(path,'r') as file:
        reader = csv.DictReader(file,delimeter=',')
        lcount = 0
        cols=[]
        for row in reader:
            # entering the column name if the row is 0
            if line_count == 0:
                cols = row
                line_count += 1
            data.append(dict(row))
            line_count += 1
    return data

# to read the json and return its content
def get_json_data(path):
    data={}
    with open(path,'r') as file:
        data=json.load(file)
    return data