import re,codecs
import json
from lxml import etree
from os import walk
from pymystem3 import Mystem
m = Mystem()

infolder = '../TEI'
results = '../results/'
outfile = codecs.open (results+'stats_per_play.csv', 'w', 'utf-8')
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
header = ['play name','written','print','number of stages','len_stages_words','verbs set','number of unique verbs']

class Play:
    def __init__(self, filename, name, written, printdate, number_stages, len_stages_words, verbset,number_of_verbs):
        self.filename = filename
        self.name = name
        self.written = written
        self.printdate = printdate
        self.number_stages = number_stages
        self.len_stages_words = len_stages_words
        #self.stages_unique_words = stages_unique_words
        self.verbset = verbset
        self.number_of_verbs = number_of_verbs

def getname (root):
    return (re.sub('\r|\n','',root.find('.//tei:titleStmt/tei:title', ns).text))

def getwhen(date):
    if 'when' in date.attrib:
        return date.attrib ['when']
    else:
        return 'not specified in tei'

def getdates (root):
    written = getwhen(root.find('.//tei:bibl/tei:bibl/tei:date[@type="written"]', ns))
    printdate = getwhen(root.find('.//tei:bibl/tei:bibl/tei:date[@type="written"]', ns))
    return (written, printdate)
    #return (.text)

def getverbs(text):
    verbs = set()
    analysis = m.analyze(text) #json.dumps(m.analyze(text)) # , ensure_ascii=False, encoding='utf-8'
    for word in analysis:
        #print (word)
        if 'analysis' in word:
            if len (word['analysis'])>0:
                word_analysis = word['analysis'][0]
            #print (word_analysis)
                lemma = word_analysis['lex']
                gram = word_analysis ['gr'].split (',')
                if gram[0] == 'V':
                    #print (text)
                    #print (lemma)
                    verbs.add(lemma)
    return verbs
                

def parse_xml(path, filename):
    fullpath = path+'/'+filename
    #counter = 0
    #name = 'noname'
    #year = 'noyear'
    root = etree.parse(fullpath)
    name = getname (root)
    #print (name)
    written, printdate = getdates (root)
    thisplay = Play (filename,name,written, printdate,0,0,set(),0)
    
    for stage in root.iterfind ('.//tei:stage', ns):
        #counter+=1
        text = stage.text
        if text != None:
            thisplay.number_stages +=1
            lenwords = len(m.lemmatize(text))
            thisplay.len_stages_words += lenwords
            for verb in getverbs(text):
                thisplay.verbset.add(verb)  
    thisplay.number_of_verbs += len (thisplay.verbset)
        
    
        #lemtext = m.lemmatize(line)
        #print (text)
    return (thisplay)
        
    #allstages = root.findall('.//stage')

def settostring (someset):
    string =''
    for item in someset:
        string+= item+','
    return string

def write_data (play, outfile):
    play_data = [play.name, play.written, play.printdate,str(play.number_stages), str(play.len_stages_words), settostring(play.verbset),str(play.number_of_verbs)]
    outfile.write (';'.join (play_data) + '\r\n')
    
    
outfile.write (';'.join(header)+'\r\n')

for path, dirs, filenames in walk (infolder):
    for filename in filenames:
        if '.xml' in filename:
            #print (filename)
            play = parse_xml (path,filename)
            write_data (play, outfile)
            #openfile = codec.open ()
            #for line in 

outfile.close()
