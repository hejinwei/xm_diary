# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, session
import MongoDBDao.UserDao
app = Flask(__name__)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    # 查询用户名密码
    user = MongoDBDao.UserDao.find_user(username)
    if user is None:
        print('用户不存在')
        return None

    if user.password != password:
        print('密码不正确')
        return None

    # 把username存到session
    session['username'] = username

    # TODO  返回到首页

    return render_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.run()

