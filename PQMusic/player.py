from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaPlaylist,
    QMediaContent,
    QMediaMetaData,
)
from PyQt5.QtCore import QUrl, QCoreApplication, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QStandardItem
from pathlib import Path
from .utils import getMetaData
from urllib.parse import urlparse
from os import path

import magic

_translate = QCoreApplication.translate


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
    def __init__(self, parent=None):
        super(Player, self).__init__(parent)
        self.parent = parent
        self.player = QMediaPlayer()
        self.queueList = QMediaPlaylist()
        self.player.setPlaylist(self.queueList)
        self.queueData = []
        self.position = 0
        self.prevPosition = -1
        self.volume = 100

        self.player.mediaStatusChanged.connect(self.qmp_mediaStatusChanged)
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.player.positionChanged.connect(self.qmp_positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.queueList.currentIndexChanged.connect(self.playlistPosChanged)

    def addFile(self, file):
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

            self.parent.plModel.appendRow(item)
            self.parent.playButton.setEnabled(True)
            self.parent.timeSlider.setEnabled(True)
            self.parent.queueNextButton.setEnabled(True)

    def addUrl(self, url, mimetype):
        self.queueList.addMedia(QMediaContent(QUrl(url)))
        if mimetype.startswith('audio/'):
            parse = urlparse(url)
            filename = path.basename(parse.path)
            self.parent.plModel.appendRow(QStandardItem(filename))
            self.parent.playButton.setEnabled(True)
            self.parent.timeSlider.setEnabled(True)
            self.parent.queueNextButton.setEnabled(True)

    def playPause(self):
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

    def startPlay(self):
        self.queueList.setCurrentIndex(0)
        self.player.play()
        icon = QIcon.fromTheme("media-playback-pause")
        self.parent.playButton.setIcon(icon)

    def stop(self):
        self.player.stop()
        icon = QIcon.fromTheme("media-playback-start")
        self.parent.playButton.setIcon(icon)

    def setPosition(self, pos):
        self.player.setPosition(pos)

    def durationChanged(self, duration):
        total_time = '0:00:00'
        duration = self.player.duration()

        if duration > 0:
            total_time = ms_to_time(duration)
            self.parent.timeSlider.setMaximum(duration)
            self.parent.timeSlider.setEnabled(True)
            self.currentTrackDuration = duration
            self.parent.totalTimeLabel.setText(total_time)

    def qmp_mediaStatusChanged(self, status):
        icon = QIcon.fromTheme("media-playback-pause")
        if self.player.state() == QMediaPlayer.StoppedState:
            icon = QIcon.fromTheme("media-playback-start")
        elif self.player.state() == QMediaPlayer.PausedState:
            icon = QIcon.fromTheme("media-playback-start")

        self.parent.playButton.setIcon(icon)

    def qmp_positionChanged(self, position, senderType=False):
        self.currentTime = position
        current_time = '0:00:00'

        if position != -1:
            current_time = ms_to_time(position)

        self.parent.timeLabel.setText(current_time)

        self.parent.timeSlider.blockSignals(True)
        self.parent.timeSlider.setValue(position)
        self.parent.timeSlider.blockSignals(False)

    def playlistPosChanged(self):
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

    def setVolume(self, volume):
        self.player.setVolume(volume)

    def delete(self, position):
        """ Delete the track and her data from position"""
        self.queueList.removeMedia(position)
        if self.queueList.mediaCount() > 0:
            if position == self.position:
                self.playlistPosChanged()
        else:
            self.parent.clearMetadata()
            self.stop()

    def changePos(self, pos):
        self.queueList.setCurrentIndex(pos)
        self.playlistPosChanged()
        if (
            self.player.state() == QMediaPlayer.StoppedState or
            self.player.state() == QMediaPlayer.PausedState
        ):
            self.player.play()

    def metaDataChanged(self):
        if self.player.isMetaDataAvailable():
            if self.player.metaData(QMediaMetaData.Title):
                self.parent.titleLabel.setText(
                    self.player.metaData(QMediaMetaData.Title)
                )
            else:
                file = self.player.currentMedia().canonicalUrl().toString()

                self.parent.titleLabel.setText(
                    Path(file).stem
                )

            if self.player.metaData(QMediaMetaData.AlbumArtist):
                self.parent.artistLabel.setText(
                    self.player.metaData(QMediaMetaData.AlbumArtist)
                )
            elif self.player.metaData(QMediaMetaData.ContributingArtist):
                artist = self.player.metaData(
                    QMediaMetaData.ContributingArtist
                )

                if type(artist) is list:
                    self.parent.artistLabel.setText(artist[0])
                else:
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
            else:
                cover = QPixmap(':/no_cover.svg')
                self.parent.labelCover.setPixmap(
                    cover.scaled(QSize(128, 128), Qt.KeepAspectRatio)
                )

    def checkValidFile(self, file):
        f = magic.Magic(mime=True)
        if f.from_file(file).startswith('audio'):
            return True
        return False
