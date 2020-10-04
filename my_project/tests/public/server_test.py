import json
import os
import requests

import unittest

from settings.service_settings import MyProjectService


class TestUserHandler(unittest.TestCase):
    url = os.path.join(MyProjectService.endpoint, 'user')

    def test_user_post(self):
        data = {
            'user_id': 11112,
            'user_name': 'xihua2',
            'login_name': 'xihuatwo'
        }
        res = requests.post(self.url, data=data, timeout=10)
        print('post resp: %s' % res.content)

    def test_user_get(self):
        params = {
            'user_id': 11112,
            'user_name': 'xihua2',
            'login_name': 'xihuatwo'
        }
        res = requests.get(self.url, params=params, timeout=10)
        print('get resp: %s' % res.content)


if __name__ == '__main__':
    unittest.main()
