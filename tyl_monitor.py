#!/opt/pro/python279/bin/python

import log_helper, date_helper 
import os, ConfigParser, time
import mes

global  __log__path
cf = ConfigParser.ConfigParser()
cf.read('/opt/scripts/Streamer_Monitor/config.ini')
__log__path = cf.get('global','tyl_log_path')
channelist = cf.options('TYL_Channel')
m3u8_path = cf.get('global','m3u8_path')

def logger(mes):
    log_helper.get_logger(__log__path).info(mes)

def last_ts_time(m3u8):
    f = open(m3u8)
    mLines = f.readlines();
    targeLine = mLines[-1]
    f.close()
    tsTime = targeLine.strip('\n')[-18:-3]
    return date_helper.format_tup(tsTime)

def main():
    for channel in channelist:
        tsTime = last_ts_time(m3u8_path + channel + '.m3u8')
        delayTime = time.time() - tsTime
        if delayTime > 600:
	    logger('%s breakdown, last ts time %s' %(channel,tsTime))
            cf = ConfigParser.ConfigParser()
            cf.read('/opt/scripts/Streamer_Monitor/config.ini')
            rtmp = cf.get('TYL_Channel',channel)
	    logger('channel: %s rtmp: %s' %(channel,rtmp))
            mes.redis_process(channel,'TYL',rtmp=rtmp)
        else:
	    pass
            
            
if __name__ == '__main__':
    for channel in channelist:
        tsTime = last_ts_time(m3u8_path + channel + '.m3u8')
        delayTime = time.time() - tsTime
        print delayTime
        if delayTime > 600:
            cf = ConfigParser.ConfigParser()
            cf.read('/opt/scripts/Streamer_Monitor/config.ini')
            rtmp = cf.get('TYL_Channel',channel)
            mes.redis_process(channel,'TYL',rtmp=rtmp)
        else:
            print "channel:%s normal" %channel
