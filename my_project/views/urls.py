from views.public.test_handler import TestHandler
from views.public.user_handler import UserHandler

url_list = [
    (r"/", TestHandler),
    (r"/user$", UserHandler),

    ]