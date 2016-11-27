#!/usr/bin/python
# -*- coding: UTF-8 -*-
import jwt,json
from flask import Flask,request
import task
import user
import redisop
from common import logger
import thread
import config

lock = thread.allocate_lock()
app = Flask(__name__)
secret = config.get('secret')


@app.route('/users', methods=['GET'])
def getAllUsers():
    users = redisop.getusers()
    # return jsonify(users)
    return jwt.encode(users, secret)


@app.route('/addUser', methods=['POST'])
def addUser():
    value = request.get_json()
    test = value['test']
    time = value['time']
    (newport,newPassword) = user.addUser(test, time)
    data = {
        'port':newport,
        'password':newPassword
    }
    temp = jwt.encode(data, secret)
    user.addNodesUsers(temp)
    return json.dumps(data)


@app.route('/flow', methods=['POST'])
def resetFlow():
    global lock
    lock.acquire()
    try:
        value = request.get_json()
        logger.info('flow request:' + json.dumps(value))
        mac = value['mac']
        flows = value['flow']
        time = value['time']
        for k,v in flows.item():
            redisop.setFlow(mac, time, k, v)
    finally:
        lock.release()

    return ""


@app.route('/host', methods=['POST'])
def postHost():
    value = request.get_json()
    logger.info('flow request:' + json.dumps(value))
    mac = value['mac']
    time = value['time']
    port = value['port']
    ip = request.remote_addr
    data = {
        'time':time,
        'ip':ip,
        'port':port
    }
    redisop.postHostInfo(mac, data)
    return "ok"

@app.route('/host', methods=['GET'])
def getHost():
    mac = str(request.args.get('mac', ''))
    if mac.__len__() == 0:
        return ''
    else:
        str = redisop.getHostInfo(mac)
        if str is None:
            return ''
        else:
            return json.dumps(str)


if __name__ == '__main__':
    port = int(config.get('port'))
    task.myThread().start()
    app.run(host="0.0.0.0", port=port, debug=False)
