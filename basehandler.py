import tornado.web
import tornado.options

class BaseHandler(tornado.web.RequestHandler):
    def options(self):
        # no body
        self.set_status(204)
        self.finish()


    def set_default_headers(self):
        ''' 设置header头部解决跨域 '''
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "*")
        # self.set_header("Access-Control-Allow-Headers", "token")








