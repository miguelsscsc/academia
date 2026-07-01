from app import AppHandler, init_db


class handler(AppHandler):
    def __init__(self, *args, **kwargs):
        init_db()
        super().__init__(*args, **kwargs)
