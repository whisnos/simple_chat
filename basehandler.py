import tornado.web
import tornado.options


class BaseHandler(tornado.web.RequestHandler):
    def options(self):
        # no body
        self.set_status(204)
        self.finish()



    def send_cms_msg(self, code, msg='ok', result=None):
        '''设置CMS接口回调内容'''
        responsedict = {}
        responsedict.setdefault('code', code)
        responsedict.setdefault('msg', msg)
        responsedict.setdefault('data', result)
        self.write(responsedict)
        raise tornado.web.Finish()
        # return self.finish()

    def send_message(self, success, code, msg='ok', result=None):
        '''send error message'''
        responsedict = {}
        responsedict.setdefault('success', success)
        responsedict.setdefault('code', code)
        responsedict.setdefault('message', msg)
        responsedict.setdefault('result', result)
        self.write(responsedict)
        # tornado.web.Finish()
        return self.finish()

    def send_msg_count(self, success, code, msg='ok', count=0, result=None):
        '''send error message'''
        responsedict = {}
        responsedict.setdefault('success', success)
        responsedict.setdefault('code', code)
        responsedict.setdefault('message', msg)
        responsedict.setdefault('count', count)
        responsedict.setdefault('result', result)
        self.write(responsedict)
        # tornado.web.Finish()
        return self.finish()

    def send_msg(self, success, code, msg='ok', result=None):
        '''send error message'''
        responsedict = {}
        responsedict.setdefault('success', success)
        responsedict.setdefault('code', code)
        responsedict.setdefault('message', msg)
        responsedict.setdefault('result', result)
        self.write(responsedict)
        # tornado.web.Finish()
        return self.finish()

    def set_default_headers(self):
        ''' 设置header头部解决跨域 '''
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "*")
        # self.set_header("Access-Control-Allow-Headers", "token")




