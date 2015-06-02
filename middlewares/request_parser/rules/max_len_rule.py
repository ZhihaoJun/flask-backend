from rule import Rule, RuleError


class MaxLenRule(Rule):
    def __init__(self, max_len, msg='exceeded max length', **kwargs):
        super(MaxLenRule, self).__init__(
            max_len=max_len,
            msg=msg,
            **kwargs
        )

    def check(self, key, data):
        if key in data:
            if len(data[key]) > self.max_len:
                raise RuleError(
                    key=key,
                    max_len=self.max_len,
                    msg=self.msg,
                    **self.extra
                )
