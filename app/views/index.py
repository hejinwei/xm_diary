# coding=utf-8

import os
from flask import Blueprint, request, session, render_template, redirect, url_for, json, make_response
from werkzeug.utils import secure_filename
from MongoDBDao import DiaryDao, IDDao
import sys, time
import re
from uploader import Uploader

reload(sys)
sys.setdefaultencoding('utf8')

index = Blueprint('index', __name__, static_folder='../static')

default_page_size = 15

UPLOAD_FOLDER = '/Users/jinweihe/Desktop/tmpFileUpload'


@index.route('/show_diary_list/<user_id>/<int:page_num>')
def show_diary_list(user_id, page_num):
    count = DiaryDao.find_diaries_count(user_id)
    diaries = DiaryDao.find_diaries(user_id, page_num, default_page_size)
    return render_template('index.html', count=count, diaries=diaries, user_id=user_id)


@index.route('/view_diary/<diary_id>')
def view_diary(diary_id):
    diary = DiaryDao.find_diary_by_id(int(diary_id))
    return render_template('view_diary.html', diary=diary)


@index.route('/go_write_diary/<user_id>')
def go_write_diary(user_id):
    return render_template('write_diary.html', user_id=user_id)


@index.route('/save_diary', methods=['post'])
def save_diary():

    ##验证用户
    user_id = request.form['user_id']
    session_user_id = session['user_id']
    if str(user_id) != str(session_user_id):
        return 'error'

    title = request.form['title']
    type = request.form['type']
    weather = request.form['weather']
    content = request.form['content']
    diary_id = IDDao.find_and_modify('diary')
    date = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
    DiaryDao.insert_one_diary(diary_id['id'], int(user_id), title, weather, type, date, content)
    return 'ok'


@index.route('/shouye')
def shouye():
    return redirect(url_for('index.show_diary_list', user_id=session['user_id'], page_num=1))


@index.route('/upload', methods=['GET', 'POST'])
def upload():

    mimetype = 'application/json'
    result = {}

    action = request.args.get('action')
    static_home = '/Users/jinweihe/python-projects/diary/static'
    print(os.path.join(static_home,'third_party', 'ueditor', 'js', 'php', 'config.json'))

    try:
        with open(os.path.join(static_home,'third_party', 'ueditor', 'js', 'php', 'config.json')) as fp:
            try:
                CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
            except:
                CONFIG = {}
    except IOError,e:
        print(e)

    if action == 'config':
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, static_home)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, static_home, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']
        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)
        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, static_home, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })
        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list
    else:
        result['state'] = '请求地址出错'
    result = json.dumps(result)
    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res



