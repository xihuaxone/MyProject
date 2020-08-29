import os
import requests
from settings.global_config import Service


def test_api():
    """
    test api after server deploy;
    """
    url = os.path.join(Service.endpoint, '')
    print(url)
    res = requests.get(url, timeout=10)
    print(res.content)


if __name__ == '__main__':
    test_api()
