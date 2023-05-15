from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pathlib import Path
from os import (
    access,
    R_OK,
    getpid,
    remove,
    environ,
)
from os.path import isfile
from PyQt5 import QtDBus, QtCore
import psutil
from random import randint

LOCKFILE = '/tmp/pqmusic.lock'
COVER_CACHE = environ['HOME'] + '/.cache/pqmusic'
last_notify_body = ''


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

    trackers_extensions = ['s3m', 'xm', 'mod', 'it']
    ext = Path(filename).suffix
    ext = ext.replace('.', '').lower()

    tags = {
        'album':    'Unknown',
        'artist':   'Unknown',
        'title':    'Unknown',
        'notags':   ''
    }

    info = None

    if ext in trackers_extensions:
        tags['title'] = getTrackerTitle(filename, ext)
        tags['artist'] = ''
        return tags
    elif ext == 'mp3':
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

                        if int(duration) > 0:
                            artist, title = trackname.split(' - ', 1)
                            track_info['artist'] = artist
                            track_info['title'] = title
                            have_info = True
                        else:
                            track_info['notags'] = trackname
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
                if 'notags' not in data or not data['notags']:
                    if not data['artist']:
                        file.write(f"#EXTINF:0,{data['title']}\n")
                    else:
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


def saveVolume(volume):
    with open(COVER_CACHE + '/volume', 'w') as f:
        f.write(str(volume))
        f.close()


def getSaveVolume():
    volfile = COVER_CACHE + '/volume'
    if not isfile(volfile):
        return 100

    with open(volfile, 'r') as f:
        volume = int(f.readline())
        f.close()
        remove(volfile)
        return volume


def getTrackerTitle(filepath, ext=None):
    """Return the title of some Music Trackers formats

    Args:
        filepath (str): the path to the file
    Return:
        (str) The title if available or empty string
    """
    title = ''

    trackers_extensions = ['s3m', 'xm', 'mod', 'it']
    filepath = filepath.replace('file://', '')

    if not ext:
        ext = Path(filepath).suffix
        ext = ext.replace('.', '').lower()
        if ext not in trackers_extensions:
            return ''

    with open(filepath, 'rb') as f:
        head = f.read(128)
        if ext == 'xm':
            title = head[17:37]
        elif ext == 's3m':
            title = head[0:28]
        elif ext == 'mod':
            title = head[0:20]
        elif ext == 'it':
            title = head[4:26]

        title = title.decode('utf-8', 'ignore').strip()
        fil = filter(str.isprintable, title)
        title = "".join(fil)
        return title


def notify(title, body='', icon='', timeout=-1):
    global last_notify_body
    # Prevent send many notifications
    if body == last_notify_body:
        return

    last_notify_body = body

    item = "org.freedesktop.Notifications"
    path = "/org/freedesktop/Notifications"
    interface = "org.freedesktop.Notifications"
    app_name = "pqmusic"

    # random int to identify all notifications
    v = QtCore.QVariant(randint(1000, 10000))

    if v.convert(QtCore.QVariant.UInt):
        id_replace = v

    actions_list = QtDBus.QDBusArgument([], QtCore.QMetaType.QStringList)
    hint = {}

    bus = QtDBus.QDBusConnection.sessionBus()
    if not bus.isConnected():
        print("Not connected to dbus!")

    notify = QtDBus.QDBusInterface(item, path, interface, bus)

    if notify.isValid():
        x = notify.call(QtDBus.QDBus.AutoDetect, "Notify", app_name,
                        id_replace, icon, title, body,
                        actions_list, hint, timeout)
        if x.errorName():
            print("Failed to send notification!")
            print(x.errorMessage(), x.errorName())
    else:
        print("Invalid dbus interface")
