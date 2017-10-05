#this script is intended for harvesting MARC XML files from ArchivesSpace instances and saving the locally
#written and tested with Python 3.5 and AS 1.4 on Windows 10, alterations may be needed depending on your system
#by tristan dahn, tristandahn@gmail.com

#in the following four lines you will set the parameters of the script

#set url to crawl (!!mind the slash after the url, make sure it is removed!!)
archiveUrl = 'http://cpparchives.org'

#set repository id, most AS instances have the main repository id set to 2, browse the target site to check
repoId = '2'

#set resource ID range
resourceRange = range(1000,5000)

#set path for saving .xml files locally
path = '/Users/tdahn/Documents/marcxml'

#-----------------------------------------------------------
#nothing needs to be altered from this point on

import urllib.request
import os

#create repository URL
repo = archiveUrl + '/repositories/' + repoId + '/resources/'

#save current path for returning after script is run
curPath = os.getcwd()

#change to path set above
os.chdir(path)

#create directory for saving .xml files
archiveName = archiveUrl[7:]
directory = archiveName + '_MARCXML'

if not os.path.exists(directory):
    os.makedirs(directory)

print('Exporting MarcXML from repository ' + repoId + ' of ' + archiveUrl + ' to ' + path + '/' + directory)
print('------------------------------------')

#read xml from url and write to file
for num in resourceRange:
    xmlUrl = (repo + str(num) + '/format/marcxml')
    
    print('Reading ' + xmlUrl + ' . . .')
    
    xmlString = urllib.request.urlopen(xmlUrl).read().decode()
    
    #will skip ids in range that do not refer to a resource
    if 'Record Not Found' in xmlString:
        print('No record found, moving to next resource.')
        print('------------------------------------')
        continue
    
    print('Record found, writing file . . .')
        
    #finds accession number from ead and converts in into filename format
    #(this is using string methods but appears to work, extracting the accession from the xml element tree might be more robust)
    accessionStart = xmlString.find('<subfield code="c">')
    accessionEnd = xmlString.find('</subfield>\n    </datafield>')
    accessionString = xmlString[accessionStart+19:accessionEnd]
    accessionString = accessionString.replace(' ', '_')
    accessionString = accessionString.replace('/', '_')
    
    #writes .xml file with a filename of the resource id and accession number into the directory created above
    xmlTemp = open(directory + '/' + str(num) + '-' + accessionString + '.xml', 'w', encoding='utf8')
    xmlTemp.write(xmlString)
    xmlTemp.close()
    
    print(accessionString + ' written to ' + path + '/' + directory + '/' + str(num) + '-' + accessionString + '.xml')
    print('------------------------------------')

print('Done! Exported MarcXML is in ' + path + '/' + directory)

#return to original path
os.chdir(curPath)
