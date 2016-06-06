# coding=utf-8

from flask import Blueprint, request, session, render_template, redirect, url_for
import MongoDBDao.UserDao
import sys
reload(sys)
sys.setdefaultencoding('utf8')

login = Blueprint('login', __name__)


@login.route('/')
def index():
    return redirect(url_for('login.go_login'))


@login.route('/go_login')
def go_login():
    return render_template('login.html')


@login.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    # 查询用户名密码
    user = MongoDBDao.UserDao.find_user(username)
    if user is None:
        error = 'User Not Exist'
        return render_template('login.html', error=error)

    print(user)
    print(user['password'])
    if user['password'] != password:
        error = '密码不正确'
        return render_template('login.html', error=error)

    # 把user_id存到session
    session['user_id'] = user['user_id']

    # 跳转到首页
    return redirect(url_for('mine.show_diary_list', user_id=user['user_id'], page_num=1))


@login.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login.go_login'))
