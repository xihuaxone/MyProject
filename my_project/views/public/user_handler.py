import json
import traceback

import tornado.web
import logging as logger

from controllers.public.user_controller import user_info_base_ctr


class UserHandler(tornado.web.RequestHandler):
    def get(self):
        ret = {'success': True, 'code': 200, 'msg': '', 'data': None}

        user_id = self.get_argument('user_id', None)
        login_name = self.get_argument('login_name', None)
        user_name = self.get_argument('user_name', None)
        email = self.get_argument('email', None)
        phone = self.get_argument('phone', None)

        try:
            resp = user_info_base_ctr.get(user_id, login_name, user_name, email, phone, get_list=False)
        except Exception as err:
            logger.error('get user_info_base error: %s'
                         % traceback.format_exc(10))
            ret['success'] = False
            ret['code'] = 1000
            ret['msg'] = str(err)
            self.write(ret)
            return

        logger.info('query result: %s' % resp)

        if not resp.get('success'):
            ret['success'] = False
            ret['code'] = 1005
            ret['msg'] = 'user not found.'

        else:
            ret['info'] = resp.get('info')

        logger.info('request uri [%s] from host [%s] with method [%s], response: %s'
                    % (self.request.uri, self.request.host, self.request.method, ret))
        self.write(ret)

    def post(self):
        ret = {'success': True, 'code': 200, 'msg': '', 'data': None}

        user_info = json.loads(self.request.body.decode('utf-8'))

        try:
            resp = user_info_base_ctr.add(user_info, 'ignore')
        except Exception as err:
            logger.error('add user info failed. detail: %s'
                         % traceback.format_exc(10))
            ret['success'] = False
            ret['code'] = 1000
            ret['msg'] = err
            self.write(ret)
            return

        if not resp.get('success'):
            ret['success'] = False
            ret['code'] = 1005
            ret['msg'] = 'add user failed. detail: %s' % resp.get('msg')
            self.write(ret)
            return
        else:
            ret['info'] = resp.get('info')

        logger.info('request uri [%s] from host [%s] with method [%s], response: %s'
                    % (self.request.uri, self.request.host, self.request.method, ret))
        self.write(ret)
