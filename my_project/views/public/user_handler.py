import traceback

import logging as logger

from controllers.public.user_controller import user_info_base_ctr, user_ctr
from views.base.base_handler import HandlerBase


class UserHandler(HandlerBase):
    def get(self):
        user_info_base_ctr.session = self.db_session

        query_info = self.get_param_info(['user_id', 'login_name',
                                          'user_name', 'email', 'phone'],
                                         allow_empty=True)
        try:
            resp = user_info_base_ctr.get(query_info, get_list=False)
        except Exception as err:
            logger.error('get user_info_base error: %s'
                         % traceback.format_exc(10))
            self.write(None, success=False, code=1000, msg=str(err))
            return

        logger.info('query result: %s' % resp)

        if not resp.get('success'):
            self.write(None, success=False, code=1005, msg='user not found.')

        else:
            self.write(resp.get('info'))

        self.flush()

    def post(self):
        user_ctr.session = self.db_session

        user_info = self.get_body_info(['login_name', 'user_name',
                                        'email', 'phone', 'identify_type',
                                        'identify_code',  'identify_psw'],
                                       allow_empty=True)
        if not user_info.get('login_name'):
            self.write(None, False, 2001, 'login_name not set.')
            return

        try:
            resp = user_ctr.update(user_info, action_if_exist='ignore')
        except Exception as err:
            logger.error('update user info failed. detail: %s'
                         % traceback.format_exc(10))
            self.write(None, success=False, code=1000, msg=str(err))
            return

        if not resp.get('success'):
            msg = 'add user failed. detail: %s' % resp.get('msg')
            self.write(None, success=False, code=1005, msg=msg)

            return
        else:
            self.write(resp.get('info'))

        self.flush()

    def put(self):
        user_ctr.session = self.db_session

        user_info = self.get_body_info(
            ['login_name', 'user_name', 'email', 'phone'],
            allow_empty=True)

        if not user_info:
            logger.info('user login info must input at least 1.')
            self.write(None, False, 2001,
                       'login_name/user_name/email/phone '
                       'must set at least 1.')
            return

        user_info.update(self.get_body_info(
            ['identify_type', 'identify_code',
             'identify_psw'],
            allow_empty=False))

        try:
            resp = user_ctr.add(user_info, action_if_exist='ignore')
        except Exception as err:
            logger.error('add user info failed. detail: %s'
                         % traceback.format_exc(10))
            self.write(None, False, 1000, str(err))
            return

        if not resp.get('success'):
            msg = 'add user failed. detail: %s' % resp.get('msg')
            self.write(None, False, 1005, msg)
            return
        else:
            self.write(resp.get('info'))

        self.flush()

    def delete(self):
        user_ctr.session = self.db_session

        user_id = self.get_body_info(
            ['user_id'], allow_empty=False)['user_id']

        try:
            success = user_ctr.delete(user_id)
        except Exception as err:
            logger.error('delete user info failed. detail: %s'
                         % traceback.format_exc(10))
            self.write(None, False, 1000, str(err))
            return
        if not success:
            self.write(None, False, 1005, 'delete user failed.')
            return
        self.write(None)
        self.flush()
