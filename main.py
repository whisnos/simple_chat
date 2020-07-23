# coding:utf-8
import random
import time
import re
import tornado.ioloop
from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode, json_decode
from tornado.web import RequestHandler, StaticFileHandler, url, Application
from tornado.options import define, options
from tornado.httpserver import HTTPServer
import os
import base64
import tornado.log

from basehandler import BaseHandler

define('port', default=9999, type=int, help="监听端口")
define('host', default="0.0.0.0", type=str, help="host")

current_path = os.path.dirname(__file__)
static_path = os.path.join(current_path, 'static')
template_path = os.path.join(current_path, 'templates')

# 用户组
users = []

settings = {
    'cookie_secret': 'snow_rabbit',
    'static_path': static_path,
    'template_path': template_path
}


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class LoginHandler(BaseHandler):
    def post(self, *args, **kwargs):
        pattern = re.compile("^[\u4E00-\u9FA5]{3,7}$")
        username = self.get_body_argument('username')

        if pattern.match(username):
            self.set_secure_cookie('username', username)
            self.redirect('/chat')
        else:
            self.redirect('/')


class ChatHandler(BaseHandler):
    def get(self, *args, **kwargs):
        ret = {}
        name = random.choice(the_list)
        # self.set_secure_cookie('username',name)
        ret['username'] = name
        # print(66,self.get_secure_cookie('username'))
        self.write(ret)


class ChatWebSocketHandler(WebSocketHandler, BaseHandler):
    def open(self, *args, **kwargs):
        users.append(self)

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        message = json_decode(message)
        name = message.get('username')
        user_info = name + " | " \
                    + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if message.get('type') == "text":
            user_msg = message.get('body')
            for user in users:
                ret = json_encode({'type': 'text', 'user_info': user_info, 'user_msg': user_msg})
                user.write_message(ret)
        elif message.get('type') == "pic":
            user_msg = message.get('body')
            for user in users:
                ret = json_encode({'type': 'pic', 'user_info': user_info, 'user_msg': user_msg})
                user.write_message(ret)

    def on_close(self):
        users.remove(self)


the_list = ["周杰伦", "蔡依林", "莫文蔚bai", "冯德伦", "萧亚轩du", "徐若瑄", "周渝民", "吴建豪", "朱孝天", "孙楠", "张柏芝zhi", "谢霆锋", "孙俪", "邓超dao",
            "马伊俐", "文章", "关之琳", "吴佩慈", "佟大为", "关悦", "那英", "王菲", "苏有朋", "李亚鹏", "周迅", "古巨基", "谭咏麟", "巩俐", "章子怡", "范冰冰",
            "李冰冰", "李小璐", "王珞丹", "胡军", "刘德华", "黎明", "郭富城", "张学友", "成龙", "韩庚", "汪东城", "吴尊", "陈乔恩", "宋慧乔", "何润东", "蔡卓妍",
            "刘亦菲", "王力宏", "梁静茹", "王光良", "罗大佑", "周华健", "李宗盛", "齐秦", "萧蔷", "陈小春", "陈晓东", "应采儿", "黄晓明", "方力申", "伍思凯",
            "温兆伦", "言承旭", "陈浩民", "立威廉", "金城武", "李连杰", "孙红雷", "蒲巴甲", "罗中旭", "韩红", "陈红", "徐帆", "蒋雯丽", "屠洪刚", "濮存昕", "许晴",
            "林俊杰", "王心凌", "杜德伟", "林子祥", "谭耀文", "张卫健", "罗嘉良", "费玉清", "张雨生", "徐静蕾", "潘玮柏", "陶喆", "陈奕迅", "范逸臣", "方力申",
            "周慧敏", "曹格", "苏永康", "吴奇隆", "曾志伟", "曾宝仪", "童安格", "安以轩", "杨丞琳", "郑秀文", "梁咏琪", "胡杏儿", "黄宗泽", ]
if __name__ == '__main__':
    options.parse_config_file('config.conf')

    app = Application([
        url(r'/', IndexHandler),
        url(r'/login', LoginHandler),
        url(r'/chat', ChatHandler),
        url(r'/access', ChatWebSocketHandler)
    ], **settings)
    server = HTTPServer(app)
    # server.bind(options.port,options.host)
    # 多进程模式启动(windows不可用)
    # server.start(2)
    server.listen(options.port)
    tornado.ioloop.IOLoop().current().start()
