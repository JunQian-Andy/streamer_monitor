import redis

def redis_conn(redis_host, port=6379, db=0):
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

def redis_set(key, value, redis_host, port=6379, db=0):
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    r.set(key,value)
    return None

def redis_get(key, redis_host, port=6379, db=0):
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    return r.get(key)

def redis_delete(key, redis_host, port=6379, db=0):
    redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    r.delete(key)
    return None

def redis_flush(redis_host, port=6379, db=0):
    redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    r.flushdb()
    return None

def redis_settimeout(key, timeout, redis_host, port=6379, db=0):
    redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    r.expire(key,timeout)
    ### expire 多少时间后超时 r.expire(key, 10) --- 10s后超时
    return None

def redis_settimeout2(key, timeout, redis_host, port=6379, db=0):
    redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
    r.expireat(key, timeout)
    ### expireat 到具体时间点key超时 r.expireat(key, 2015-12-24 12:00:00) --- 到2015年12月24日 12点超时
    return None



