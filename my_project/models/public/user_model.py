# coding: utf-8
from sqlalchemy import Column, DateTime, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from models.base.base import Base


class UserInfo(Base):
    __tablename__ = 'user_info'
    __table_args__ = (
        Index('identify_keys', 'identify_type', 'identify_code', 'identify_psw', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True, comment='用户主键id')
    identify_type = Column(INTEGER(3), nullable=False, comment='登录认证方式')
    identify_code = Column(VARCHAR(255), nullable=False, comment='登录认证code')
    identify_psw = Column(VARCHAR(255), nullable=False, comment='登录认证密码')
    time_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    time_modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')



class UserInfoBase(Base):
    __tablename__ = 'user_info_base'
    __table_args__ = (
        Index('user_contact_info', 'user_name', 'phone', 'email'),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False, comment='用户主键id，用于关联其他用户表')
    login_name = Column(String(255), nullable=False, comment='用户登录名')
    user_name = Column(String(100), nullable=False, comment='用户自定义名')
    email = Column(String(255), comment='email地址')
    phone = Column(String(50), comment='手机号')
    time_created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    time_modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
