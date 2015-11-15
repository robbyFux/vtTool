__description__ = 'Download Sample from Malwr Sandbox https://malwr.com/'
__author__ = 'Robby Zeitfuchs'
__version__ = '0.0.1'
__date__ = '2015/11/13'

import os
import re
import requests
import random
import string

from requests.adapters import HTTPAdapter
from BeautifulSoup import BeautifulSoup as bs

class Malwr():
    
    USERNAME = ''
    PASSWORD = ''
    
    BOUNDARY_CHARS = string.digits + string.ascii_letters
    STR_URL_BASE = 'https://malwr.com'
    STR_URL_LOGIN = '%s/account/login/' % STR_URL_BASE
    STR_URL_SEARCH = '%s/analysis/search/' % STR_URL_BASE
    STR_ANALYSIS_SEARCH = '/analysis/search/'
    REGEX_ANALYSIS_URL = re.compile('/analysis/[-A-Za-z0-9]*[-A-Za-z0-9/]')
    REGEX_DOWNLOAD_URL = re.compile('/analysis/file/[-A-Za-z0-9]*[-A-Za-z0-9/]sample/[-A-Za-z0-9]*[-A-Za-z0-9/]')

    def __init__(self):
        self.downloadURLs = []
        self.token = ''
        self.header = {} 
        self.cookie = {}
        if not self.USERNAME or self.USERNAME == '': raise Exception("Username not set!") 
        if not self.PASSWORD or self.PASSWORD == '': raise Exception("Passwort not set!") 
        # Einloggen
        self.session = self.loginAndGetSession()
    
    def searchSample(self, sha256, sha1, md5): 
        data, headers = self.encode_multipart({'search': sha256, 'csrfmiddlewaretoken': self.token})       
        
        headers['Referer'] = self.STR_URL_LOGIN  
        headers['User-Agent'] = USER_AGENT           
               
        response = self.session.post(self.STR_URL_SEARCH, data=data, headers=headers)
        response.raise_for_status()
        
        soup = bs(response.text)
        
        for siteURL in self.getAnalyseURLs(soup):
            url = self.getDownloadURLFromPage(siteURL)
            if url:
                self.downloadURLs.append(self.STR_URL_BASE + url) 

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
    
    def getAnalyseURLs(self, soup):
        for analyse in self.REGEX_ANALYSIS_URL.findall(str(soup.findAll('a'))):
            if analyse != self.STR_ANALYSIS_SEARCH:
                yield analyse
    
    def getDownloadURLs(self):
        if self.downloadURLs:
            return self.downloadURLs
        else:
            raise Exception("Keine Download-URL vorhanden!") 
        
    def getDownloadURLFromPage(self, siteURL):
        url = None
        self.header['Referer'] = self.STR_URL_SEARCH
        webSite = self.session.get(self.STR_URL_BASE + siteURL, headers=self.header, timeout=TIME_OUT).text
        matchDownloadURL = self.REGEX_DOWNLOAD_URL.search(webSite)
        
        if matchDownloadURL:
            url = matchDownloadURL.group()
        
        return url
        
    def loginAndGetSession(self):        
        # need to capture a valid csrf token                                           
        # first visit the login page to generate one  
        self.header['Referer'] = self.STR_URL_BASE  
        self.header['User-Agent'] = USER_AGENT                            
        session = requests.session()                                                         
        session.mount(self.STR_URL_BASE, HTTPAdapter(max_retries=5))
        response = session.get(self.STR_URL_LOGIN, timeout=TIME_OUT, headers=self.header)                              
        response.raise_for_status()
                 
        self.token = session.cookies['csrftoken']                                                           
        self.cookie = {'csrftoken':self.token}
                                                                                       
        # now post to that login page with some valid credentials and the token
        auth = {"username": self.USERNAME,
                "password": self.PASSWORD,
                "csrfmiddlewaretoken": self.token}          
                                                                                                     
        response = session.post(self.STR_URL_LOGIN, data=auth, headers=self.header, 
                                 cookies=self.cookie) 
        response.raise_for_status()

        self.token = session.cookies['csrftoken']                                                           
        self.cookie = {'csrftoken':self.token}
        self.header['Referer'] = self.STR_URL_LOGIN
        
        return session   
    
    def downloadFile(self, fileURL, downloadFolder, filename):
        filename = os.path.join(downloadFolder, filename)
        self.header['Referer'] = self.STR_URL_LOGIN
        
        try:
            response = self.session.get(fileURL, stream=True, headers=self.header)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)  
            return True   
        except Exception as e:
            print "Error:", e
            return False
    
    def encode_multipart(self, fields, boundary=None):
        def escape_quote(s):
            return s.replace('"', '\\"')
    
        if boundary is None:
            boundary = ''.join(random.choice(self.BOUNDARY_CHARS) for i in range(30))
        lines = []
    
        for name, value in fields.items():
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
                '',
                str(value),
            ))
    
        lines.extend((
            '--{0}--'.format(boundary),
            '',
        ))
        body = '\r\n'.join(lines)
    
        headers = {
            'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
            'Content-Length': str(len(body)),
        }
    
        return (body, headers)

AddPlugin(Malwr)