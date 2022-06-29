from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pathlib import Path
from os import (
    access,
    R_OK,
    getpid,
    remove
)
import psutil

LOCKFILE = '/tmp/pqmusic.lock'


def delLockFile():
    """ Delete the lockfile
    """
    if Path(LOCKFILE).is_file():
        remove(LOCKFILE)


def checkIfRuning():
    """ Checks if an instance of the application is already running.
        If this is the case and the -f|--force parameter is not passed
        to the program, it closes.
    """

    if Path(LOCKFILE).is_file():
        with open(LOCKFILE, 'r') as file:
            pid = file.read()
            pid = int(pid)
            file.close()
            if psutil.pid_exists(pid):
                exit()
    else:
        with open(LOCKFILE, 'w') as file:
            file.write(str(getpid()))
            file.close()
            return False


def getMetaData(filename):
    """ Return the metadata of the audio file

    Args:
        filename (str): The file patch

    Returns:
        dict: A dictionary with the metadata
    """

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
    """Open a M3U playlist file and return a array with the tracks info

    Args:
        file (str): The M3U path

    Returns:
        array: A dictionary array with all tracks on the playlist
    """

    tracks = []
    if Path(file).is_file() and access(file, R_OK):
        with open(file, encoding='utf-8', errors="ignore") as m3u:
            have_info = False
            track_info = {
                'artist':   'Unknown',
                'title':    'Unknown',
                'notags':   ''
            }

            # Files in M3U format must start with this line.
            # If it does not, it is not considered as such
            # and we terminate the function
            first_line = m3u.readline()
            if not first_line.startswith('#EXTM3U'):
                return []

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
    """Save the playlist on a M3U playlist format file

    Args:
        filename (str): the path to write the playlist
        playlist (array): The playlist array
    """
    try:
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
    except IOError as x:
        print('A error ocurrod on write {}: {}'.format(
            filename,
            x.strerror
        ))
