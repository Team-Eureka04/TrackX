from flask import Flask,request,jsonify,abort,render_template
from flask_cors import CORS,cross_origin
import sqlite3

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
        db = sqlite3.connect('./db/database.db')
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
        for admins in data:
            if response['username'] == admins[0] and response['password'] == admins[1]:
                # return render_template('login.html')
                return jsonify({'success': True}),201

        # return jsonify({'success': False}),400
        return render_template('login.html',purpose='Sign In',posturl='/admin/signin')


@app.route('/admin/signup',methods=['GET','POST'])
def admin_signup():
    with app.app_context():
        db = sqlite3.connect('./db/database.db')
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
        for admin in data:
            if admin[0] == response['username'] and admin[1] == data['password']:
                return jsonify({'success': False,'admin':'already exists'}),400
        if not response['username'] == '':
            cur.execute('INSERT INTO admin VALUES ("{}","{}")'.format(response['username'], response['password']))
            db.commit()
            db.close()
            return jsonify({'success': True}),201
        else:
            return render_template('login.html',purpose='Sign Up',posturl='/admin/signup')


@app.route('/employees/data',methods=['GET'])
def list_employees():
    with app.app_context():
        db = sqlite3.connect('./db/database.db')
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS list_employees (id INTEGER PRIMARY KEY,name char(100) NOT NULL, location TEXT, efficiency float DEFAULT 0.0)')
        cur.execute('SELECT * FROM list_employees')
        data = cur.fetchall()
        response = {}
        db.close()
        if not data:
            return jsonify({'users':None}),201
        c = 0
        for employee in data:
            temp = {}
            temp['id'] = employee[0]
            temp['name'] = employee[1]
            temp['location'] = employee[2]
            temp['efficiency'] = employee[3]
            response[c] = temp
            c += 1
        return jsonify(response),201

@app.route('/employee/add', methods=['GET','POST'])
def add_employee():
    with app.app_context():
        if not request.json and not request.json['name'] in request.json and not request.json['id'] in request.json:
            data = {
                'name': '',
                'id' : -1
            }
        else:
            data = {
                'name': request.json['name'],
                'id' : request.json['id']
            }
        print(data)
        if request.json['location']:
            data['location'] = request.json['location']
        # if request.json['efficiency']:
        #     data['efficiency'] = request.json['efficiency']
        db = sqlite3.connect('./db/database.db')
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS list_employees (id INTEGER PRIMARY KEY,name char(100) NOT NULL, location TEXT, efficiency float DEFAULT 0.0)')
        cur.execute('SELECT * FROM list_employees')
        edata = cur.fetchall()
        for employee in edata:
            if employee[0] == data['id'] and employee[1] == data['name']:
                return jsonify({'success': False,'user':'already exists'}),400
        if not data['id'] == -1:
            if data['location']:
                cur.execute('INSERT INTO list_employees (id,name,location) VALUES ("{}","{}","{}")'.format(data['id'],data['name'],data['location']))
            # elif data['efficiency'] and not data['location']:
            #     cur.execute('INSERT INTO list_employees (id,name,efficiency) VALUES ("{}","{}","{}")'.format(data['id'],data['name'],data['efficiency']))
            # elif data['location'] and data['efficiency']:
            #     cur.execute('INSERT INTO list_employees (id,name,location,efficiency) VALUES ("{}","{}","{}",{})'.format(data['id'],data['name'],data['location'],data['efficiency']))
            # else:
            #     cur.execute('INSERT INTO list_employees (id,name) VALUES ("{}","{}")'.format(data['id'],data['name']))
            return jsonify({'success': True}),201
        else:
            return jsonify({'success': False}),201

        db.commit()
        db.close()
        return jsonify({'success': True,'user':data[name],'id':data['id']}),201


        


app.run()