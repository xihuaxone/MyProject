import traceback

import logging as logger

from controllers.public.user_controller import user_info_base_ctr
from views.base.base_handler import HandlerBase


class UserHandler(HandlerBase):
    def get(self):
        query_info = self.get_param_info(['user_id', 'login_name',
                                          'user_name', 'email', 'phone'],
                                         allow_empty=True)
        try:
            resp = user_info_base_ctr.get(query_info, get_list=False)
        except Exception as err:
            logger.error('get user_info_base error: %s'
                         % traceback.format_exc(10))
            self.write(None, success=False, code=1000, msg=err)
            return

        logger.info('query result: %s' % resp)

        if not resp.get('success'):
            self.write(None, success=False, code=1005, msg='user not found.')

        else:
            self.write(resp.get('info'))

        self.flush()

    def post(self):
        user_info_base = self.get_body_info(['login_name', 'user_name',
                                             'email', 'phone', 'identify_type',
                                             'identify_code',  'identify_psw'],
                                            allow_empty=True)
        try:
            resp = user_info_base_ctr.add(user_info_base, action_if_exist='ignore')
        except Exception as err:
            logger.error('add user info failed. detail: %s'
                         % traceback.format_exc(10))
            self.write(None, success=False, code=1000, msg=err)
            return

        if not resp.get('success'):
            msg = 'add user failed. detail: %s' % resp.get('msg')
            self.write(None, success=False, code=1005, msg=msg)

            return
        else:
            self.write(resp.get('info'))

        self.flush()
