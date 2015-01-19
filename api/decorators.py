import pymongo
import time


def db_open_close(fn):
    def wrapper(*args, **kwargs):
        conn = pymongo.Connection(DbKeys.Host, DbKeys.Port)
        # select default database
        kwargs['db'] = conn[DbKeys.Notes]
        output = fn(*args, **kwargs)
        conn.close()
        return output
    return wrapper


def time_it(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        output = fn(*args, **kwargs)
        end = time.time() - start
        return output
    return wrapper