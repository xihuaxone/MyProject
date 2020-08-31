# -*- coding: utf-8 -*-

from controllers.base.base_controller import ControllerBase, ViewControllerBase
from models.public.user_model import UserInfoBase, UserInfo


class UserInfoBaseController(ControllerBase):
    def __init__(self):
        super(UserInfoBaseController, self).__init__(UserInfoBase)

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
        super(UserInfoController, self).__init__(UserInfo)

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


class UserCollector(ViewControllerBase):
    def __init__(self):
        super(UserCollector, self).__init__([UserInfo, UserInfoBase], [{'user_info.id': 'user_info_base.user_id'}])

    def get(self, user_info_base):
        pass

    def update(self):
        pass

    def add(self):
        pass

    def delete(self):
        pass


user_info_base_ctr = UserInfoBaseController()
user_info_ctr = UserInfoBaseController()
