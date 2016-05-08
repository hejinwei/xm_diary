# coding=utf-8

from flask import Flask
from app import create_app
app = create_app()

if __name__ == '__main__':
    server_ip = '0.0.0.0'
    server_port = 8000
    app.run(host=server_ip, port=server_port, debug=True)
