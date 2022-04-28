from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pathlib import Path


def getMetaData(filename):
    ext = Path(filename).suffix

    tags = {
        'album':    'Unknown',
        'artist':   'Unknown',
        'title':    'Unknown',
        'notags':   ''
    }

    info = None

    if ext == '.mp3':
        info = MP3(filename, ID3=EasyID3)
    else:
        info = File(filename)

    if info:
        if 'album' in info:
            tags['album'] = info['album'][0]
        if 'artist' in info:
            tags['artist'] = info['artist'][0]
        if 'title' in info:
            tags['title'] = info['title'][0]
        if 'title' not in info and 'artist' not in info:
            tags['notags'] = Path(filename).stem
    else:
        tags['notags'] = Path(filename).stem

    return tags
