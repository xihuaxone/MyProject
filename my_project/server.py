import logging
import os
import signal

import tornado.ioloop
import tornado.web

from views.urls import url_list


def init_log(level, stream=True, file=True, file_path='./logs/', log_name='tornado_log.log'):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)

    if file:
        if not os.path.isdir(os.path.dirname(file_path)):
            os.mkdir(file_path)
        file_handler = logging.FileHandler(os.path.join(file_path, log_name))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


init_log('INFO')

logger = logging.getLogger()


def make_app():
    return tornado.web.Application(url_list)


def signal_handler(signum, frame):
    logger.warning("got signal %s" % signum)
    if signum == signal.SIGINT:
        logger.warning("got Ctrl+C, will do exit(1)")
        service.stop()
        logger.info('service stopped.')
        exit(1)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    port = 8080

    app = make_app()
    logger.info('app created.')

    logger.info('listen port %s.' % port)
    app.listen(port)

    service = tornado.ioloop.IOLoop.current()

    logger.info('starting tornado with single process.')
    service.start()


