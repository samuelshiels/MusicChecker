# MusicChecker
Scripts to load information from Music files and common validation and checks you may want to perform on them

# Usage

```python
import MusicChecker
config = {
    'directory': '/music',
    'tags':'TXXX:MusicBrainz Album Artist Id'
}
output = MusicChecker.execute(config)
```
Output is a list of MusicFile objects that contain the tags specified in the config input

Supports MP3