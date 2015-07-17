from flask import request


class RequestParser(object):
    def __init__(self):
        super(RequestParser, self).__init__()

    def check_data(self, rules, data):
        """\
        check data using rules
        """
        for key, rule in rules.iteritems():
            if 'rules' in rule:
                for r in rule['rules']:
                    r.check(key, data)

    def format_data(self, rules, data):
        """\
        format data using defined formatter
        """
        print(rules)
        for key, rule in rules.iteritems():
            if key not in data and 'default' in rule:
                data[key] = rule['default']
            if 'formatter' in rule:
                data[key] = rule['formatter'].format(data[key])
        return data

    def parse(self, rules):
        """\
        function to parse data into self.data
        """
        def decorator(view_func):
            def decorated(**kwargs):
                self.data = request.args.to_dict()
                self.data.update(request.form.to_dict())
                self.data.update(**kwargs)
                self.check_data(rules, self.data)
                self.data = self.format_data(self.data)
                return view_func(**kwargs)
            return decorated
