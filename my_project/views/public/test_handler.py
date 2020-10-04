import logging as logger

from views.base.base_handler import HandlerBase


class TestHandler(HandlerBase):
    def get(self):
        logger.info('request uri [%s] from host [%s] with method [%s]'
                    % (self.request.uri, self.request.host, self.request.method))
        self.write('Hello I\'m alive')
