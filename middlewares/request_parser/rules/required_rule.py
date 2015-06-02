from rule import Rule, RuleError


class RequiredRule(Rule):
    def __init__(self, msg='required error', **kwargs):
        super(RequiredRule, self).__init__(
            msg=msg,
            **kwargs
        )

    def check(self, key, data):
        if key not in data:
            print(self.extra)
            raise RuleError(
                key=key,
                msg=self.msg,
                **self.extra
            )
