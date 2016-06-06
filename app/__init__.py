# coding=utf-8

from flask import Flask
from views import login, mine, profile

DEFAULT_APP_NAME = 'diary'

DEFAULT_MODULES = (
    (login, ''),
    (mine, ''),
    (profile, '')
    # (admin, '/admin'),
)


def setting_modules(app, modules):
    #  注册Blueprint模块
    for module, url_prefix in modules:
        # 通过register_blueprint注册
        app.register_blueprint(module, url_prefix=url_prefix)


def create_app():
    app = Flask(DEFAULT_APP_NAME)
    app.secret_key = 'abcd1234'
    # 使用flask中的Blueprint设置站点模块
    setting_modules(app, DEFAULT_MODULES)
    return app
