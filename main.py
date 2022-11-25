import MusicChecker

config = {
    'directory': '/media/library/Music/Metal/Cryptopsy/',
    'tags':'TXXX:MusicBrainz Album Artist Id'
}

retVal = MusicChecker.execute(config)
print(retVal)
for f in retVal:
    #print(f.tags)
    pass