from flask import request, g, abort
from functools import wraps
from error_handler import ErrorHandler
from decrypter import Decrypter


class DefaultErrorHandler(ErrorHandler):
    def on_error(self, err):
        abort(404)


class DefaultDecrypter(Decrypter):
    def decrypt(self, data):
        return data


class RequestParser(object):
    def __init__(self, error_handler):
        super(RequestParser, self).__init__()
        self.error_handler = error_handler
        self.default_error_handler = DefaultErrorHandler()
        self.decrypter = DefaultDecrypter()

    def set_decrypter(self, decrypter):
        self.decrypter = decrypter

    def retrieve_data(self, **kwargs):
        data = request.args.to_dict()
        data.update(request.form.to_dict())
        data.update(kwargs)
        return data

    def retrieve_raw_data(self, **kwargs):
        data = request.get_data()
        return data

    def format_data(self, rules, data):
        if rules is None:
            return
        for key, item_rule in rules.iteritems():
            if key not in data and 'default' in item_rule:
                data[key] = item_rule['default']
            if key in data and 'formatter' in item_rule:
                data[key] = item_rule['formatter'].format(data[key])
        return data

    def check_data(self, rules, data):
        if rules is None:
            return
        for key, item_rule in rules.iteritems():
            if 'rules' not in item_rule:
                break
            for rule in item_rule['rules']:
                print(rule, key, data)
                rule.check(key, data)

    def __error_handler_wrapper(self, e):
        # try:
        self.error_handler.on_error(e)
        # except Exception, e:
            # self.default_error_handler.on_error(e)

    def rules(self, rules, no_format=False):
        def deocrate_func(view_func):
            @wraps(view_func)
            def decorated(**kwargs):
                data = self.retrieve_data(**kwargs)
                try:
                    self.check_data(rules, data)
                except Exception, e:
                    self.__error_handler_wrapper(e)
                self.data = {}
                if not no_format:
                    self.data = self.format_data(rules, data)
                else:
                    self.data = data
                return view_func(**kwargs)
            return decorated
        return deocrate_func

    def decrypt(self, decrypter=None):
        def deocrate_func(view_func):
            @wraps(view_func)
            def decorated(**kwargs):
                data = self.retrieve_raw_data(**kwargs)
                try:
                    if decrypter is None:
                        self.data = self.decrypter.decrypt(data)
                    else:
                        self.data = decrypter.decrypt(data)
                except Exception, e:
                    self.__error_handler_wrapper(e)
                return view_func(**kwargs)
            return decorated
        return deocrate_func
