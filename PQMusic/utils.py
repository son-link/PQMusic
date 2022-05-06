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
        tags['duration'] = int(info.info.length)

    else:
        tags['notags'] = Path(filename).stem

    return tags


def openM3U(file):
    tracks = []
    if Path(file).is_file():
        with open(file, encoding='utf-8', errors="ignore") as m3u:
            have_info = False
            track_info = {
                'artist':   'Unknown',
                'title':    'Unknown',
                'notags':   ''
            }
            for line in m3u:
                line = line.rstrip()
                if not have_info:
                    if line.startswith('#EXTINF:'):
                        duration, trackname = line.split(':')[1].split(',', 1)
                        track_info = {
                            'duration': duration,
                        }
                        artist, title = trackname.split(' - ', 1)
                        track_info['artist'] = artist
                        track_info['title'] = title
                        have_info = True
                    else:
                        have_info = False
                        if Path(line).is_file():
                            track_info['notags'] = Path(line).stem
                            track_info['file'] = line
                            tracks.append(track_info)
                        track_info = {}
                else:
                    have_info = False
                    if Path(line).is_file():
                        track_info['file'] = line
                        tracks.append(track_info)
                        track_info = {}
    return tracks


def saveM3U(self, filename, playlist):
    with open(filename, 'w') as file:
        file.write("#EXTM3U\n")
        for data in playlist:
            if not data['notags']:
                file.write("#EXTINF:{},{} - {}\n".format(
                    data['duration'],
                    data['artist'],
                    data['title']
                ))
            file.write("{}\n".format(data['file']))
        file.close()
