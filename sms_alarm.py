#-*- encoding: utf-8 -*-

import os
import sys
import time
import logging
import logging.handlers

import requests
try:
    import curses
except ImportError:
    curses = None

import log_helper



#短信接口配置
_sms_api = 'http://172.16.45.128:80/sendsms'
_sms_params = {
    'svcid' : '11011',
    'svcpass' : '111111',
    'msgtype' : '9',
    'smstype' : '1',
    'priority' : '3',
}
#日志程序路径
_log_path = '/data/log/python/send_alarms.log'


def sms_alarm(mobile, msg):
    global _sms_params
    global _sms_api
    
    params = _sms_params
    params['phone'] = mobile
    params['msg'] = msg

    r = requests.get(url = _sms_api, params = params)
    l = 'sms_req_url:%s;status:%d;result:%s' % (r.url, r.status_code, r.text)
    logger(l)

    if r.status_code != 200:
        return None
    else:        
        return r.text


def logger(msg):
    global _log_path
    log_helper.get_logger(_log_path).info(msg)









if __name__ == '__main__':
    ''' 需传入两个参数，第一个为手机号，多个以半角逗号分隔，第二个为短信消息 '''
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8') 

    if 2 > len(sys.argv):
        logger('sms params error. cmd:'+sys.argv)
    else:
        mobiles = sys.argv[1].split(',')
        msg = sys.argv[2]
        for m in mobiles:
            sms_alarm(m, msg)
            time.sleep(1)
    
