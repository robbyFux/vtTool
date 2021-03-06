# vtTool - VirusTotal malware naming tool

###Find the name of the evil

VT-Tool offers a convenient way of determining the likely name of malware by querying VirusTotal using the file’s hash via the command line. 

![vtTool](https://raw.githubusercontent.com/robbyFux/Tools/master/doc/vtTool.png)

##Introduction

Source file can be found here: https://raw.githubusercontent.com/robbyFux/Tools/master/src/vtTool.py

##Requirements

For use is Python 2.7 preferred.

###required

    requests: http://docs.python-requests.org/en/latest/ 

###optional dependencies

Lexical clustering requires the following dependencies:

    numpy: http://scikit-learn.org/stable/install.html
    scikit-learn: http://scikit-learn.org/stable/install.html
    FuzzyWuzzy?: https://github.com/seatgeek/fuzzywuzzy
    python-levenshtein: https://github.com/miohtama/python-Levenshtein 

##Install on Ubuntu:

`sudo apt-get -y install python-numpy python-scipy python-levenshtein`

`sudo pip install requests fuzzywuzzy scikit-learn`

`wget https://malware-crawler.googlecode.com/svn/MalwareCrawler/src/tools/vtTool.py`

`chmod a+xr vtTool.py`

`sudo mv vtTool.py /usr/local/bin`

##Usage

```
vtTool.py -h

usage: vtTool.py [-h] -hash HASHLIST [--debug] [--cluster]

VirusTotal MalwareName-Tool

optional arguments:
  -h, --help            show this help message and exit
  -hash HASHLIST, --hashlist HASHLIST
                        Malware hash or CSV Hashlist
  --debug               Debugmodus
  --cluster             Strictly lexical clustering over malware-names
```

##hash-bulk

```
for I in `cat checksums_sha256.txt| awk '{print $1}'  | sort | uniq`; do (vtTool.py -hash $I >> $I.out ); done
```

##Tests

###regin
```
vtTool.py --cluster -hash a0d82c3730bc41e267711480c8009883d1412b68977ab175421eabc34e4ef355,b12c7d57507286bbbe36d7acf9b34c22c96606ffd904e3c23008399a4a50c047
```

###hikit, hikiti
```
vtTool.py --cluster -hash 2a5a236a9a3595407fb0818c9e13db5b9c8681b874886961347cb3c027a283d6,76efffab160f28fd999ae240e305572059aee689f7463b11032b5dd3dccbf415,aa4b2b448a5e246888304be51ef9a65a11a53bab7899bc1b56e4fc20e1b1fd9f
```

###chindo
```
vtTool.py --cluster -hash 0f3320793450a4b757728ebbff2b5f89def2aa917ec9dd5534851166605d2204,0f3320793450a4b757728ebbff2b5f89def2aa917ec9dd5534851166605d2204,18ffa4f1ccd85c0a5fe4b45fc969e66ae3ed91be77056163fc28a02fb040d9ef,61f5a94e895c29412c3501036c88bef2be262e49119eb61b9f37600aaf645af5,71853eb1e60ce98dc06356ee9614b838cf9ba535827ea3f9521b6c3d79f55de9
```

###kuluoz, kuluo
```
vtTool.py --cluster -hash 2304eb9af68a9dc43297ae35212fcc9577f27bdb1735b68321edac8b42353394,9d43c7efb4debb6dea3f269c0fbb8bf81899d4cd3f8a21ab3b78b91fb21b63d8,8e9dcf22388c5479708575d206d9088466c18d37257057b449524b08802bd20f,3cd40d1f7d51cbb4d328497f68d0807547e2dfac7fa31b6b055a3cab9765e820,26ff7f50c66eeea33772a8739b15c5a2532524e1cf1b7ba46b26432ffe5dc93a
```

###kuluoz, kuluo
```
vtTool.py --cluster -hash 4b62d45f36082ff53a375ef0ae959090516a501897cc45c2fb5e94c96fc18b0f,fc98c254b04b57d9a10d10c4045e78bc10a51c2d548080bba7aabe30d9627e38,4b6dc78482c9a7c23b24d1bb577273971355e203e7a36db218cea7a8699597b0,f04bead31a6a37b6b5d002f16ca1404ee4f3487fe537ecc70cfb7ab2a64eb52a,ed2c88bcd511018df835c3172afcee46559a5c1f08bf764bdc74bd162682be34,13cbbd269a1af1d5f6f7730c67c0cbb0ff38a5bd65b07ceb22a432a7d5005c24,13cbbd269a1af1d5f6f7730c67c0cbb0ff38a5bd65b07ceb22a432a7d5005c24,fa728994a76ab0d5dfa89f262c47102550cb85db6a68a3b0b7d69005b7758e53
```

###krepper, kreepper
```
vtTool.py --cluster -hash a994343b80a0cee0efa88108e6d716e209cfedddc69dee1c828554f1a60116a0,c7c8cff02c4b23006019155f7ee19b5b1cccff17b2b0b41ae6fd8b8ce77665f3,9a56297a2fcfdff84316f2aa2d1b3233e5f1ced30ba0bdea5867e1ea3d342dcb,5b96b57ef0f5fc72cf6bfc7f00c3a3cd275630626f88ecea9fe3738d90bc15ac,fa048255536ed8d8f01130bb496165ba75a5783fb3408c87f9c1805498921e87,e61984ae095642c5eea47a7f97f7e58558701ffa771fb0764a0141971a51e162
```
