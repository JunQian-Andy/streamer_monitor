#!/usr/bin/env python
#encoding=utf-8

import time, ConfigParser, sys, redis
import log_helper, date_helper
from sms_alarm import sms_alarm

#phone = "15721282565,13818111063,18917637631"
phone = "15721282565,18917637631,18222629776,15316005909"

cf = ConfigParser.ConfigParser()
cf.read('/opt/scripts/Streamer_Monitor/config.ini')
__meslog__path = cf.get('global','mes_log_path')
redis_host = cf.get('global','redis_server')


def logger(mes):
	log_helper.get_logger(__meslog__path).info(mes)

def message(mobile,mes):
    mobiles = mobile.split(',')
    for m in mobiles:
    	sms_alarm(m,mes)
    	time.sleep(5)

#Redis##############
def redis_process(channel, tratype, rtmp=None, rtsp=None, channelname=None):
	if tratype == 'TYL':
		r = redis.StrictRedis(host=redis_host, port=6379, db=0)
		if r.get(channel) == None:
			TYL_send_mes(1, channel, rtmp)
			nowtime = date_helper.get_now_datestr3()
			r.set(channel, nowtime)
			r.expire(channel, 3600)
		else:
			pass
	elif tratype == 'TM':
		r = redis.StrictRedis(host=redis_host, port=6379, db=1)
		if r.get(channel) == None:
			TM_send_mes(1, channel, channelname)
			nowtime = date_helper.get_now_datestr3()
			r.set(channel, nowtime)
			r.expire(channel, 3600)
		else:
			pass
	elif tratype == 'NLTP':
		r = redis.StrictRedis(host=redis_host, port=6379, db=2)
		if r.get(channel) == None:
			NLTP_send_mes(1, channel, rtmp)
			nowtime = date_helper.get_now_datestr3()
			r.set(channel, nowtime)
			r.expire(channel, 3600)
		else:
			pass

        elif tratype == 'RTSP':
                r = redis.StrictRedis(host=redis_host, port=6379, db=3)
                if r.get(channel) == None:
                        RTSP_send_mes(1, channel, rtsp)
                        nowtime = date_helper.get_now_datestr3()
                        r.set(channel, nowtime)
                        r.expire(channel, 3600)
                else:
                        pass

#MESS##############
def TYL_send_mes(judgment,channelname,rtmp):
    #print "judgment is %s" %judgment
    #print channelname
    if judgment == 1:
        breakdown_mes = "频道:%s TYL-HLS流异常(%s)" %(channelname,rtmp)
        message(phone,breakdown_mes)
	logger(breakdown_mes)
	#print breakdown_mes

    elif judgment == 0:
        recovery_mes = "频道:%s TYL-HLS流恢复(%s)" %(channelname,rtmp)
        message(phone,recovery_mes)
	logger(recovery_mes)
	#print recovery_mes

def TM_send_mes(judgment,channel,channelname):
    #print "judgment is %s" %judgment
    #print channelname
    if judgment == 1:
        breakdown_mes = "频道:%s(%s) TM源站流异常" %(channel,channelname)
	#print "%s 频道异常" %channel
        message(phone,breakdown_mes)
	logger(breakdown_mes)
	#print breakdown_mes

    elif judgment == 0:
        recovery_mes = "频道:%s(%s) TM源站流恢复[server01]" %(channel, channelname)
        message(phone,recovery_mes)
	logger(recovery_mes)
	#print recovery_mes
	
def NLTP_send_mes(judgment, channelname, rtmp):
    #print "judgment is %s" %judgment
    #print channelname
    if judgment == 1:
        breakdown_mes = "频道:%s NLTP-HLS 失败次数达到101次(%s)" %(channelname,rtmp)
        message(phone,breakdown_mes)
	logger(breakdown_mes)
	#print breakdown_mes

    elif judgment == 0:
        recovery_mes = "频道:%s NLTP-HLS流恢复(%s)" %(channelname,rtmp)
        message(phone,recovery_mes)
	logger(recovery_mes)
	#print recovery_mes

def RTSP_send_mes(judgment, channelname, rtsp):
    #print "judgment is %s" %judgment
    #print channelname
    if judgment == 1:
        breakdown_mes = "频道:%s RTSP直播流异常(%s)" %(channelname,rtsp)
        message(phone,breakdown_mes)
        logger(breakdown_mes)
        #print breakdown_mes

    elif judgment == 0:
        recovery_mes = "频道:%s NLTP-HLS流恢复(%s)" %(channelname,rtmp)
        message(phone,recovery_mes)
        logger(recovery_mes)
        #print recovery_mes


'''
if __name__ == '__main__':
	redis_process(0, 'df-450k',)
	#path =os.path.dirname(amodule.__file__)
	#print sys.path
	print "over"
'''
