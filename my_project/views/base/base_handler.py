import json
from abc import ABC

import tornado.web

from models.base.base import Session


class HandlerBase(tornado.web.RequestHandler, ABC):
    def __init__(self, *args, **kwargs):
        self.db_session = Session()
        super(HandlerBase, self).__init__(*args, **kwargs)

    def prepare(self):
        pass

    def on_finish(self):
        self.db_session.close()

    def set_default_headers(self):
        pass

    def write(self, data, success=True, code=200, msg=''):
        chunk = json.dumps({'success': success,
                            'data': data,
                            'msg': msg
                            })
        return super(HandlerBase, self).write(chunk)

    def get_body_info(self, fields: list, allow_empty=False, default=None):
        if allow_empty:
            return {k: self.get_body_argument(k, default) for k in fields}
        else:
            return {k: self.get_body_argument(k) for k in fields}

    def get_param_info(self, fields: list, allow_empty=False, default=None):
        if allow_empty:
            return {k: self.get_argument(k, default) for k in fields}
        else:
            return {k: self.get_argument(k) for k in fields}
