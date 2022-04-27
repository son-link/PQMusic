from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pathlib import Path
from urllib import request
from io import BytesIO
from functools import reduce


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


def getMetaDataUrl(url, mimetype):
    data = get_n_bytes(url, 10)

    size_encoded = bytearray(data[-4:])
    size = reduce(lambda a, b: a*128+b, size_encoded, 0)
    header = BytesIO()
    data = get_n_bytes(url, size+2881)
    # mutagen needs one full frame in order to function. Add max frame size
    header.write(data)
    header.seek(0)

    tags = {
        'album':    'Unknown',
        'artist':   'Unknown',
        'title':    'Unknown',
        'notags':   ''
    }

    info = None

    if mimetype == 'audio/mpeg':
        info = MP3(header, ID3=EasyID3)
    else:
        info = File(header)

    if info:
        if 'album' in info:
            tags['album'] = info['album'][0]
        if 'artist' in info:
            tags['artist'] = info['artist'][0]
        if 'title' in info:
            tags['title'] = info['title'][0]
        if 'title' not in info and 'artist' not in info:
            tags['notags'] = url
    else:
        tags['notags'] = url

    return tags


def get_n_bytes(url, size):
    req = request.Request(url)
    req.headers['Range'] = 'bytes=%s-%s' % (0, size-1)
    response = request.urlopen(req)
    return response.read()
