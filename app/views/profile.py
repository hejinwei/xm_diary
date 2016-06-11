# coding=utf-8

import os
from flask import Blueprint, request, session, render_template, redirect, url_for, json, make_response
from MongoDBDao import DiaryDao, UserDao
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

    return render_template('profile.html', diaries=diaries, owner=owner, select_type='0')


@profile.route('/profile/choose_by_type/<owner_id>/<diary_type>')
def choose_by_type(owner_id, diary_type):
    # 查询所有者
    owner = UserDao.find_user_by_user_id(owner_id)

    # 查询列表
    diaries = DiaryDao.find_diaries_by_type(owner_id, diary_type, 1, default_page_size)
    return render_template('profile.html', diaries=diaries, owner=owner, select_type=diary_type)