import LinuxHelper as lh
import os
import sys
import mimetypes
from File import File as F
from MusicFile import MusicFile as mf
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import MusicBrainzAPI
import copy

#001 Build File List
def buildList(rootPath):
    returnArray = []
    i = 0
    for root, dirs, filenames in os.walk(rootPath):
        for f in filenames:
            i = i + 1
            if i > 15000:
                return returnArray
            fullpath = os.path.join(root, f)
            mt = mimetypes.guess_type(fullpath, True)
            #print(fullpath,mt)
            compatibleTypes = ['audio/mpeg','audio/x-flac']
            if mt[0] in compatibleTypes:
                fileObj = mf(path=root, fileName=f, fileType=mt[0])
                returnArray.append(fileObj)
    return returnArray
#002 Extract Tags

def extractTags(fileList, tagList):
    returnList = fileList
    i = 0
    for file in returnList:
        i = i + 1
        #print(file.tags)
        #print(file.fileName)
        if i > 15000:
            continue
        if file.fileType != 'audio/mpeg':
            continue
        try:
            pathToSong = os.path.join(file.path,file.fileName)
            #print(pathToSong)
            m = mutagen.File(pathToSong)
            tags = m.tags
            #print(tags)
            if tags == None:
                pass
            else:
                for v in tagList:
                    #print(v)
                    if v in tags:
                        #print('found')
                        #print({v[0]:str(v[1])})
                        tagsObj = {tags[0]:str(tags[1])}
                        print(tagsObj)
                        file.tags = copy.deepcopy(tagsObj)
                        #print(file.tags)

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            pass
        
    return returnList
#003 MP3

#004 FLAC

#005 Return
fileList = buildList('/media/library/Music/')

fileList = extractTags(fileList, ['MUSICBRAINZ_ARTISTID'])
#print(fileList[0].tags)
print('finished')
for file in fileList:
    #print(MusicBrainzAPI.getReleasesByArtist(fileList[0].tags[0]['MUSICBRAINZ_ARTISTID']))
    print(fileList[0].tags)
    pass
#print(fileList[0].path,fileList[0].fileName,fileList[0].fileType, fileList[0].tags)
