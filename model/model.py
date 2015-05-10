class Model(object):
    """\
        dict abstraction for model
    """

    def __init__(self):
        super(Model, self).__init__()
        self.content = {}

    def __getitem__(self, key):
        return self.content[key]

    def __setitem__(self, key, value):
        self.content[key] = value
