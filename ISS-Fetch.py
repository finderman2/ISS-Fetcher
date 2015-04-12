import urllib.request, json
import time, datetime, codecs, threading

#Enter your latitude and longitude below, altitude in meters is optional
lat = '0.0'
lon = '-0.0'
alt = '0'

#enter time to wait between each check
tMin = 0.17
#Do not alter this, converts minutes into seconds for timer
tSec = tMin*60

#save the configured url to a variable
url = 'http://api.open-notify.org/iss-pass.json?lat='+lat+'&lon='+lon+'&alt='+alt+'&n=1'
#setup reader codec to make sure html content is UTF-8, otherwise urllib throws an error
reader = codecs.getreader("utf-8")

def checkPasses ():
    #download JSON data
    rawWebsite = urllib.request.urlopen(url)
    #runs it through read to make sure it is utf8, then converts it to python dict
    jsonData = json.load(reader(rawWebsite))
    #save the result as a list
    data = jsonData['response']
    #set item equal to the first line of data
    item = data[0]
    #get duration of the pass
    duration = item['duration']

    #take the unix timestamp and convert to human readable format
    riseTime = datetime.datetime.fromtimestamp(item['risetime']).strftime('%b %d %H:%M:%S %Y')
    currentTime = datetime.datetime.now().strftime('%b %d %H:%M:%S %Y')
    #convert times to integers to do math operations
    riseTimeInt = datetime.datetime.strptime(riseTime, '%b %d %H:%M:%S %Y')
    currentTimeInt = datetime.datetime.strptime(currentTime, '%b %d %H:%M:%S %Y')

    #Subtract the rise time from the current time
    diff = riseTimeInt-currentTimeInt
    #break it out into hours and seconds
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    #determine if there is a pass coming soon
    if hours > 0:
        print('I will check again later, the next pass in in', hours, 'hours on', riseTime)
    elif minutes >= 10:
        print('There is a pass in', minutes, 'minutes', 'that lasts for', round(duration/60), 'minutes')
        #perform action here, i.e. blink led
    else:
        print('Flash Lights! Pass in', minutes, 'minutes and', seconds, 'seconds for', round(duration/60), 'minutes')
        #flash lights based on how many minutes are left
    
    return

def checker():
    checkPasses()
    #edit tMin at top of file to change timing
    threading.Timer(tSec, checker).start()

#run timer on startup
checker()
