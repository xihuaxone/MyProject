import json
import os
import requests
from settings.global_config import Service

import unittest


class TestUserHandler(unittest.TestCase):
    url = os.path.join(Service.endpoint, 'user')

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
