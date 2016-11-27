import threading
import time
import datetime
from common import logger
import redisop
import json
import requests

import config

secret = config.get("secret")

headers = {'content-type': 'application/json'}

task_time = config.get("task_time")

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.oldTime = datetime.datetime.now()

    def run(self):
        self.taskLoad()

    def taskLoad(self):
        self.timer_start()
        while True:
            time.sleep(10)

    def timer_start(self):
        t = threading.Timer(int(task_time), self.test_func)
        t.start()

    def test_func(self):
        newTime = datetime.datetime.now()
        logger.info("time is :%s" ,newTime)
        day = int((newTime - self.oldTime).days)
        if day != 0:
            self.lowDays()
        self.checkFlow()
        logger.info("day is :%s", day)
        self.oldTime = newTime
        self.timer_start()


    def checkFlow(self):
        logger.info('task check low flows begin!!!!')
        users = redisop.getusers()
        deleteUsers = []
        for k,v in users.items():
            value = json.loads(v)
            if value.get("f") is None:
                logger.info("no flow, port:" + str(k))
            else:
                flow = value.get("f")
                useFlow = redisop.getFlow(str(k).split(":")[1])
                if useFlow is None:
                    continue
                if int(useFlow) >= int(flow):
                    logger.info("flow used!delete port:" + str(k) + ', use flow:' + str(useFlow) + ', ori flow:' + str(flow))
                    deleteUsers.append(str(k).split(":")[1])
        if len(deleteUsers) != 0:
            self.deleteUsers(deleteUsers)

    def lowDays(self):
        logger.info('task check low days begin!!!!')
        users = redisop.getusers()
        delUsers = []
        for k,v in users.items():
            value = json.loads(v)
            days = int(value['d'])
            if days > 1:
                days = days-1
                value['d'] = days
                redisop.updateUser(k, json.dumps(value))
            else:
                temp = str(k).split(":")
                tempPort = int(temp[1])
                delUsers.append(tempPort)

        if delUsers.__len__() != 0:
            self.deleteUsers(delUsers)

    def deleteUsers(self, delUsers):
        logger.info('delete users:' + json.dumps(delUsers))
        nodes = redisop.getAllNodes()

        for k, v in nodes.items():
            value = json.loads(v)
            url = 'http://' + str(value['ip']) + '/:' + str(value['port']) + '/deleteUser'
            data = delUsers,
            requests.post(url=url, data=json.dumps(data), timeout=3)

