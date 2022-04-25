from .ui import Ui_gui
from .player import Player
from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
    QLocale,
    QTranslator,
    QTimer,
    QSize
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import (
    QIcon,
    QCursor,
    QPixmap,
    QStandardItemModel,
    QFont,
    QFontDatabase
)
from os import path

_translate = QCoreApplication.translate


class MainWindow(QtWidgets.QMainWindow, Ui_gui.Ui_MainWindow):
    """
    The main window
    """
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.player = Player(self)

        self.plModel = QStandardItemModel()
        self.playlistView.setModel(self.plModel)

        # Hide the playlisy layout
        self.playListFrame.hide()
        QTimer.singleShot(0, self.adjustSize)

        self.timeSlider.valueChanged.connect(self.player.setPosition)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)
        self.playButton.clicked.connect(self.player.playPause)
        self.playlistView.doubleClicked.connect(self.changeTrack)
        self.queuePrevButton.clicked.connect(self.player.queueList.previous)
        self.queueNextButton.clicked.connect(self.player.queueList.next)
        self.playlistButton.clicked.connect(self.showHidePlaylist)
        self.listRemoveButton.clicked.connect(self.delTracks)
        self.listClearButton.clicked.connect(self.clearPlaylist)

        # Menu
        trayMenu = QtWidgets.QMenu()
        self.menuAdd = QtWidgets.QAction(
            QIcon.fromTheme('list-add'),
            _translate('MainWindow', 'Add file(s)'),
            trayMenu
        )
        self.menuAdd.triggered.connect(self.open_files)
        trayMenu.addAction(self.menuAdd)

        self.menuButton.setMenu(trayMenu)

        # Volume
        icon = QIcon.fromTheme("audio-volume-high")
        self.iconVol.setPixmap(icon.pixmap(16, 16))
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setValue(self.player.volume)

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            _translate('MainWindow', 'Select file to open'),
            '',
            _translate('MainWindow', 'Audio (*.mp3 *.ogg *.opus *.aac *.m4a *.flac *.wav)'),
        )

        if file:
            self.player.add(file)

    def open_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            _translate('MainWindow', 'Select file to open'),
            '',
            _translate('MainWindow', 'Audio (*.mp3 *.ogg *.opus *.aac *.m4a *.flac *.wav)'),
        )

        startPlay = (self.player.queueList.mediaCount() == 0)
        if files:
            for file in files:
                self.player.add(file)

            if startPlay:
                self.player.startPlay()

    def changeTrack(self, w):
        row = w.row()
        self.player.changePos(row)

    def showHidePlaylist(self):
        if self.playlistButton.isChecked():
            self.playListFrame.show()
        else:
            self.playListFrame.hide()

        QTimer.singleShot(0, self.adjustSize)

    def delTracks(self):
        model = self.playlistView.selectionModel()
        indexes = model.selectedIndexes()
        indexes.sort(reverse=True)
        items = [self.playlistView.model().itemFromIndex(index) for index in indexes]
        for item in items:
            pos = item.row()
            self.playlistView.model().removeRow(pos)
            self.player.delete(pos)

    def clearPlaylist(self):
        model = self.playlistView.model()
        model.removeRows(0, model.rowCount())
        self.player.stop()
        self.player.queueList.clear()
        self.clearMetadata()

    def clearMetadata(self):
        self.titleLabel.setText('')
        self.artistLabel.setText('')
        self.albumLabel.setText('')

        cover = QPixmap('no-cover.png')
        self.labelCover.setPixmap(
            cover.scaled(QSize(128, 128), Qt.KeepAspectRatio)
        )

        self.queuePrevButton.setEnabled(False)
        self.queueNextButton.setEnabled(False)
        self.playButton.setEnabled(False)
        self.timeSlider.setEnabled(False)


def init():
    LOCAL_DIR = path.dirname(path.realpath(__file__))
    app = QtWidgets.QApplication([])
    '''defaultLocale = QLocale.system().name()
    if defaultLocale == 'es_ES':
        defaultLocale = 'es'

    translator = QTranslator()
    translator.load(LOCAL_DIR + "/locales/" + defaultLocale + ".qm")
    app.installTranslator(translator)'''

    QFontDatabase.addApplicationFont('OpenSans.ttf')

    with open(LOCAL_DIR + '/style.qss', 'r', encoding='utf8') as fh:
        app.setStyleSheet(fh.read())

    searchPaths = QIcon.fallbackSearchPaths()
    searchPaths.append(':/icons')
    QIcon.setFallbackSearchPaths(searchPaths)
    QIcon.setThemeName('luv')

    window = MainWindow()
    window.retranslateUi(window)
    window.show()
    app.exec_()
