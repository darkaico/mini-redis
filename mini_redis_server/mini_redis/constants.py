from enum import Enum

class RedisCommand(Enum):

    SET = 'SET'
    GET = 'GET'
    DEL = 'DEL'
    DBSIZE = 'DBSIZE'
    INCR = 'INCR'
    ZADD = 'ZADD'
    ZCARD = 'ZCARD'
    ZRANK = 'ZRANK'
    ZRANGE = 'ZRANGE'