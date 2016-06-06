# coding=utf-8

import os
from flask import Blueprint, request, session, render_template, redirect, url_for, json, make_response
from MongoDBDao import DiaryDao, UserDao
import sys

reload(sys)
sys.setdefaultencoding('utf8')

profile = Blueprint('profile', __name__)

default_page_size = 15


@profile.route('/profile/<owner_id>/<int:page_num>')
def profile_list(owner_id, page_num):

    # 查询所有者
    owner = UserDao.find_user_by_user_id(owner_id)

    # 查询count
    total_count = DiaryDao.find_diaries_count(owner_id)

    # total_pages
    total_pages = 0
    if total_count < default_page_size:
        total_pages = 1
    elif total_count % default_page_size == 0:
        total_pages = total_count / default_page_size
    else:
        total_pages = (total_count / default_page_size) + 1

    # 查询列表
    diaries = DiaryDao.find_diaries(owner_id, page_num, default_page_size)

    return render_template('profile.html', diaries=diaries, owner=owner, total_count=total_count,
                           page_num=page_num, total_pages=total_pages)


@profile.route('/profile/<diary_id>')
def profile_diary_detail(diary_id):
    # 查询详情
    diary = DiaryDao.find_diary_by_id(int(diary_id))

    return render_template('profile_detail.html', diary=diary)
