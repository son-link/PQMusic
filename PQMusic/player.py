from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaPlaylist,
    QMediaContent,
    QMediaMetaData,
)
from PyQt5.QtCore import QUrl, QCoreApplication, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QStandardItem
from PyQt5 import QtWidgets
from pathlib import Path
from .utils import getMetaData, openM3U, saveM3U
from urllib.parse import urlparse
from os import path, access, R_OK, mkdir, environ
from .sys_notify import Notification, init

import magic

_translate = QCoreApplication.translate
LOCAL_DIR = path.dirname(path.realpath(__file__))
COVER_CACHE = environ['HOME'] + '/.cache/pqmusic'

if not path.exists(COVER_CACHE):
    mkdir(COVER_CACHE)


def ms_to_time(t):
    '''
    Convert nanoseconds to hours, minutes and seconds
    '''
    s, ns = divmod(t, 1000)
    m, s = divmod(s, 60)

    if m < 60:
        return "0:%02i:%02i" % (m, s)
    else:
        h, m = divmod(m, 60)
        return "%i:%02i:%02i" % (h, m, s)


class Player(QMediaPlayer):
    def __init__(self, parent):
        super(Player, self).__init__(parent)
        self.parent = parent
        self.player = QMediaPlayer()
        self.queueList = QMediaPlaylist()
        self.player.setPlaylist(self.queueList)
        self.queueData = []
        self.position = 0
        self.prevPosition = -1
        self.volume = 100

        init('pqmusic')

        self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.player.positionChanged.connect(self.qmp_positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.queueList.currentIndexChanged.connect(self.playlistPosChanged)

    def addFile(self, file):
        """ Add a file to the playlist """
        if self.checkValidFile(file):
            self.queueList.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
            tags = getMetaData(file)

            if tags['notags']:
                item = QStandardItem(tags['notags'])
            else:
                item = QStandardItem('{} - {}'.format(
                    tags['artist'],
                    tags['title']
                ))

            tags['file'] = file

            self.parent.plModel.appendRow(item)
            self.queueData.append(tags)
            self.parent.playButton.setEnabled(True)
            self.parent.repeatButton.setEnabled(True)
            self.parent.timeSlider.setEnabled(True)
            self.parent.queueNextButton.setEnabled(True)
            if self.queueList.mediaCount() > 1:
                self.parent.suffleButton.setEnabled(True)

    def addUrl(self, url, mimetype):
        """ Add a URL to the playlist.
            Args:
                url : str
                    The URL to add
                mimetype:
                    The URL mimetype
        """
        self.queueList.addMedia(QMediaContent(QUrl(url)))
        if mimetype.startswith('audio/'):
            parse = urlparse(url)
            filename = path.basename(parse.path)
            self.parent.plModel.appendRow(QStandardItem(filename))
            self.parent.playButton.setEnabled(True)
            self.parent.timeSlider.setEnabled(True)
            self.parent.queueNextButton.setEnabled(True)

    def changePos(self, pos):
        """ Change the playlist position to the position indicted.
            Args:
                pos : int
                    The new playlist position
        """
        self.queueList.setCurrentIndex(pos)
        self.playlistPosChanged()
        if (
            self.player.state() == QMediaPlayer.StoppedState or
            self.player.state() == QMediaPlayer.PausedState
        ):
            self.player.play()

    def checkValidFile(self, file):
        """ Check if the file is a valid audio file.
            Args:
                file : str
                    Path to the file
            Returns:
                True is valid, False is not
        """
        if access(file, R_OK):
            f = magic.Magic(mime=True)

            if f.from_file(file).startswith('audio'):
                return True

        return False

    def delete(self, position):
        """ Delete the track and her data from position.
            Args:
                position : int
                    The current playlist position
        """
        self.queueList.removeMedia(position)
        if self.queueList.mediaCount() > 0:
            if position == self.position:
                self.playlistPosChanged()
        else:
            self.parent.clearMetadata()
            self.stop()

    def durationChanged(self, duration):
        """ This function is called when the duration of the track changes,
            mainly when changing tracks.
            Args:
                duration : int
                    The current track duration in milliseconds
        """
        total_time = '0:00:00'
        duration = self.player.duration()

        if duration > 0:
            total_time = ms_to_time(duration)
            self.parent.timeSlider.setMaximum(duration)
            self.parent.timeSlider.setEnabled(True)
            self.currentTrackDuration = duration
            self.parent.totalTimeLabel.setText(total_time)

    def metaDataChanged(self):
        """ This function is called whenever the metadata changes,
            e.g. track changes or is received during a live stream.
        """
        self.parent.tray.setToolTip('')
        artist = None
        title = None
        notifyIcon = LOCAL_DIR + '/icon.svg'

        file = self.player.currentMedia().canonicalUrl().toString()
        if self.player.isMetaDataAvailable():
            if self.player.metaData(QMediaMetaData.Title):
                self.parent.titleLabel.setText(
                    self.player.metaData(QMediaMetaData.Title)
                )
                title = self.player.metaData(QMediaMetaData.Title)
            else:
                self.parent.titleLabel.setText(
                    Path(file).stem
                )
                title = Path(file).stem

            if self.player.metaData(QMediaMetaData.AlbumArtist):
                self.parent.artistLabel.setText(
                    self.player.metaData(QMediaMetaData.AlbumArtist)
                )
                artist = self.player.metaData(QMediaMetaData.AlbumArtist)
            elif self.player.metaData(QMediaMetaData.ContributingArtist):
                artist = self.player.metaData(
                    QMediaMetaData.ContributingArtist
                )

                if type(artist) is list:
                    artist = artist[0]

                self.parent.artistLabel.setText(artist)
            else:
                self.parent.artistLabel.setText(
                    _translate('MainWindow', 'Unknown')
                )

            self.parent.albumLabel.setText(
                self.player.metaData(QMediaMetaData.AlbumTitle)
            )

            if self.player.metaData(QMediaMetaData.CoverArtImage):
                cover = self.player.metaData(QMediaMetaData.CoverArtImage)
                cover = QPixmap.fromImage(cover)
                scaledCover = cover.scaled(
                    QSize(128, 128),
                    Qt.KeepAspectRatio,
                    transformMode=Qt.SmoothTransformation
                )
                self.parent.labelCover.setPixmap(scaledCover)
                coverName = Path(file).stem + '.png'
                notifyIcon = COVER_CACHE + '/' + coverName
                if not path.isfile(notifyIcon):
                    scaledCover.save(notifyIcon, 'PNG')
            else:
                cover = QPixmap(':/no_cover.svg')
                self.parent.labelCover.setPixmap(
                    cover.scaled(QSize(128, 128), Qt.KeepAspectRatio)
                )

        if artist:
            trayTooltip = '{} - {}'.format(artist, title)
        else:
            trayTooltip = title

        if trayTooltip:
            self.parent.setWindowTitle('PQMusic: ' + trayTooltip)
            self.parent.tray.setToolTip(trayTooltip)

            if self.parent.config['shownotify']:
                n = Notification(
                    'PQMusic',
                    trayTooltip,
                    notifyIcon,
                    timeout=3000
                )
                n.show()

    def openPlaylist(self, file=None):
        """ Opens the dialog to select files to add """
        if not file:
            file, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.parent,
                _translate('MainWindow', 'Select playlist to open'),
                self.parent.config['musicfolder'],
                _translate(
                    'MainWindow',
                    'Playlists (*.m3u *.m3u8)'
                ),
            )

        startPlay = (self.queueList.mediaCount() == 0)
        if file:
            tracks = openM3U(file)
            for track in tracks:
                if 'notags' in track:
                    item = QStandardItem(track['notags'])
                else:
                    item = QStandardItem('{} - {}'.format(
                        track['artist'],
                        track['title']
                    ))
                self.queueList.addMedia(
                    QMediaContent(QUrl.fromLocalFile(track['file']))
                )
                self.parent.plModel.appendRow(item)
                self.queueData.append(track)

            if startPlay:
                self.parent.playButton.setEnabled(True)
                self.parent.repeatButton.setEnabled(True)
                self.parent.timeSlider.setEnabled(True)
                self.parent.queueNextButton.setEnabled(True)
                self.startPlay()

    def playlistPosChanged(self):
        """ This function is called when the position
            on the playlist is change
        """
        self.parent.timeSlider.setValue(0)
        self.parent.timeSlider.setEnabled(False)
        if self.queueList.mediaCount() > 0:
            pos = self.queueList.currentIndex()

            if self.queueList.mediaCount() > 1:
                if pos < self.queueList.mediaCount() - 1:
                    self.parent.queueNextButton.setEnabled(True)
                else:
                    self.parent.queueNextButton.setEnabled(False)

                if pos > 0:
                    self.parent.queuePrevButton.setEnabled(True)
                else:
                    self.parent.queuePrevButton.setEnabled(False)

            if self.prevPosition > -1:
                prevItem = self.parent.playlistView.model().item(
                    self.prevPosition
                )

                if prevItem:
                    font = prevItem.font()
                    font.setBold(False)
                    prevItem.setFont(font)

            self.position = pos
            self.prevPosition = pos
            item = self.parent.playlistView.model().item(pos)
            if (item):
                font = item.font()
                font.setBold(True)
                item.setFont(font)

    def playPause(self):
        """ Start/Pause the current track """
        icon = QIcon.fromTheme("media-playback-pause")

        if self.player.state() == QMediaPlayer.StoppedState:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                if self.queueList.mediaCount() != 0:
                    self.player.play()
            elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
                self.queueList.setCurrentIndex(self.position)
                self.player.play()
            elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
                self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            icon = QIcon.fromTheme("media-playback-start")
            self.player.pause()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

        self.parent.playButton.setIcon(icon)
        self.parent.trayPlay.setIcon(icon)

    def qmp_mediaStatusChanged(self):
        """ This function is called when the media status is change. """
        icon = QIcon.fromTheme("media-playback-pause")
        if self.player.state() == QMediaPlayer.StoppedState:
            icon = QIcon.fromTheme("media-playback-start")
        elif self.player.state() == QMediaPlayer.PausedState:
            icon = QIcon.fromTheme("media-playback-start")

        self.parent.playButton.setIcon(icon)
        self.parent.trayPlay.setIcon(icon)

    def qmp_positionChanged(self, position, senderType=False):
        """ This function is called when the time track is change
            and update the label.
            Args:
                position : int
                    The current time in milliseconds
        """
        self.currentTime = position
        current_time = '0:00:00'

        if position != -1:
            current_time = ms_to_time(position)

        self.parent.timeLabel.setText(current_time)

        self.parent.timeSlider.blockSignals(True)
        self.parent.timeSlider.setValue(position)
        self.parent.timeSlider.blockSignals(False)

    def savePlaylist(self):
        """ Opens the dialog to save the playlist """
        file, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.parent,
            _translate('MainWindow', 'Save the playlist'),
            self.parent.config['musicfolder'],
            _translate(
                'MainWindow',
                'Playlists (*.m3u *.m3u8)'
            ),
        )
        if file:
            saveM3U(self, file, self.queueData)

    def setPosition(self, pos):
        """ Change the playlist position
            Args:
                pos : int
                    The new playlist position to play
        """
        self.player.setPosition(pos)

    def setRepeatMode(self):
        """ Change repeat track mode between sequential and loop """
        checked = self.parent.repeatButton.isChecked()
        if checked:
            self.queueList.setPlaybackMode(
                QMediaPlaylist.CurrentItemInLoop
            )
        else:
            self.queueList.setPlaybackMode(
                QMediaPlaylist.Sequential
            )

    def setVolume(self, volume):
        """ Set the volume """
        self.player.setVolume(volume)

    def startPlay(self):
        """ Automatically starts playback from the first song """
        self.queueList.setCurrentIndex(0)
        self.player.play()
        icon = QIcon.fromTheme("media-playback-pause")
        self.parent.playButton.setIcon(icon)

    def stop(self):
        """ Stop playback """
        self.player.stop()
        icon = QIcon.fromTheme("media-playback-start")
        self.parent.playButton.setIcon(icon)

    def switchRandomMode(self):
        """ Switch between sequential and random modes """
        checked = self.parent.suffleButton.isChecked()
        if checked:
            self.queueList.setPlaybackMode(
                QMediaPlaylist.Random
            )
        else:
            self.queueList.setPlaybackMode(
                QMediaPlaylist.Sequential
            )
