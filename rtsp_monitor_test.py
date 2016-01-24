#!/opt/pro/python279/bin/python
#encoding = utf-8

import log_helper, date_helper, datetime
import os, ConfigParser, time, subprocess, json
import mes

global  __log__path
cf = ConfigParser.ConfigParser()
cf.read('/opt/scripts/Streamer_Monitor/config.ini')
__log__path = cf.get('global','rtsp_log_path')
Test_Channel_list = cf.options("Test_Channel")
#print Test_Channel_list

def logger(mes):
    log_helper.get_logger(__log__path).info(mes)

def rtsp_monitor_url(channelurl):
    urloption = "?ip=127.0.0.1&uid=00000000000000000000&cid=9800000000000000000000000000006&cdntoken=api_20160112"
    rtsp_url = cf.get('Test_Channel', channelurl) + urloption
    #print rtsp_url
    return rtsp_url

def probe_stream(rtsp_url):
    start = datetime.datetime.now() 
    cmd = "/usr/local/ffmpeg2/bin/ffprobe -v quiet -print_format json -show_streams -i " + '"' + rtsp_url + '"'
    p = subprocess.Popen(cmd, bufsize=10000, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #print cmd
    while p.poll() is None:
        time.sleep(0.1)
	now = datetime.datetime.now()
        if (now - start).seconds > 20:
            #print (now - start).seconds
            try:
                p.terminate()
	    except Exception,e:
                return None
        #return None
    return p.stdout.read()
    #out = process.communicate()[0]
    #if process.stdin:
    #  process.stdin.close()
    #if process.stdout:
    #  process.stdout.close()
    #if process.stderr:
    #  process.stderr.close()
    #try:
    #  process.kill()
    #except OSError:
    #  pass
    #return out

    #return p.stdout.read()

def stram_info_json_format(stream_info):
    #print stream_info_json
    #stream_info = json.loads(stream_info_json)
    video_codec_type =  stream_info['streams'][0]['codec_type']
    video_codec_name =  stream_info['streams'][0]['codec_name']
    width =  stream_info['streams'][0]["width"]
    height =  stream_info['streams'][0]['height']
    video_profile =  stream_info['streams'][0]['profile']
    video_Resolution = str(height) + "x" + str(height)
    profile_level =  stream_info['streams'][0]['level']
    video_start_time = stream_info['streams'][0]['start_time']

    audio_codec_type = stream_info['streams'][1]['codec_type']
    audio_codec_name = stream_info['streams'][1]['codec_name']
    audio_channels =  stream_info['streams'][1]['channels']
    sample_rate = stream_info['streams'][1]['sample_rate']
    audio_start_time = stream_info['streams'][1]['start_time']
    m = {
        'video_codec_type':video_codec_type,
        'video_codec_name':video_codec_name,
        'video_profile':video_profile,
        'video_Resolution':video_Resolution,
        'profile_level':profile_level,
        'video_start_time':str(video_start_time),
        'audio_codec_type':audio_codec_type,
        'audio_codec_name':audio_codec_name,
        'audio_channels':audio_channels,
        'sample_rate':sample_rate,
        'audio_start_time':str(audio_start_time),
    }
    
    return m



def main():
    for Test_Channel in Test_Channel_list:
        rtsp_url = rtsp_monitor_url(Test_Channel)
        #print rtsp_url
        channel_info_json = probe_stream(rtsp_url)
        #print channel_info_json
        if channel_info_json:
            channel_info = json.loads(channel_info_json)
	    #print channel_info
            if channel_info:
                print "%s normal" %Test_Channel
		#logger(channel_info_json)
                m = stram_info_json_format(channel_info)
	        '''
                print "video_codec_type: %(video_codec_type)s \n" \
                  "video_codec_name: %(video_codec_name)s \n" \
                  "video_profile: %(video_profile)s \n" \
                  "video_Resolution: %(video_Resolution)s \n" \
                  "profile_level: %(profile_level)s \n" \
                  "video_start_time: %(video_start_time)s \n" \
                  "audio_codec_type: %(audio_codec_type)s \n" \
                  "audio_codec_name: %(audio_codec_name)s \n" \
                  "audio_channels: %(audio_channels)s \n" \
                  "sample_rate: %(sample_rate)s \n" \
                  "audio_start_time:%(audio_start_time)s" % m
	       '''
            else:
	        print "%s breakdown" %Test_Channel
	        rtsp = cf.get('Test_Channel', Test_Channel)
	        #mes.redis_process(Test_Channel,'RTSP',rtsp=rtsp)
	        logger("RTSP %s breakdown" %Test_Channel)
		logger("%s json is %s" %(Test_Channel,channel_info_json))
        else:
            print "%s ***breakdown***" %Test_Channel
            rtsp = cf.get('Test_Channel', Test_Channel)
	    #mes.redis_process(Test_Channel,'RTSP',rtsp=rtsp)
            logger("RTSP %s ***breakdown***" %Test_Channel)
	    logger("%s json is %s" %(Test_Channel,channel_info_json))

if __name__ == "__main__":
    main()
