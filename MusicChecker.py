import LinuxHelper as lh
import os
import mimetypes
from MusicFile import MusicFile as mf
import mutagen
import copy
import json
import Cache
import argparse

appName = 'MusicChecker'
useHome = True
fileAge = 5
cacheDirectory = lh.getCacheDirectory() + appName


def __init_argparse() -> argparse.ArgumentParser:

	parser = argparse.ArgumentParser(
		usage="%(prog)s [OPTION] [FILE]...",
		description="<program_description"
	)

	parser.add_argument(
		"-v", "--version", action="version",
		version=f"{parser.prog} version 0.01"
	)
	###
	# Add Custom arguments here with add_argument
	###
	parser.add_argument('-d', '--directory', nargs=1, default='',
				help='Directory to search')
	parser.add_argument('-t', '--tags', nargs=1, default='',
				help='Tags to validate')

	args = parser.parse_args()
	return parser


# 001 Build File List
def buildList(rootPath, compatibleTypes=['audio/mpeg','audio/x-flac']):
	'''
	Takes a string representing a path and returns a list of MusicFiles
	'''
	returnArray = []
	i = 0
	for root, dirs, filenames in os.walk(rootPath):
		for f in filenames:
			i = i + 1
			#if i > 15000:
				#return returnArray
			fullpath = os.path.join(root, f)
			mt = mimetypes.guess_type(fullpath, True)
			#print(fullpath,mt)
			if mt[0] in compatibleTypes:
				fileObj = mf(path=root, fileName=f, fileType=mt[0])
				returnArray.append(fileObj)
	return returnArray

def _readCache(file, tagList):
	global useHome, cacheDirectory, fileAge
	fileName = lh.encodeMD5(file.fileName)
	config = {
		'home': useHome,
		'cache': os.path.join(cacheDirectory,lh.encodeMD5(','.join(tagList))),
		'file': fileName,
		'time': fileAge,
		'dump': True
	}
	output = Cache.readCache(config)
	#print(output)
	if output['valid']:
		return output['content'][0]
	return False

def _writeCache(file, tagList):
	global useHome, cacheDirectory, fileAge
	fileName = lh.encodeMD5(file.fileName)
	config = {
		'home': useHome,
		'cache': os.path.join(cacheDirectory,lh.encodeMD5(','.join(tagList))),
		'file': fileName,
		'time': fileAge,
		'dump': False,
		'write': json.dumps(file.tags)
	}
	Cache.writeCache(config)
	return

#002 Extract Tags

def extractTags(fileList, tagList):
	returnList = fileList
	#print(tagList)
	for file in returnList:
		check = _readCache(file, tagList)
		if check is False:
			if file.fileType == 'audio/mpeg':
				getMP3Tags(file, tagList, True)
			if file.fileType != 'audio/mpeg':
				continue
		else:
			file.tags = json.loads(check)
	return returnList



#003 MP3
def getMP3Tags(file, tagList, cache=False):
	'''
	Using a MusicFile object and list of tag keys returns the MusicFile with the tags found
	'''
	try:
		pathToSong = os.path.join(file.path,file.fileName)
		m = mutagen.File(pathToSong)
		tags = m.tags
		if tags == None:
			pass
		else:
			tagsObj = {}
			for v in tagList:
				if v in tags:
					#print(tags[v])
					tagsObj[v] = str(tags[v])
					#print(tagsObj)
			file.tags = copy.deepcopy(tagsObj)
			if cache:
				_writeCache(file, tagList)
			return file
	except Exception as err:
		file.error = f"Unexpected {err=}, {type(err)=}"
		pass

#004 FLAC

#005 Return

def __validateConfig(config):
	config['tags'] = config['tags'].split(',')
	return config

def execute(config):
	config = __validateConfig(config)
	if not config:
		return False
	returnJSON = False
	fileList = buildList(config['directory'])
	tags = extractTags(fileList, config['tags'])
	returnJSON = tags
	return returnJSON

def main():
	args = __init_argparse()
	config = {
		'directory': args.directory,
		'tags':args.taglist
	}
	returnJSON = execute(config)
	print(returnJSON)

if __name__ == '__main__':
	main()