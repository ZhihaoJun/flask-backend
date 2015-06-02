class RuleError(Exception):
    def __init__(self, **kwargs):
        super(RuleError, self).__init__()
        for k, v in kwargs.iteritems():
            self.__setattr__(k, v)


class Rule(object):
    def __init__(self, **kwargs):
        super(Rule, self).__init__()
        if kwargs is None:
            self.extra = {}
        else:
            self.extra = kwargs

    def check(self, key, data):
        raise NotImplementedError
