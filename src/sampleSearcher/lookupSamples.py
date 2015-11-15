import os
import sys
import time
import logging

try:
    import requests
except ImportError:
    sys.stderr.write('Requests ist erforderlich: http://docs.python-requests.org oder sudo pip install requests')
    sys.exit() 
    
logging.captureWarnings(True)

PLUGIN_DIR = 'searchmodule'
SAMPLES_DIR = 'samples'
LOGFILE = 'logfile.log'
LOG_VIRUSTOTAL = "VIRUSTOTAL\t%s\t%s"
LOG_DOWNLOAD = "DOWNLOAD\t%s\t%s"
LOG_DOWNLOAD_URL = "URL\t%s\t%s"

TIME_OUT = 240
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

VIRUSTOTAL_URL = 'https://www.virustotal.com/vtapi/v2/file/report'
VIRUSTOTAL_URL_SUBMIT = 'https://www.virustotal.com/vtapi/v2/file/scan'
VIRUSTOTAL_API_KEY = 'a0283a2c3d55728300d064874239b5346fb991317e8449fe43c902879d758088'

# Static variable decorator for function
def staticVTCounterVar(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

# Gibt ein Triple zurueck: [sha256,sha1,md5]
@staticVTCounterVar("counter", 0)
@staticVTCounterVar("startTime", 0)
def processHashVT(malware_hash):
    data = {'resource' : malware_hash, 'apikey' : VIRUSTOTAL_API_KEY}
    md5 = ""
    sha1 = ""
    sha256 = ""
    
    # Set on first request
    if processHashVT.startTime == 0:
        processHashVT.startTime = time.time()

    # Increment every request
    processHashVT.counter += 1

    try:
        response = requests.post(VIRUSTOTAL_URL, data=data)
        virustotal = response.json()
    except Exception as e:
        print "Error: Failed performing request: %s"% e
        return
    
    # Create [sha256, sha1, md5] Hash-List
    if 'response_code' in virustotal and int(virustotal.get('response_code')) > 0:
        sha256 = virustotal.get('sha256')
        sha1 = virustotal.get('sha1')
        md5 = virustotal.get('md5')
        
    # Determine minimum time we need to wait for limit to reset
    waitTime = 59 - int(time.time() - processHashVT.startTime)

    if processHashVT.counter == 4 and waitTime > 0:
        waitTime + 5 # Sicherheitsaufschlag
        print "Warn: Limit requests per minute reached (%d per minute); waiting %d seconds" % (processHashVT.counter, waitTime)
        time.sleep(waitTime)
        waitTime = 60
        # Reset static vars
        processHashVT.counter = 0
        processHashVT.startTime = 0

    return sha256,sha1,md5

def log(msg):
    logfile = os.path.join(os.path.dirname(sys.argv[0]), LOGFILE)
    with open(logfile, 'a') as f:
        f.write("%s\t%s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))

def AddPlugin(pluginClass):
    plugins.append(pluginClass)

def loadPlugins():
    pluginPath = os.path.join(os.path.dirname(sys.argv[0]), PLUGIN_DIR)
    dirList = os.listdir(pluginPath)
    
    for plugin in dirList:
        try:
            if plugin.lower().endswith('.py'):
                exec open(os.path.join(pluginPath, plugin), 'r') in globals(), globals()
                print "Load Plugin: %s" % plugin.replace('.py', '')
        except Exception as e:
            print('Error %s loading plugin: %s' % (e, plugin.replace('.py', '')))
            
def process(sha256, sha1, md5):   
    if not os.path.exists(SAMPLES_DIR):
        os.makedirs(SAMPLES_DIR) 
    
    for pluginClass in plugins:
        pluginObj = pluginClass()
        pluginObj.searchSample(sha256, sha1, md5)
        
        if pluginObj.isDownloadable():
            if pluginObj.downloadSample(SAMPLES_DIR, sha256 + ".bin"):
                log(LOG_DOWNLOAD % (sha256, pluginObj.__class__.__name__))
                print "Download: %s" % sha256
                break
            
if __name__ == "__main__":
    global plugins
    plugins = []
    
    if (len(sys.argv) != 2):
        print "Usage: ",__file__," Hashlist(1 column)"
        sys.exit()
        
    hashlist = sys.argv[1]
    
    if not os.path.isfile(hashlist):
        print "File %s does not exist!" % (hashlist)
        sys.exit()
    
    if not hashlist[-4] == '.':
        print "Filename rejected. Needs file extension like .txt, .csv, or ..."
        sys.exit()
    
    # Hashes einlesen
    f = open(hashlist,'rb')
    hashes = [x.strip() for x in f.readlines()]
    f.close()
    
    # Plugins vom plugin directory laden
    loadPlugins()
        
    for malware_hash in hashes:
        sha256,sha1,md5 = processHashVT(malware_hash)
        if (sha256 and sha1 and md5):
            process(sha256, sha1, md5)
        else:
            # Hash bei VirusTotal nicht gefunden
            log(LOG_VIRUSTOTAL % (malware_hash, "Hash nicht gefunden"))
            # Download mit Hash versuchen 
            process(malware_hash, malware_hash, malware_hash)
    
    print "Fertich"