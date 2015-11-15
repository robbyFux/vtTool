__description__ = 'Download Sample from HybridAnalysis Sandbox https://www.hybrid-analysis.com'
__author__ = 'Robby Zeitfuchs'
__version__ = '0.0.1'
__date__ = '2015/11/13'

#TODO: urllib2 auf requests umschreiben

import re
import io
import os
import gzip
import urllib2

#beautifulsoup 4-4.3.2
from bs4 import BeautifulSoup as bs

class HybridAnalysis():

    STR_URL_BASE = 'https://www.hybrid-analysis.com'
    STR_URL_SEARCH = '%s/search?query=%s'
    REGEX_DOWNLOAD_URL = re.compile('/sample/[-A-Za-z0-9%]*/[-A-Za-z0-9%]*.bin.gz')

    def __init__(self):
        self.downloadURLs = []
        
    def searchSample(self, sha256, sha1, md5):
        url = self.STR_URL_SEARCH % (self.STR_URL_BASE, sha256)
    
        request = urllib2.Request(url)
        request.add_header('User-Agent', USER_AGENT)
        soup = bs(urllib2.urlopen(request, timeout=TIME_OUT))
    
        if soup.find(text='No results'):
            #Nichts gefunden
            return False
        
        if soup.find(text='Search results'):
            #Multiple Downloads
            for row in soup("tr"):
                for a in row("a"):
                    dlUrl = self.getDownloadURLMultiplePages(a['href'])
                    if dlUrl: self.downloadURLs.append(dlUrl) 
        else:
            #Direkter Download
            url = self.REGEX_DOWNLOAD_URL.search(str(soup))
            if url:
                url = self.STR_URL_BASE + url.group()
                self.downloadURLs.append(url) 
        
        if self.downloadURLs:
            return True
        return False      
        
    def isDownloadable(self):
        if self.downloadURLs:
            return True
        return False
        
    def downloadSample(self, path, filename):
        if not self.downloadURLs:
            raise Exception("Keine Download-URL vorhanden!") 
        
        #einzelne URLs testen und versuchen das Sample zu laden
        for downloadURL in self.downloadURLs:
            if self.downloadFile(downloadURL, path, filename):
                return True
    
    def getDownloadURLs(self):
        if self.downloadURLs:
            return self.downloadURLs
        else:
            raise Exception("Keine Download-URL vorhanden!") 
    
    def getDownloadURLMultiplePages(self, siteURL):
        request = urllib2.Request(self.STR_URL_BASE + siteURL)
        request.add_header('User-Agent', USER_AGENT)
        page = urllib2.urlopen(request, timeout=TIME_OUT).read()
        
        url = self.REGEX_DOWNLOAD_URL.search(page)
        
        if url:
            url = self.STR_URL_BASE + url.group()
    
        return url
        
    def downloadFile(self, fileURL, downloadFolder, filename):
        filename = os.path.join(downloadFolder, filename)
        
        try:
            page = urllib2.urlopen(fileURL)
            if page.getcode() == 200:
                gz = gzip.GzipFile(fileobj=io.BytesIO(page.read()))
                
                with open(filename, 'wb') as f:
                    f.write(gz.read())
                    f.close() 
                    gz.close
            
            return True   
        except Exception as e:
            print "Error:", e
            return False
        
AddPlugin(HybridAnalysis)