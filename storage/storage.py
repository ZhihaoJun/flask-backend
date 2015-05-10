class Storage(object):
    def __init__(self):
        super(Storage, self).__init__()

    @staticmethod
    def get_storage():
        raise NotImplementedError()

    @staticmethod
    def set_config(**config):
        raise NotImplementedError()

    def insert(self, key, value):
        raise NotImplementedError()

    def find(self, key):
        raise NotImplementedError()

    def update(self, key, value):
        raise NotImplementedError()

    def delete(self, key, value):
        raise NotImplementedError()

    def upsert(self, key, value):
        raise NotImplementedError()
