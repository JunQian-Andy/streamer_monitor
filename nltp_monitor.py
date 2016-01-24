#!/opt/pro/python279/bin/python
#encoding=utf-8

import mysql_helper_nltp, log_helper, mes
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('/opt/scripts/Streamer_Monitor/config.ini')
__nltplog__path = cf.get('global','nltp_log_path')

def logger(mes):
	log_helper.get_logger(__nltplog__path).info(mes)

def mysql_breakdown_channel():
    #sql = 'select code from sl_original_live where id in (select olid from slt_live_transcode_task_group where taskFailCount = %s);'
    sql = 'select id,code from sl_original_live where id in (select olid from slt_live_transcode_task_group where taskFailCount = %s);'
    #params = ('tm-shsport-512k', '1', '2')
    params = ('101',)
    #process = mysql_helper_nltp.find_all(sql, params, ['code'])
    process = mysql_helper_nltp.find_all(sql, params)
    return process


def mysql_reset_channel(channelid):
    sql = 'UPDATE `stream_live`.`slt_live_transcode_task_group` SET `taskFailCount`=0 WHERE `olid`=%s; '
    params = (channelid,)
    process = mysql_helper.insert_or_update_or_delete(sql, params)
    return process
    

def main():
    channelist = mysql_breakdown_channel()
    if len(channelist) != 0:
        for i in channelist:
            channelid = i[0].encode('utf-8')
            channel = i[1].encode('utf-8')
            print channel
            print channelid
            cf = ConfigParser.ConfigParser()
            cf.read('/opt/scripts/Streamer_Monitor/config.ini')
            rtmp = cf.get('NLTP_Channel',channel)
            print "%s is %s" %(channel, rtmp)
            mes.redis_process(channel, 'NLTP', rtmp=rtmp)
            mysql_reset_channel(channelid)
    else:
        print "channel normal"
		
if __name__ == '__main__':
    channelist = mysql_breakdown_channel()
    if len(channelist) != 0:
        for i in channelist:
            channelid = i[0].encode('utf-8')
            channel = i[1].encode('utf-8')
            print channel
	    print channelid
            cf = ConfigParser.ConfigParser()
            cf.read('/opt/scripts/Streamer_Monitor/config.ini')
            rtmp = cf.get('NLTP_Channel',channel)
            print "%s is %s" %(channel, rtmp)
            mes.redis_process(channel, 'NLTP', rtmp=rtmp)
            mysql_reset_channel(channelid)
    else:
        print "channel normal"
