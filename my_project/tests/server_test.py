import requests


def test_api():
    """
    test api after server deploy;
    """
    url = 'http://127.0.0.1:8080/'
    res = requests.get(url)
    print(res.content)


if __name__ == '__main__':
    test_api()
