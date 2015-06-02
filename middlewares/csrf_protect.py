from functools import wraps
from flask import request, session, make_response
import base64
import time
import os


class CSRFError(Exception):
    def __init__(self, referrer, csrf_token):
        super(CSRFError, self).__init__()
        self.referrer = referrer
        self.csrf_token = csrf_token


class CSRFProtect(object):
    EXPIRE_TIME = 60*60*24

    def __init__(self, error_handler):
        super(CSRFProtect, self).__init__()
        self.__error_handler = error_handler

    def require_local_referrer(self, view_func):
        @wraps(view_func)
        def decorated(**kwargs):
            if request.referrer is None or request.referrer.strip() == '':
                self.__error_handler.on_error(CSRFError(request.referrer, None))
            return view_func(**kwargs)
        return decorated

    @staticmethod
    def _get_timestamp():
        return int(time.time())

    @staticmethod
    def check_csrf_token(csrf_token):
        if ('csrf_token' not in session or
                session.get('csrf_generate_time', 0) + CSRFProtect.EXPIRE_TIME\
                < CSRFProtect._get_timestamp()):
            return False
        if isinstance(csrf_token, unicode):
            csrf_token = csrf_token.decode('utf-8')
        print('csrf_token', csrf_token)
        print('session csrf', session['csrf_token'])
        if csrf_token != session['csrf_token']:
            return False
        return True

    @staticmethod
    def get_csrf_token():
        return base64.b64encode(os.urandom(32))

    @staticmethod
    def generate_csrf_token():
        if ('csrf_token' not in session or
                session.get('csrf_generate_time', 0) + CSRFProtect.EXPIRE_TIME\
                < CSRFProtect._get_timestamp()):
            session['csrf_token'] = CSRFProtect.get_csrf_token()
            session['csrf_generate_time'] = CSRFProtect._get_timestamp()

    @staticmethod
    def send_csrf_cookie(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            r = make_response(view_func(*args, **kwargs))
            CSRFProtect.generate_csrf_token()
            r.set_cookie(
                'csrf_token',
                session['csrf_token']
            )
            return r
        return decorated

    def protect(self, view_func):
        @wraps(view_func)
        def decorated(**kwargs):
            data = request.args.to_dict()
            data.update(request.form.to_dict())
            if not CSRFProtect.check_csrf_token(data.get('csrf_token', '')):
                self.__error_handler.on_error(
                    CSRFError(
                        request.referrer,
                        session['csrf_token']
                    )
                )
            return view_func(**kwargs)
        return decorated
