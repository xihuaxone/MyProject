from models.base.base import Session
from models.public.user_model import UserInfo


def test_session():
    session = Session()
    res = session.query(UserInfo).filter(UserInfo.identify_type == 1).all()
    print(res)
    if not res:
        user_identify = UserInfo()
        user_identify.identify_type = 1
        user_identify.identify_code = 'test'
        user_identify.identify_psw = 'test_pwd'
        session.add(user_identify)
        session.commit()
        session.close()
        print(user_identify)


if __name__ == '__main__':
    test_session()
