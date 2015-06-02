import re
from rule import Rule, RuleError


class RegexRule(Rule):
    def __init__(self, regex_str, msg='regex error', **kwargs):
        super(RegexRule, self).__init__(
            msg=msg, **kwargs
        )
        self.regex_str = regex_str
        self.__pat = re.compile(regex_str)

    def check(self, key, data):
        if key in data:
            if self.__pat.match(data[key]) is None:
                raise RuleError(
                    key=key,
                    msg=self.msg,
                    **self.extra
                )
