# coding:utf-8

import time
import re
import tornado.ioloop
from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode,json_decode
from tornado.web import RequestHandler,StaticFileHandler,url,Application
from tornado.options import define,options
from tornado.httpserver import HTTPServer
import os
import base64
import tornado.log

define('port',default=8080,type=int,help="监听端口")
define('host',default="0.0.0.0",type=str,help="host")

current_path = os.path.dirname(__file__)
static_path = os.path.join(current_path,'static')
template_path = os.path.join(current_path,'templates')

# 用户组
users = []

settings = {
    'cookie_secret':'snow_rabbit',
    'static_path':static_path,
    'template_path':template_path
}

class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')

class LoginHandler(RequestHandler):
    def post(self, *args, **kwargs):
        pattern = re.compile("^[\u4E00-\u9FA5]{3,7}$")
        username = self.get_body_argument('username')

        if pattern.match(username):
            self.set_secure_cookie('username',username)
            self.redirect('/chat')
        else:
            self.redirect('/')

class ChatHandler(RequestHandler):
    def get(self, *args, **kwargs):
        ret = {}
        ret['username'] = self.get_secure_cookie('username')
        self.render('chat.html',**ret)

class ChatWebSocketHandler(WebSocketHandler):
        def open(self, *args, **kwargs):
            users.append(self)

        def on_message(self, message):
            user_info = self.get_secure_cookie('username').decode('utf-8') + " | " \
                        + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            message = json_decode(message)
            if message.get('type') == "text":
                user_msg = message.get('body')
                for user in users:
                    ret = json_encode({'type':'text','user_info':user_info,'user_msg':user_msg})
                    user.write_message(ret)
            elif message.get('type') == "pic":
                user_msg = message.get('body')
                for user in users:
                    ret = json_encode({'type':'pic','user_info':user_info,'user_msg':user_msg})
                    user.write_message(ret)

        def on_close(self):
            users.remove(self)

if __name__ == '__main__':
    options.parse_config_file('config.conf')

    app = Application([
        url(r'/',IndexHandler),
        url(r'/login',LoginHandler),
        url(r'/chat',ChatHandler),
        url(r'/access',ChatWebSocketHandler)
    ],**settings)
    server = HTTPServer(app)
    #server.bind(options.port,options.host)
    # 多进程模式启动(windows不可用)
    #server.start(2)
    server.listen(options.port)
    tornado.ioloop.IOLoop().current().start()