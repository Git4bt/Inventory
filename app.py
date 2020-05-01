# from flask import Flask, request, Response
from flask import Flask, flash, render_template, request, session, Response
import requests
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_table import User, create_table, create_users
from elastic import create_elastic_index, populate_inventory

engine = create_engine('sqlite:///users.db', echo=True)

app = Flask(__name__)


def initialize_app():
    app.config['ENV'] = 'development'
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8000, debug=True)


@app.route('/')
@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('table.html')


@app.route('/login', methods=['POST'])
def do_admin_login():

    uname = str(request.form['username'])
    passwd = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([uname]), User.password.in_([passwd]) )
    if query.first():
        session['logged_in'] = True
        return render_template('table.html', uname=query.first().username)
    elif request.method == 'POST':
        flash('wrong username and password!')
    return home()


@app.route('/update')
def edit_server_count():
    return render_template('table.html', action="edit")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/inventory/<dc>', methods=['GET', 'POST'])
def server_count(dc):
    url = "http://localhost:9200/inventory/_doc/{}".format(dc)
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}

    if request.method == 'GET':
        response = requests.request("GET", url + "/_source", headers=headers)
        return Response(response=response, content_type="application/json", status=response.status_code)
    else:
        payload = {"servers": int(request.get_data())}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.text)
        return Response(response=response.text, status=response.status_code)


if __name__ == '__main__':
    create_elastic_index()
    populate_inventory()
    create_table()
    create_users()
    initialize_app()
