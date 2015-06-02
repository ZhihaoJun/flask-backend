class ErrorHandler(object):
    """docstring for ErrorHandler"""
    def __init__(self):
        super(ErrorHandler, self).__init__()

    def on_error(self, err):
        raise NotImplementedError()
