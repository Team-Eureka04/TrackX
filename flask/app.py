from flask import Flask,request,jsonify,abort,render_template, url_for, redirect
from flask_cors import CORS,cross_origin
import sqlite3
import os
import json

FLASK_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(FLASK_ROOT,'db', 'database.db')


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
    with app.app_context():
        return '''<h1>Welcome</h1>'''

@app.route('/admin/signin',methods=['GET','POST'])
def admin_login():
    with app.app_context():
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        if request.json and request.json['username'] and request.json['password']:
            response = {
                'username' : request.json['username'],
                'password' : request.json['password']
            }
        else:
            response = {
                'username' : '',
                'password' : ''
            }
        cur.execute('CREATE TABLE IF NOT EXISTS admin (username char(100) PRIMARY KEY, password char(100) NOT NULL)')
        cur.execute('SELECT * FROM admin')
        data = cur.fetchall()
        if not data:
            cur.execute('INSERT INTO admin (username, password) VALUES ("admin","admin")')
        db.commit()
        cur.execute('SELECT * FROM admin')
        data = cur.fetchall()
        db.close()
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"username : {username} passoword: {password} from post request")
        for admins in data:
            if username == admins[0] and password == admins[1]:
                return redirect(url_for('list_employees'))

        # return jsonify({'success': False}),400
        return render_template('login.html',purpose='Sign In',posturl='/admin/signin')


@app.route('/admin/signup',methods=['GET','POST'])
def admin_signup():
    with app.app_context():
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
       
        if request.json and request.json['username'] and request.json['password']:
            response = {
                'username' : request.json['username'],
                'password' : request.json['password']
            }
        else:
            response = {
                'username' : '',
                'password' : ''
            }
        cur.execute('CREATE TABLE IF NOT EXISTS admin (username char(100) PRIMARY KEY, password char(100) NOT NULL)')
        cur.execute('SELECT * FROM admin')
        data = cur.fetchall()
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"username : {username} passoword: {password} from post request")
        for admin in data:
            if admin[0] == username:
                return jsonify({'success': False,'admin':'already exists'}),400
        if username and password:
            cur.execute('INSERT INTO admin VALUES ("{}","{}")'.format(username, password))
            db.commit()
            db.close()
            return redirect(url_for('list_employees'))
        else:
            return render_template('login.html',purpose='Sign Up',posturl='/admin/signup')
        return render_template('login.html',purpose='Sign Up',posturl='/admin/signup')


@app.route('/employees/data',methods=['GET'])
def list_employees():
    with app.app_context():
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS list_employees (id INTEGER PRIMARY KEY,name char(100) NOT NULL, location TEXT, efficiency float DEFAULT 0.0,team TEXT NOT NULL)')
        cur.execute('SELECT * FROM list_employees ORDER BY efficiency desc')
        data = cur.fetchall()
        response = {}
        db.close()
        if not data:
            return render_template('list.html',response=["no users"])
        c = 0
        for employee in data:
            temp = {}
            temp['id'] = employee[0]
            temp['name'] = employee[1]
            temp['location'] = employee[2]
            temp['efficiency'] = employee[3]
            temp['team'] = employee[4]
            response.append(temp)
        print(response)
        return render_template('list.html',response=response)

@app.route('/employee/add', methods=['GET','POST'])
def add_employee():
    with app.app_context():
        if not request.json:
            data = {
                'name': '',
                'id' : -1
            }
        else:
            data = {
                'name': request.json['name'],
                'id' : request.json['id'],
                'team' : request.json['team']
            }
        if request.json['location']:
            data['location'] = request.json['location']
        # if request.json['efficiency']:
        #     data['efficiency'] = request.json['efficiency']
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS list_employees (id INTEGER PRIMARY KEY,name char(100) NOT NULL, location TEXT, efficiency float DEFAULT 0.0,team TEXT NOT NULL)')
        cur.execute('SELECT * FROM list_employees')
        edata = cur.fetchall()
        for employee in edata:
            if employee[0] == data['id'] and employee[1] == data['name']:
                return jsonify({'success': False,'user':'already exists'}),400
        if not data['id'] == -1:
            if data['location']:
                cur.execute('INSERT INTO list_employees (id,name,location,team) VALUES ("{}","{}","{}","{}")'.format(data['id'],data['name'],data['location'],data['team']))
            # elif data['efficiency'] and not data['location']:
            #     cur.execute('INSERT INTO list_employees (id,name,efficiency) VALUES ("{}","{}","{}")'.format(data['id'],data['name'],data['efficiency']))
            # elif data['location'] and data['efficiency']:
            #     cur.execute('INSERT INTO list_employees (id,name,location,efficiency) VALUES ("{}","{}","{}",{})'.format(data['id'],data['name'],data['location'],data['efficiency']))
            # else:
            #     cur.execute('INSERT INTO list_employees (id,name) VALUES ("{}","{}")'.format(data['id'],data['name']))
            db.commit()
            db.close()
            return jsonify({'success': True,'user':data["name"],'id':data['id']}),201

        else:
            return jsonify({'success': False}),201


