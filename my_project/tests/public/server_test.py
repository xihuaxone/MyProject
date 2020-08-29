import json
import os
import requests
from settings.global_config import Service


def test_api():
    """
    test api after server deploy;
    """
    url = os.path.join(Service.endpoint, 'user')
    print(url)
    data = {
        'user_id': 11111,
        'user_name': 'xihua',
        'login_name': 'xihuaxone'
    }
    res = requests.get(url, data=json.dumps(data), timeout=10)
    print(res.content)


if __name__ == '__main__':
    test_api()
