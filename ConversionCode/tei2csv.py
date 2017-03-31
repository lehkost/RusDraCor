import codecs, re
import xml.etree.ElementTree as ET
from os import walk


infolder = '../ilibrary/TEI_OrdinaryV1' ##'../feb-web'
outfolder =  '../ilibrary/CSV_OrdinaryV1/'## '../feb-web_csv'

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


## add edge (as string) to a dictionary of edges (one per file) 
def addedge (edgesdict, someedge):
    if someedge in edgesdict:
        edgesdict[someedge]+=1
    else:
        edgesdict[someedge]=1

## convert a set of nodes edges and add them to dictionary of edges (one per file) 
def nodestoedges (nodeset, edgeslist):
    tempedgeset = set()
    for source in nodeset:
        for target in nodeset:
            if source != target:
                edge = sorted([source, target])
                edgeasstring = ';Undirected;'.join(edge)
                if edgeasstring not in  tempedgeset:
                    addedge (edgeslist, edgeasstring)
                    tempedgeset.add (edgeasstring)


## parse a list of speeches (<sp>) and add all values of @who to 
def getnodes (speeches):
    
    nodes_to_connect = set()
    for sp in speeches:
        #print (sp.tag)
        #print (sp.attrib)
        #print (sp.attrib['who'])
        if 'who' in sp.attrib:
            speaker = re.sub ('\#','',sp.attrib['who'])
            nodes_to_connect.add(speaker)
    
    #print ('nodes_to_connect in getnodes')
    #print (nodes_to_connect)
    return nodes_to_connect
            
        
##def parsediv(div):
##    speeches = div.findall ('tei:sp', ns)
##    if len (speeches) > 0:
##        #print (len(speeches))
##        #print ('launch get nodes')
##        nodes_in_this_div = getnodes(speeches)
##        #print ('nodes_to_connect in parsediv')
##        #print (nodes_in_this_div)
##        return nodes_in_this_div
##    else:
##        subdivs = div.findall ('tei:div', ns)
##        if len (subdivs) >0:
##            for subdiv in subdivs:
##                parsediv(subdiv)


def parsedivs (divs, allfilelinks):
    
    for div in divs:
        speeches = div.findall ('tei:sp', ns)
        if len (speeches) > 0:
            #print (len(speeches))
            #print ('launch get nodes')
            nodes_in_this_div = getnodes(speeches)
            #print ('nodes_to_connect in parsedivs')
            #print (nodes_in_this_div)
            allfilelinks.append (nodes_in_this_div)
        else:
            subdivs = div.findall ('tei:div', ns)
            if len (subdivs) >0:
                #for subdiv in subdivs:
                parsedivs(subdivs, allfilelinks)
        

def parse_xml_to_network (filepath):
    tree= ET.parse (filepath)
    tei = tree.getroot()
    text = tei[1]
    #print (text.tag)
    body = text.find('tei:body', ns)
    #print (body.tag)
    divs = body.findall ('tei:div', ns)
    allinks = []
    parsedivs (divs, allinks)

    
##    for div in divs:
##        divnodes = parsediv(div)
##        print ('nodes_to_connect in parsexml')
##        print (divnodes)
##        allinks.append (divnodes)
    #print ('ALL LINKS!')
    #print (allinks)
    return allinks
        
        

def parse_folder (folderwithtei, folderwithcsv): 
    for path, dirs, filenames in walk (folderwithtei):
        for filename in filenames:
            if '.xml' in filename:
                outfile = codecs.open (folderwithcsv+re.sub('.xml','.csv', filename), 'w', 'utf-8')
                outfile.write ('Source;Type;Target;Weight\r\n')
                print (filename)
                nodeslist = parse_xml_to_network (path+'/'+filename)
                file_edges = {}
                for nodes in nodeslist:
                    nodestoedges (nodes, file_edges)
                #print (file_edges)
                for singleedge in  file_edges:
                    #print (singleedge)
                    weight =  file_edges[singleedge] 
                    outfile.write (singleedge+';'+str(weight)+'\r\n')
                outfile.close()
            
parse_folder (infolder, outfolder)            
            
