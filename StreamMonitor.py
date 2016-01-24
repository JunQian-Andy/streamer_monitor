#!/opt/pro/python279/bin/python-monitor
#encoding=utf-8

import multiprocessing, ConfigParser, time
import tyl_monitor, tm_monitor, nltp_monitor, rtsp_monitor
import log_helper

cf = ConfigParser.ConfigParser()
cf.read('/opt/scripts/Streamer_Monitor/config.ini')
__processlog__path = cf.get('global','process_log_path')

def logger(mes):
	log_helper.get_logger(__processlog__path).info(mes)

def monitor_work():
    tyl_monitor = multiprocessing.Process(target = tyl_monitor_work)
    tm_monitor = multiprocessing.Process(target = tm_monitor_work)
    nltp_monitor = multiprocessing.Process(target = nltp_monitor_work)
    rtsp_monitor = multiprocessing.Process(target = rtsp_monitor_work)

    tyl_monitor.start()
    tm_monitor.start()
    nltp_monitor.start()
    rtsp_monitor.start()

def tyl_monitor_work():
    logger("tyl_monitor process start")
    tyl_monitor.main()
    
def tm_monitor_work():
    logger("tm_monitor process start")
    tm_monitor.main()
    
def nltp_monitor_work():
    logger("nltp_monitor process start")
    nltp_monitor.main()

def rtsp_monitor_work():
    logger("rtsp_monitor process start")
    rtsp_monitor.main()
    
if __name__ == '__main__':
    monitortime = cf.get('global','monitor_time')

    while True:
        monitor_work()
        time.sleep(int(monitortime))
