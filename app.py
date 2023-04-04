import asyncio
import hashlib
from flask import Flask, render_template, request,flash
from dbstaff import Database


app = Flask(__name__)


async def get_data_from_db():
    database = await Database.ConnectDB()
    data_from_db = await Database.read_db(database)
    return data_from_db



@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login_page')
def redirect_to_login_page():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():
    data = request.form.to_dict()
    data_from_db = asyncio.run(get_data_from_db())
    message = ""
    for i in data_from_db:
        if data['email'] == i['email'] and hashlib.sha256(data['password'].encode('utf-8')).hexdigest() == i['password']:
            data = [i[j] for j in i.keys() if j != 'id' and j != 'password']
            keys = [j for j in i.keys() if j != 'id' and j != 'password']
            return render_template('success_page.html', data_keys=keys,data=data)
        else:
            message = "Sorry, we were unable to log you in. Please check your email and password and try again."
    return render_template('login.html',message=message,id_for_block="fail_input")


if __name__ == '__main__':
    app.run()
