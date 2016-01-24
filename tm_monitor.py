#!/opt/pro/python279/bin/python
#encoding=utf-8

import mysql_helper_tm, log_helper, mes
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('/opt/scripts/Streamer_Monitor/config.ini')
__tmlog__path = cf.get('global','tm_log_path')

def logger(mes):
	log_helper.get_logger(__tmlog__path).info(mes)

def mysql_breakdown_channel():
    sql = 'select processId,code,lastCollectTime from r_task where status = %s and isdelete = %s and lastCollectTime < date_sub(now(),INTERVAL 3 MINUTE);'
    #sql = 'select processId,code,lastCollectTime from r_task where status = %s and isdelete = %s and lastCollectTime < date_sub(now(),INTERVAL 20 SECOND);'
    params = ('1', '2')
    process = mysql_helper_tm.find_all(sql, params)
    #print process
    return process
    
#if __name__ == '__main__':
def main():
    channelist = mysql_breakdown_channel()
    if len(channelist) != 0:
        for i in channelist:
            channel = i[1].encode('utf-8')
            cf = ConfigParser.ConfigParser()
            cf.read('/opt/scripts/Streamer_Monitor/config.ini')
            channelname = cf.get('TM_Channel',channel)
	    logger("channel %s breakdown" %channelname)
            #mes.redis_process(channel, 'TM', channelname=channelname)
    else:
	    pass


if __name__ == '__main__':
    channelist = mysql_breakdown_channel()
    if len(channelist) != 0:
        for i in channelist:
            channel = i[1].encode('utf-8')
            #print channel
            cf = ConfigParser.ConfigParser()
            cf.read('/opt/scripts/Streamer_Monitor/config.ini')
            channelname = cf.get('TM_Channel',channel)
            print "%s is %s" %(channel, channelname)
            #mes.redis_process(channel, 'TM', channelname=channelname)
    else:
        print "channel normal"
