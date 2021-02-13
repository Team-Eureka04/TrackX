import requests
import json
def send_data():
    API_ENDPOINT = "http://localhost:5000/employee/add"
    post_data = {
            "process" : "script.py - Nishit Patel - Visual Studio Code",
            "timestamp": "2021, 2, 13, 14, 57, 26, 532165",
            "ip" : "219.90.100.25",
            "name" : "code, Code" ,
            "city" : "Mumbai",
            "country" : "IN",
            "key" : "23985844",
            "timespent" : "5 mins",
            "lat" : 19.0728,
            "long" : 72.8826,
            "id" : 3
        }
    new_Data = {
        "name": "patel",
        "id": 10,
        "location": "ghatkopar"
    }        
    r = requests.post(url = "http://localhost:5000/employee/add", json=json.dumps(new_Data,indent=4))
    print(r.status_code)

send_data()