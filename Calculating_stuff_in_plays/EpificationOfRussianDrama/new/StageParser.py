import re,codecs
import json
from lxml import etree
from os import walk
from pymystem3 import Mystem
m = Mystem()

infolder = '../TEI'
results = '../results/'
outfile = codecs.open (results+'stats_per_play_with_dirtext_and_more_stats1711.csv', 'w', 'utf-8')
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
header = ['play name','written','print', 'number of stages','len_stages_words','len_speeches_words','total_number_of_verbs','verbs set','number of unique verbs','stages_to_speeches_ratio','verb_diversity(uniqueverbs/totalverbs)','all_stage_texts']

class Play:
    def __init__(self, filename, name, written, printdate, len_speeches_words, number_stages, len_stages_words, total_number_of_verbs, verbset, number_of_unique_verbs, all_stage_texts):
        self.filename = filename
        self.name = name
        self.written = written
        self.printdate = printdate
        self.number_stages = number_stages
        self.len_stages_words = len_stages_words
        self.len_speeches_words = len_speeches_words
        #self.stages_unique_words = stages_unique_words
        self.verbset = verbset
        self.number_of_unique_verbs = number_of_unique_verbs
        self.all_stage_texts = all_stage_texts
        self.total_number_of_verbs = total_number_of_verbs
    def stages_to_speeches_ratio(self):
        return float(self.len_stages_words/self.len_speeches_words)
    def verb_diversity(self):
        return float(self.number_of_unique_verbs/self.total_number_of_verbs)
        

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
    verbcounter = 0
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
                    verbcounter+=1
                    #print (text)
                    #print (lemma)
                    verbs.add(lemma)
    return verbs, verbcounter
                

def parse_xml(path, filename):
    fullpath = path+'/'+filename
    #counter = 0
    #name = 'noname'
    #year = 'noyear'
    root = etree.parse(fullpath)
    name = getname (root)
    #print (name)
    written, printdate = getdates (root)
    thisplay = Play (filename,name,written, printdate,0,0,0,0,set(),0,'')
    
    for stage in root.iterfind ('.//tei:stage', ns):
        #counter+=1
        text = stage.text
        if text != None:
            cleantext = re.sub('\r|\n','',text)
            thisplay.number_stages +=1
            lenwords = len(m.lemmatize(text))
            thisplay.len_stages_words += lenwords
            thisverbs, thisverbscount = getverbs(text)
            for verb in thisverbs:
                thisplay.verbset.add(verb)
            thisplay.all_stage_texts += cleantext + ' '
            thisplay.total_number_of_verbs += thisverbscount
    thisplay.number_of_unique_verbs += len (thisplay.verbset)

    for anyspeech in root.iterfind ('.//tei:sp//tei:p', ns): # or .//tei:l
        anyspeech_text = anyspeech.text
        if anyspeech_text != None:
        #print (anyspeech.text)
            thisplay.len_speeches_words += len(m.lemmatize(anyspeech_text))
        
    for anyverse in root.iterfind ('.//tei:sp//tei:l', ns): # or .//tei:p        
        anyverse_text = anyverse.text
        #print (anyverse.text)
        if anyverse_text != None:
            thisplay.len_speeches_words += len(m.lemmatize(anyverse_text))  

    return (thisplay)
        


def settostring (someset):
    string =''
    for item in someset:
        string+= item+','
    return string

def write_data (play, outfile):
    #print (play.play.total_number_of_verbs)
    play_data = [play.name, play.written, play.printdate,str(play.number_stages), str(play.len_stages_words),str(play.len_speeches_words), str(play.total_number_of_verbs), settostring(play.verbset),str(play.number_of_unique_verbs), str(play.stages_to_speeches_ratio()), str(play.verb_diversity()), play.all_stage_texts]
    outfile.write ('\t'.join (play_data) + '\r\n')
    
    
outfile.write ('\t'.join(header)+'\r\n')

for path, dirs, filenames in walk (infolder):
    for filename in filenames:
        if '.xml' in filename:
            #print (filename)
            play = parse_xml (path,filename)
            write_data (play, outfile)
            #openfile = codec.open ()
            #for line in 

outfile.close()
