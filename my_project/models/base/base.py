#!/bin/env python
# -*- coding:utf8 -*-
import datetime
import logging as logger
import traceback
import MySQLdb
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from settings.service_settings import MyProjectDb


drop_keys = ['_sa_instance_state']


def dict_format(self):
    info = self.__dict__
    [info.pop(k) for k in drop_keys if k in info]
    for k, v in info.items():
        if isinstance(v, datetime.datetime):
            info.update({k: v.strftime('%Y-%m-%d %H:%M:%S')})

    return info


Base = declarative_base()
Base.dict_format = dict_format

connect = "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" \
              % (MyProjectDb.user, MyProjectDb.passwd,
                 MyProjectDb.host, MyProjectDb.port,
                 MyProjectDb.db_name, MyProjectDb.charset)

# when creating engine, if db driver import error occurred,
# you need to specify module class manually. For example: module=MySQLdb;
engine = create_engine(connect, module=MySQLdb, encoding='utf-8',
                       pool_recycle=MyProjectDb.pool_recycle,
                       pool_size=MyProjectDb.pool_size,
                       pool_timeout=MyProjectDb.pool_timeout,
                       max_overflow=MyProjectDb.max_overflow,
                       echo=MyProjectDb.echo, echo_pool=MyProjectDb.echo_pool)

Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def singleton_session():
    global Session
    s = scoped_session(Session)()
    yield s
    try:
        s.commit()
    except:
        logger.error('session commit failed. detail: %s'
                     % traceback.format_exc(10))
    finally:
        s.close()
