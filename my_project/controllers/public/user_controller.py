# -*- coding: utf-8 -*-
import logging as logger
from controllers.base.base_controller import ControllerBase
from models.base.base import Session
from models.public.user_model import UserInfoBase, UserInfo


class UserInfoBaseController(ControllerBase):
    def __init__(self):
        super(UserInfoBaseController, self).__init__(UserInfoBase, Session())

    def get(self, user_info_base, get_list=False):
        query_method = 'all' if get_list else 'one_or_none'
        filter_dict = {k: v.strip() for k, v in user_info_base.items() if v}
        info = self._get(filter_dict, query_method=query_method)
        return self.format_return(True, '', info)

    def add(self, user_info_base, action_if_exist='update'):
        if not isinstance(user_info_base, dict):
            raise Exception('param user_info is not dict.')
        if not user_info_base.get('login_name'):
            raise Exception('login_name must present.')

        query_dict = {'login_name': user_info_base['login_name']}

        if self._get(query_dict, query_method='one_or_none'):
            if action_if_exist == 'update':
                info = self._update(query_dict, user_info_base)
                return self.format_return(True, 'user exists',
                                          info, user_exists=True)

            elif action_if_exist == 'ignore':
                return self.format_return(False, 'user exists',
                                          None, user_exists=True)

            else:
                raise Exception('user already exists.')

        else:
            info = self._add(user_info_base)
            return self.format_return(True, '', info, user_exists=False)


class UserInfoController(ControllerBase):
    def __init__(self):
        super(UserInfoController, self).__init__(UserInfo, Session())

    def get(self, user_id=None):
        info = self._get({'user_id': user_id}, query_method='one_or_none')
        return self.format_return(True, '', info)

    def add(self, user_info):
        if not isinstance(user_info, dict):
            raise Exception('param user_info is not dict.')
        if not user_info.get('user_id'):
            raise Exception('user_id must present.')

        query_dict = {'user_id': user_info['user_id']}

        if self._get(query_dict, query_method='one_or_none'):
            raise Exception('user info exists.')
        else:
            info = self._add(user_info)
            return self.format_return(True, '', info)


class UserCollector(ControllerBase):
    def __init__(self):
        super(UserCollector, self).__init__([UserInfoBase, UserInfo], Session())

    def get(self, user_info_base):
        info = self._get(user_info_base, 'user_info')
        return self.format_return(True, '', info)

    def update_user_info(self, user_id, update_info):
        info_base_columns = self.get_table_keys('user_info_base')
        info_identify_columns = self.get_table_keys('user_info')
        user_base_info = {k: update_info.pop(k) for k in info_base_columns
                          if k in update_info}
        identify_info = {k: update_info.pop(k) for k in info_identify_columns
                         if k in update_info}

        if update_info:
            logger.warning('some update info not used: %s' % update_info)

        if not self._get({'user_id': user_id}, 'user_info_base'):
            return self.format_return(
                False, 'user id [%s] not exists' % user_id)
        info = {}
        try:
            info['user_info_base'] = self._update({'user_id': user_id},
                                                  user_base_info, 'user_info_base')

            info['user_info'] = self._update({'id': user_id},
                                             identify_info, 'user_info')
            self.commit()
        except Exception as err:
            return self.format_return(False, str(err))
        return self.format_return(True, '', info)

    def add(self):
        pass

    def delete(self):
        pass


user_info_base_ctr = UserInfoBaseController()
user_info_ctr = UserInfoBaseController()
user_ctr = UserCollector()
