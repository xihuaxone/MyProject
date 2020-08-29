import tornado.web
import logging as logger


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        logger.info('request uri [%s] from host [%s] with method [%s]'
                    % (self.request.uri, self.request.host, self.request.method))
        self.write('Hello I\'m alive')
