from .ui import Ui_gui, open_url_dialog
from .player import Player
from .utils import delLockFile
from .config import ConfigDialog
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
    QPixmap,
    QStandardItemModel,
    QFontDatabase
)
from os import path, listdir, getcwd
from sys import exit as sysExit
from pathlib import Path

_translate = QCoreApplication.translate
add_files = []


class MainWindow(QtWidgets.QMainWindow, Ui_gui.Ui_MainWindow):
    """
    The main window
    """
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.isMWShow = True
        self.player = Player(self)
        self.plModel = QStandardItemModel()
        self.playlistView.setModel(self.plModel)
        self.resize_event = False
        self.setAcceptDrops(True)
        self.config = ConfigDialog.loadConf()

        # Hide the playlisy layout
        self.blockSignals(True)
        self.playListFrame.hide()
        self.adjustSize()
        self.blockSignals(False)
        self.resize_event = True

        self.listClearButton.clicked.connect(self.clearPlaylist)
        self.listRemoveButton.clicked.connect(self.delTracks)
        self.playButton.clicked.connect(self.player.playPause)
        self.playlistButton.clicked.connect(self.showHidePlaylist)
        self.playlistView.doubleClicked.connect(self.changeTrack)
        self.queueNextButton.clicked.connect(self.player.queueList.next)
        self.queuePrevButton.clicked.connect(self.player.queueList.previous)
        self.repeatButton.clicked.connect(self.player.setRepeatMode)
        self.savePlButton.clicked.connect(self.player.savePlaylist)
        self.suffleButton.clicked.connect(self.player.switchRandomMode)
        self.timeSlider.valueChanged.connect(self.player.setPosition)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        # Menu
        self.menu = QtWidgets.QMenu()
        self.menuAddFiles = QtWidgets.QAction(
            QIcon.fromTheme('list-add'),
            _translate('MainWindow', 'Add file(s)'),
            self.menu
        )
        self.menuAddFiles.triggered.connect(self.addFiles)
        self.menu.addAction(self.menuAddFiles)

        self.menuAddFolder = QtWidgets.QAction(
            QIcon.fromTheme('folder-add'),
            _translate('MainWindow', 'Add folder'),
            self.menu
        )
        self.menuAddFolder.triggered.connect(self.addDir)
        self.menu.addAction(self.menuAddFolder)

        self.menuAddUrl = QtWidgets.QAction(
            QIcon.fromTheme('view-links'),
            _translate('MainWindow', 'Add URL'),
            self.menu
        )
        self.menuAddUrl.triggered.connect(self.addUrl)
        self.menu.addAction(self.menuAddUrl)

        self.menuAddPL = QtWidgets.QAction(
            QIcon.fromTheme('document-import'),
            _translate('MainWindow', 'Open playlist'),
            self.menu
        )
        self.menuAddPL.triggered.connect(self.player.openPlaylist)
        self.menu.addAction(self.menuAddPL)

        self.menuConfig = QtWidgets.QAction(
            QIcon.fromTheme('configure'),
            _translate('MainWindow', 'Configure'),
            self.menu
        )
        self.menuConfig.triggered.connect(self.openConfig)
        self.menu.addAction(self.menuConfig)

        self.menuButton.setMenu(self.menu)

        # Volume
        icon = QIcon.fromTheme("audio-volume-high")
        self.iconVol.setPixmap(icon.pixmap(16, 16))
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setValue(self.player.volume)

        # Tray icon
        self.tray = QtWidgets.QSystemTrayIcon(
            QIcon(QPixmap(':/icon.svg')),
            self
        )

        # Tray menu
        trayMenu = QtWidgets.QMenu()
        self.trayPlay = QtWidgets.QAction(
            QIcon.fromTheme('media-playback-start'),
            _translate('MainWindow', 'Play/Pause'),
            trayMenu
        )
        self.trayPlay.triggered.connect(self.player.playPause)
        trayMenu.addAction(self.trayPlay)

        prevAction = QtWidgets.QAction(
            QIcon.fromTheme('media-skip-backward'),
            _translate('MainWindow', 'Previous track'),
            trayMenu
        )
        prevAction.triggered.connect(self.player.queueList.previous)
        trayMenu.addAction(prevAction)

        nextAction = QtWidgets.QAction(
            QIcon.fromTheme('media-skip-forward'),
            _translate('MainWindow', 'Next track'),
            trayMenu
        )
        nextAction.triggered.connect(self.player.queueList.next)
        trayMenu.addAction(nextAction)

        trayMenuAddFiles = QtWidgets.QAction(
            QIcon.fromTheme('list-add'),
            _translate('MainWindow', 'Add file(s)'),
            trayMenu
        )
        trayMenuAddFiles.triggered.connect(self.addFiles)
        trayMenu.addAction(trayMenuAddFiles)

        trayMenuAddFolder = QtWidgets.QAction(
            QIcon.fromTheme('folder-add'),
            _translate('MainWindow', 'Add folder'),
            trayMenu
        )
        trayMenuAddFolder.triggered.connect(self.addDir)
        trayMenu.addAction(trayMenuAddFolder)

        trayMenuAddUrl = QtWidgets.QAction(
            QIcon.fromTheme('view-links'),
            _translate('MainWindow', 'Add URL'),
            trayMenu
        )
        trayMenuAddUrl.triggered.connect(self.addUrl)
        trayMenu.addAction(trayMenuAddUrl)

        trayMenuAddPL = QtWidgets.QAction(
            QIcon.fromTheme('document-import'),
            _translate('MainWindow', 'Open playlist'),
            trayMenu
        )
        trayMenuAddPL.triggered.connect(self.player.openPlaylist)
        trayMenu.addAction(trayMenuAddPL)

        trayMenuConfig = QtWidgets.QAction(
            QIcon.fromTheme('configure'),
            _translate('MainWindow', 'Configure'),
            trayMenu
        )
        trayMenuConfig.triggered.connect(self.openConfig)
        trayMenu.addAction(trayMenuConfig)

        closeAction = QtWidgets.QAction(
            QIcon.fromTheme('application-exit'),
            _translate('MainWindow', 'Quit'),
            trayMenu
        )
        closeAction.triggered.connect(self.closeEvent)
        trayMenu.addAction(closeAction)

        self.tray.setContextMenu(trayMenu)
        self.tray.setToolTip('PQMusic')

        self.tray.setVisible(True)
        self.tray.activated.connect(self.hideShowMW)

    def addDir(self):
        """ Opens the dialog to select a folder to add the supported files inside it,
            as well as subdirectories.
        """
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            _translate('MainWindow', 'Select folder'),
            self.config['musicfolder'],
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if folder:
            startPlay = (self.player.queueList.mediaCount() == 0)
            self.scanDir(folder)
            if startPlay:
                self.player.startPlay()

    def addFiles(self):
        """ Opens the dialog to select files to add """
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            _translate('MainWindow', 'Select file to open'),
            self.config['musicfolder'],
            _translate(
                'MainWindow',
                'Audio (*.mp3 *.ogg *.opus *.aac *.m4a *.flac *.wav)'
            ),
        )

        startPlay = (self.player.queueList.mediaCount() == 0)
        if files:
            for file in files:
                self.player.addFile(file)

            if startPlay:
                self.player.startPlay()

    def addFilesFromArgs(self, files):
        """ Add files from command lines arguments and drag and drop

        Args:
            files (array): A array of files and/or folders
        """
        if files and len(files) > 0:
            startPlay = (self.player.queueList.mediaCount() == 0)
            for file in sorted(files):
                file = path.join(getcwd(), file)
                if path.isfile(file):
                    ext = Path(file).suffix
                    if ext.startswith('.m3u'):
                        self.player.openPlaylist(file)
                    else:
                        self.player.addFile(file)
                elif path.isdir(file):
                    self.scanDir(file)

            if startPlay:
                self.player.startPlay()

    def addUrl(self):
        """ Displays the dialog for adding URLs """
        self.addUrlDialog = open_url_dialog.addDialog(self, self.appendUrl)
        self.addUrlDialog.exec_()

    def appendUrl(self, url, mimetype):
        """ This is a callback function.
            It is called each time a URL is added.
            Args:
                url : str
                    The URL to add
                mimetype : dtr
                    The mimetype of the URL
        """
        startPlay = (self.player.queueList.mediaCount() == 0)
        self.player.addUrl(url, mimetype)
        if startPlay:
            self.player.startPlay()

    def changeTrack(self, w):
        """ This function is called when double clicking
            on the playlist to switch to that track.
            Args:
                w : QStandarItem
                    The QStandarItem selected
        """
        row = w.row()
        self.player.changePos(row)

    def clearMetadata(self):
        """ It shows again the initial texts (cover, title, artist and album),
            as well as locking again several of the buttons.
            It is called every time you click on the button to clear
            the playlist, or to delete the selected ones and it becomes empty.
        """
        self.titleLabel.setText(
            _translate('MainWindow', 'Track Title')
        )
        self.artistLabel.setText(
            _translate('MainWindow', 'Artist')
        )
        self.albumLabel.setText(
            _translate('MainWindow', 'Album')
        )

        cover = QPixmap(':/no_cover.svg')
        self.labelCover.setPixmap(
            cover.scaled(QSize(128, 128), Qt.KeepAspectRatio)
        )

        self.setWindowTitle('PQMusic')
        self.tray.setToolTip('PQMusic')

        self.queuePrevButton.setEnabled(False)
        self.queueNextButton.setEnabled(False)
        self.playButton.setEnabled(False)
        self.repeatButton.setEnabled(False)
        self.suffleButton.setEnabled(False)
        self.timeSlider.setEnabled(False)

    def clearPlaylist(self):
        """ Clear the playlist """
        model = self.playlistView.model()
        model.removeRows(0, model.rowCount())
        self.player.stop()
        self.player.queueList.clear()
        self.clearMetadata()

    def closeEvent(self, event):
        """ This function is called when closing the main window
            or selecting Exit from the icon menu on the system tray.

        Args:
            event (QEvent): The event
        """
        if event and self.config['mintosystray']:
            self.hide()
            self.isMWShow = False
            event.ignore()
        else:
            delLockFile()
            sysExit()

    def delTracks(self):
        """ Remove the selected tracks in the playlist """
        model = self.playlistView.selectionModel()
        indexes = model.selectedIndexes()
        indexes.sort(reverse=True)
        items = [
            self.playlistView.model().itemFromIndex(index) for index in indexes
        ]

        for item in items:
            pos = item.row()
            self.playlistView.model().removeRow(pos)
            self.player.delete(pos)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """ This function is called when dragging files
            and/or folders to the window to add them.

        Args:
            event (QEvent): The event
        """
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if len(files) > 0:
            self.addFilesFromArgs(files)

    def hideShowMW(self):
        """ Show/Hide the main window """
        if self.isMWShow:
            self.hide()
            self.isMWShow = False
        else:
            self.show()
            self.isMWShow = True

    def openConfig(self):
        configDialog = ConfigDialog(self)
        configDialog.open()

    def scanDir(self, folder):
        """ Scan the specified folder and its subfolders for supported files
            Args:
                folder : str
                    The path to the folder to scan
        """
        for f in sorted(listdir(folder)):
            file = path.join(folder, f)
            if path.isdir(file):
                self.scanDir(file)
            elif path.isfile(file):
                self.player.addFile(file)

    def resizeEvent(self, event):
        """ This function is called when resize the window.
            Args:
                event : The resize event
                    The QStandarItem selected
        """
        if self.resize_event:
            if event.size().height() >= 320:
                self.playListFrame.show()
                self.playlistButton.setChecked(True)

            else:
                self.playListFrame.hide()
                self.playlistButton.setChecked(False)

    def showHidePlaylist(self):
        """ Show/Hide the playlist frame """
        self.resize_event = False

        if self.playlistButton.isChecked():
            self.playListFrame.show()
        else:
            self.playListFrame.hide()

        QTimer.singleShot(0, self.adjustSize)
        self.resize_event = True


def init(custom_theme=True, files=[]):
    LOCAL_DIR = path.dirname(path.realpath(__file__))

    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    defaultLocale = QLocale.system().name()
    if defaultLocale.startswith('es_'):
        defaultLocale = 'es'

    translator = QTranslator()
    translator.load(LOCAL_DIR + "/locales/" + defaultLocale + ".qm")
    app.installTranslator(translator)

    if custom_theme:
        QFontDatabase.addApplicationFont('OpenSans.ttf')

        with open(LOCAL_DIR + '/style.qss', 'r', encoding='utf8') as fh:
            app.setStyleSheet(fh.read())

        searchPaths = QIcon.fallbackSearchPaths()
        searchPaths.append(':/icons')
        QIcon.setFallbackSearchPaths(searchPaths)
        QIcon.setThemeName('luv')

    window = MainWindow()
    window.addFilesFromArgs(files)
    window.retranslateUi(window)
    window.show()
    app.exec_()
