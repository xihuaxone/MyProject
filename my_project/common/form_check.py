import re


class FormCheck(object):
    phone_rp = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    email_rp = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")

    def __init__(self):
        pass

    @classmethod
    def phone_form_check(cls, phone):
        if len(phone) != 11:
            return False
        if not cls.phone_rp.match(phone):
            return False
        else:
            return True

    @classmethod
    def email_form_check(cls, email):
        if not cls.email_rp.match(email):
            return False
        else:
            return True


if __name__ == '__main__':
    print(FormCheck.phone_form_check('15023456780'))
    print(FormCheck.email_form_check('xihuaxone@outlook.com'))
