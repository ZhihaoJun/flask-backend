from rule import Rule, RuleError


class MinLenRule(Rule):
    def __init__(self, min_len, msg='required min length', **kwargs):
        super(MinLenRule, self).__init__(
            min_len=min_len,
            msg=msg,
            **kwargs
        )

    def check(self, key, data):
        if key in data:
            if len(data[key]) < self.min_len:
                raise RuleError(
                    key=key,
                    min_len=self.min_len,
                    msg=self.msg,
                    **self.extra
                )
