import random
from common import logger
import redisop
import requests
import redisop
import json
import config

commonStr = config.get('commonStr')
passwordSize = config.get('passwordSize')
month = config.get('month')
year = config.get('year')
port = str(config.get('slave_port'))


def addUser(test=False, time=1):
    userDict = redisop.getusers()
    (newName, newPassword) = generateNewUser(userDict)
    if test is True:
        days = 3
        redisop.addUser(newName, newPassword, days)
    else:
        days = time * month
        redisop.addUser(newName, newPassword, days)
    logger.debug('add newUser:' + str(newName))
    return (newName, newPassword)


def addNodesUsers(data):
    nodes = redisop.getAllNodes()
    if nodes is None:
        logger.info('ERROR! no nodes in add users')
    for k,v in nodes.item():
        url = 'http://' + v['ip'] + ':' + port + '/addUser'
        requests.post(url, data=data, timeout=60)


def deleteNodesUsers(port):
    nodes = redisop.getAllNodes()
    if nodes is None:
        logger.info('ERROR! no nodes in add users')
    for k,v in nodes.item():
        url = 'http://' + v['ip'] + ':' + port + '/deleteUser'
        data = {

        }
        requests.post()

def generateNewUser(userDict):
    newName = ''
    newPassword = ''

    while(1):
        global port
        newName = port + 1
        port = port + 1

        if (userDict.has_key("0:"+str(port))):
            continue

        i = 1
        while(i <= passwordSize):
            newPassword += random.choice(commonStr)
            i += 1
        break
    return (newName, newPassword)