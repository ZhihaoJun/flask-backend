from storage import Storage
import memcache


class MemcacheStorage(object):
    """docstring for MemcacheStorage"""
    __MEM = None
    address = ['127.0.0.1:11211']

    def __init__(self, arg):
        super(MemcacheStorage, self).__init__()

    @staticmethod
    def get_storage():
        if MemcacheStorage.__MEM is None:
            MemcacheStorage.__MEM = memcache.Client(MemcacheStorage.address)
        return MemcacheStorage.__MEM

    @staticmethod
    def set_config(**config):
        MemcacheStorage.address = config['address']

    def insert(self, key, value):
        return MemcacheStorage.get_storage().set(key, value)

    def find(self, key):
        return MemcacheStorage.get_storage().get(key)

    def update(self, key, value):
        return MemcacheStorage.get_storage().set(key, value)

    def delete(self, key):
        return MemcacheStorage.get_storage().delete(key)

    def upsert(self, key, value):
        return MemcacheStorage.get_storage().set(key, value)
