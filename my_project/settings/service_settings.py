from settings import global_config


class MyProjectDb(object):
    _config = global_config.get_section('my_project_db')

    log_level = _config.get('log_level')
    host = _config.get('host')
    port = int(_config.get('port'))
    db_name = _config.get('db_name')
    user = _config.get('user')
    passwd = _config.get('passwd')
    charset = _config.get('charset')

    pool_recycle = 120
    pool_size = 20
    pool_timeout = 30
    max_overflow = 10

    if log_level == 'INFO':
        echo = True
        echo_pool = True
    elif log_level == 'DEBUG':
        echo = 'debug'
        echo_pool = 'debug'
    else:
        echo = False
        echo_pool = False


class MyProjectService(object):
    _config = global_config.get_section('my_project_service')

    endpoint = _config.get('endpoint')