@app.route('/employee/delete', methods=['DELETE'])
def rm_employee():
    with app.app_context():
        if request.json and request.json['name'] and request.json['id']:
            data = {
                'id': request.json['id'],
                'name': request.json['name']
            }
        else:
            data = {
                'id' : -1,
                'name' : ''
            }
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS list_employees (id INTEGER PRIMARY KEY,name char(100) NOT NULL, location TEXT, efficiency float DEFAULT 0.0)')
        cur.execute('SELECT * FROM list_employees')
        edata = cur.fetchall()
        for employee in edata:
            if employee[0] == data['id'] and employee[1] == data['name']:
                #user is found
                cur.execute('DELETE FROM list_employees WHERE id ={}'.format(data['id']))

        if data['id'] == -1:
            return jsonify({'success': False,'error':'user does not exist'}),201
        db.commit()
        db.close()
        return jsonify({'success': True,'user':data["name"],'id':data['id']}),201

# @app.route('/admin/signup',methods=['GET','POST'])
# def admin_signup():
#     with app.app_context():
#         db = sqlite3.connect('./db/database.db')
#         cur = db.cursor()
#         if request.json and request.json['username'] and request.json['password']:
#             response = {
#                 'username' : request.json['username'],
#                 'password' : request.json['password']
#             }
#         else:
#             response = {
#                 'username' : '',
#                 'password' : ''
#             }
#         cur.execute('CREATE TABLE IF NOT EXISTS admin (username char(100) PRIMARY KEY, password char(100) NOT NULL)')
#         cur.execute('SELECT * FROM admin')
#         data = cur.fetchall()
#         for admin in data:
#             if admin[0] == response['username'] and admin[1] == data['password']:
#                 return jsonify({'success': False,'admin':'already exists'}),400

@app.route('/add/data',methods=['POST','GET'])
def add_employee_data():
    with app.app_context():
        if not request.json:
            abort(400)

        response = json.loads(request.get_json())
        
        # response = {
        #     "process" : req['process'],
        #     'timestamp' : req['timestamp'],
        #     'ip' : req['ip'],
        #     'name' : req['name'],
        #     'city' : req['city'],
        #     'country' : req['country'],
        #     'key' : req['key'],
        #     'timespent' : req['timespent'],
        #     'lat' : req['lat'],
        #     'long' : req['long'],
        #     'id' :req['id']
        # }
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS database (
                id INT NOT NULL,
                timestamp TEXT,
                ip TEXT NOT NULL, 
                name char(100) NOT NULL,
                city char(100), 
                country char(10),
                timespent TEXT NOT NULL,
                lat float NOT NULL,
                long float NOT NULL,
                process TEXT NOT NULL,
                process_id INT NOT NULL,
                FOREIGN KEY (id) REFERENCES list_employees (id)
            )''')
        cur.execute(f'''
            INSERT INTO database VALUES (
                "{response["id"]}",
                "{response["timestamp"]}",
                "{response["ip"]}",
                "{response["name"]}",
                "{response["city"]}",
                "{response["country"]}",
                "{response["timespent"]}",
                "{response["lat"]}",
                "{response["long"]}",
                "{response["process"]}",
                "{response["process_id"]}"
            )''')
        db.commit()
        db.close()
        return jsonify({'success': True}),201

@app.route('/profile/<username>/<int:id>',methods=['GET'])
def show_personal_track(username,id):
    with app.app_context():
        db = sqlite3.connect(DATABASE_PATH)
        cur = db.cursor()
        print(id)
        cur.execute('SELECT * FROM database WHERE id ={}'.format(id))
        data = cur.fetchall()
        results = []
        c=0
        for row in data:
            response={}
            response["process"] = row[9]
            response["process_id"] = row[10]
            response["timestamp"] = row[1]
            response["ip"] = row[2]
            response["name"] = row[3]
            response["city"] = row[4]
            response["country"] = row[5]
            response["timespent"] = row[6]
            response["lat"] = row[7]
            response["long"] = row[8]
            response["id"] = row[0]
            results.append(response)
        print(results)
        return render_template('dashboard.html', data=results)


app.run()