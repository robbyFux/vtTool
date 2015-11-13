__description__ = 'Download Sample from malc0de Repo http://malc0de.com/'
__author__ = 'Robby Zeitfuchs'
__version__ = '0.0.1'
__date__ = '2015/11/13'

class Malc0de():

    downloadURLs = []
    
    # Benoetigt ein Triple: [sha256,sha1,md5]
    def searchSample(self, hashes):
        sha256,sha1,md5 = hashes
        print "Search for Sample: %s; %s; %s" % (sha256,sha1,md5)
        
        self.downloadURLs.append("xz.q58723.com/xz/setup_962_1565.exe")
        self.downloadURLs.append("xz.q58723.com/xz/setup_962_1565.exe")
        self.downloadURLs.append("xz.q58723.com/xz/setup_962_10043.exe")
        return True
        
    def isDownloadable(self):
        if self.downloadURLs:
            return True
        return False
        
    def downloadSample(self, path):
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