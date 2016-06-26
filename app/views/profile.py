# coding=utf-8

import os
from flask import Blueprint, request, session, render_template, redirect, url_for, json, make_response, jsonify
from MongoDBDao import DiaryDao, UserDao, PersonalSignDao, DiaryStatisticDao
import sys

reload(sys)
sys.setdefaultencoding('utf8')

profile = Blueprint('profile', __name__)

default_page_size = 1000


@profile.route('/profile/list/<owner_id>')
def profile_list(owner_id):

    # 查询所有者
    owner = UserDao.find_user_by_user_id(owner_id)

    # 查询count
    # total_count = DiaryDao.find_diaries_count(owner_id)
    #
    # # total_pages
    # total_pages = 0
    # if total_count < default_page_size:
    #     total_pages = 1
    # elif total_count % default_page_size == 0:
    #     total_pages = total_count / default_page_size
    # else:
    #     total_pages = (total_count / default_page_size) + 1

    # 查询列表
    diaries = DiaryDao.find_diaries(owner_id, 1, default_page_size)

    return render_template('profile.html', user_id=owner_id, diaries=diaries, owner=owner, select_type='0')


@profile.route('/profile/choose_by_type/<owner_id>/<diary_type>')
def choose_by_type(owner_id, diary_type):
    # 查询所有者
    owner = UserDao.find_user_by_user_id(owner_id)

    # 查询列表
    diaries = DiaryDao.find_diaries_by_type(owner_id, diary_type, 1, default_page_size)
    return render_template('profile.html', user_id=owner_id, diaries=diaries, owner=owner, select_type=diary_type)


@profile.route('/profile/personal_sign/<owner_id>')
def get_personal_sign_content(owner_id):
    personal_sign_record = PersonalSignDao.find_personal_sign_by_user_id(owner_id)
    if personal_sign_record is None:
        return ''

    return personal_sign_record['sign_content']


@profile.route('/profile/hot_diaries/<owner_id>')
def get_hot_diaries(owner_id):

    try:
        hot_statistics = DiaryStatisticDao.find_hot_top(owner_id, 5)
    except Exception as err:
        print(err)

    data = []
    for hot_statistic in hot_statistics:
        tmp = {}
        #tmp['user_id'] = hot_statistic['user_id']
        tmp['diary_id'] = hot_statistic['diary_id']
        #tmp['view_number'] = hot_statistic['view_number']
        diary = DiaryDao.find_diary_by_id(int(hot_statistic['diary_id']))
        tmp['title'] = diary['title']
        data.append(tmp)

    json_str = json.dumps(data)
    print(json_str)
    return json_str
