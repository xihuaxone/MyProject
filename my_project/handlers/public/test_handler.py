import tornado.web


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")