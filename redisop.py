import redis,json
from common import logger

host = "127.0.0.1"
port = "6379"
Redis = redis.Redis(host=host, port=port, db=2, password="lokfhdafjdwialfdn")


def getusers():
      return Redis.hgetall('user')


def deleteUser(port, node=0):
      return Redis.hdel('user', node+":"+port)


def addUser(port, passwd, days, flow, node=0):
      port = str(port)
      node = str(node)
      res = Redis.hexists('user', node+":"+port)
      if res is True:
            return
      temp = {
            "d":days,
            "p":passwd,
            "f":flow
      }
      Redis.hset('user', node+":"+port, json.dumps(temp))


def updateUser(key, value, node='0'):
      Redis.hset('user', key, value)


def getAllNodes():
      return Redis.hgetall('nodes')


def postHostInfo(mac, value):
      res = Redis.hget("nodes", mac)
      Redis.hset('nodes', mac, json.dumps(value))
      return res

def getHostInfo(mac):
      return Redis.hget('nodes', mac)


def getFlows():
      return Redis.hgetall('flow')


def getFlow(port, node='0'):
      port = str(port)
      return Redis.hget('flow', node + ":" + port)


def deleteFlow(port, node='0'):
      return Redis.hdel('flow', node+":"+port)


def setFlow(mac, time, port, value, node='0'):
      port = str(port)
      info = getHostInfo(mac)
      if info is None:
            logger.error('ERROR!no host info!!')
            return
      return Redis.hincrbyfloat('flow', node+":"+port, value)

