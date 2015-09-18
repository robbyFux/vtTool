#!/usr/bin/python
#----------------------------------------------------------------------------------------------------------------------
# Script zum aktualiseren fehlender Hash-Summen.
# Original-Skript Robby Zeitfuchs, modifiziert durch Viviane.
# Datum modifiziert: 
# 17.9.2015
# 
# Erklaerung:
# Dieses Skript nimmt eine lange List von Hashes einer beliebiger Art,
# und erzeugt daraus eine csv-Datei mit den ergaenzten Hashes.
# 
# Die Funktion 'updateHashlist()' kann in ein eigenes Skript importiert werden.
# Beispielweise in einem Skript, welches Nennungen von Hashes aus einem APT-Report liest.
# So sind im Nachhinein alle Hash-Sorten (Sha256, Sha1, Md5) verfuegbar, 
# selbst wenn man vorher nur eine Hash-Sorte zur Verfuegung hatte.
# 
# Beispiel Hashlist (Eingabe-Datei):
# 
# 0fe568b70a6e0044a1e315c11f8158d1
# 840721348bfaea59e0f56ef975e7431e2b14d20e5093ca3be9205b4dd8f2a036
# 1665713a380007a6f6ba3ba221345764fcb4c132d68929f031e068024aa79507
# dcc03041f43ab2cbc2141339a6884199a6842f97 
# 24f2c88fbb68d9c697adc00a306133f0eb84bbbf7bda79300690aa5b8f0dfa89
# 
# Ausgabe:
# Csv-Datei (Separator: ';'):
# Spalten:
# Sha256; Sha1; Md5
# 
#----------------------------------------------------------------------------------------------------------------------
import os,sys
import csv
import time
import base64
import logging
logging.captureWarnings(True)

try:
    import requests
except ImportError:
    sys.stderr.write('Requests ist erforderlich: http://docs.python-requests.org oder sudo pip install requests')
    sys.exit() 

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
        waitTime = 60
        print "Warn: Limit requests per minute reached (%d per minute); waiting %d seconds" % (processHashVT.counter, waitTime)
        time.sleep(waitTime)

        # Reset static vars
        processHashVT.counter = 0
        processHashVT.startTime = 0

    return sha256,sha1,md5
    
    
def updateHashlist(hashes):
    
    f = open(hashlist,'rb')
    hashes = [x.strip() for x in f.readlines()]
    f.close()
        
    out_hashlist = "%s_new.csv" % (hashlist[:-4])
    
    print "Completed Hashlist will be written to ", out_hashlist
    
    f = open(out_hashlist,'wb')
    
    f.write("Sha256; Sha1; Md5\n")
    
    for malware_hash in hashes:
        print malware_hash
        sha256,sha1,md5 = processHashVT(malware_hash)
        if (sha256 and sha1 and md5):
            f.write("%s; %s; %s\n" % (sha256,sha1,md5))
    
    f.close()
    
    return
    
        
if __name__ == '__main__':    
    
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
        
    updateHashlist(hashlist)
    
    print "Fertich!!!"
    
    sys.exit()
                
    
