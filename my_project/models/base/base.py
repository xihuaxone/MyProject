#!/bin/env python
# -*- coding:utf8 -*-
import datetime
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.ext.declarative import declarative_base
from settings.service_settings import MyProjectDb


def serialize(self):
    columns = [c.key for c in class_mapper(self.__class__).columns]
    return dict((c, getattr(self, c))for c in columns)


Base = declarative_base()
Base.serialize = serialize

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



