__description__ = 'Download Sample from malc0de Repo http://malc0de.com/'
__author__ = 'Robby Zeitfuchs'
__version__ = '0.0.1'
__date__ = '2015/11/13'

class Malc0de():

    def __init__(self):
        self.downloadURLs = []
    
    def searchSample(self, sha256, sha1, md5):
        #print "Malc0de search for Sample: %s" % sha256
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
            print downloadURL
            
        #sollte das Laden erfolgreich sein -> Hash checken
    
    def getDownloadURLs(self):
        if self.downloadURLs:
            return self.downloadURLs
        else:
            raise Exception("Keine Download-URL vorhanden!") 
        
AddPlugin(Malc0de)