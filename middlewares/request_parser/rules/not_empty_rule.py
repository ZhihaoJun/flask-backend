from rule import Rule, RuleError


class NotEmptyRule(Rule):
    def __init__(self, msg='cannot be empty', **kwargs):
        super(NotEmptyRule, self).__init__(
            msg=msg,
            **kwargs
        )

    def check(self, key, data):
        if key in data:
            if isinstance(data[key], basestring) and len(data[key]) == 0:
                raise RuleError(
                    key=key,
                    msg=self.msg,
                    **self.extra
                )
            if not data[key]:
                raise RuleError(
                    key=key,
                    msg=self.msg,
                    **self.extra
                )
