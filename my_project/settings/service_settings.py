class MyProjectDb(object):
    log_level = False

    host = '106.14.76.56'
    port = 3306
    db_name = 'my_project'
    user = 'root'
    passwd = '13241324'
    charset = 'utf8'

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
    elif not log_level:
        echo = False
        echo_pool = False
    else:
        raise Exception('log level not allowed.')
