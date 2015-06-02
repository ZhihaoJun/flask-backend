from rule import Rule, RuleError


class NotBlankRule(Rule):
    def __init__(self, msg='can not be blank', **kwargs):
        super(NotBlankRule, self).__init__(
            msg=msg,
            **kwargs
        )

    def check(self, key, data):
        if key in data:
            if isinstance(data[key], basestring) and len(data[key].strip()) == 0:
                raise RuleError(
                    msg=self.msg,
                    **self.extra
                )
            if len(data[key]) == 0:
                raise RuleError(
                    msg=self.msg,
                    **self.extra
                )
