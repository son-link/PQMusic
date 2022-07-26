from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .ui import Ui_config
from os import environ, path
import configparser

_translate = QCoreApplication.translate
configfile = environ['HOME']+'/.pqmusic'


class ConfigDialog(QtWidgets.QDialog):
    """Show Add poscast dialog"""

    def __init__(self, parent=None, callback=None):
        """ Init the class addDialog
            Parameters
            ----------
            parent : object, optional
                The MainWindow object (default is None)
            callback : function, optional
                The callback function that will be called when the thread
                adding the podcast is started.  (default is False)
        """
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_config.Ui_Config_Dialog()
        self.ui.setupUi(self)
        self.callback = callback
        self.addThread = None

        self.setWindowFlags(
            Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowTitleHint
        )

        self.ui.setMusicFolderBtn.clicked.connect(self.__selFolder)
        self.ui.buttonBox.accepted.connect(self.save)
        self.ui.buttonBox.rejected.connect(self.close)

    def open(self):
        self.config = self.loadConf()
        self.ui.musicFolderEdit.setText(self.config['musicfolder'])

        self.ui.notifyOnChange.setChecked(False)
        if self.config['shownotify'] == 1:
            self.ui.notifyOnChange.setChecked(True)

        self.ui.minimizeToTray.setChecked(False)
        if self.config['mintosystray'] == 1:
            self.ui.minimizeToTray.setChecked(True)

        self.ui.cbDownCover.setChecked(False)
        if 'sdowncover' in self.config and self.config['downcover'] == 1:
            self.ui.cbDownCover.setChecked(True)

        self.ui.cbSaveVolume.setChecked(False)
        if 'savevolume' in self.config and self.config['savevolume'] == 1:
            self.ui.cbSaveVolume.setChecked(True)
            
        self.ui.cbSaveVolume.setChecked(False)
        if 'saveplaylist' in self.config and self.config['saveplaylist'] == 1:
            self.ui.cbSavePlaylist.setChecked(True)

        self.exec_()

    @staticmethod
    def loadConf():
        if not path.isfile(configfile):
            f = open(configfile, 'w')
            f.write(
                "[pqmusic]\nmusicfolder={}\nshownotify=0\nmintosystray=0\ndowncover=0\nsavevolume=0\nsaveplaylist=0"
                .format(environ['HOME'])
            )
            f.close()

        cfg = configparser.ConfigParser()
        cfg.read([configfile])
        config = {}

        try:
            config['musicfolder'] = cfg.get('pqmusic', 'musicfolder')
            config['shownotify'] = int(cfg.get('pqmusic', 'shownotify'))
            config['mintosystray'] = int(cfg.get('pqmusic', 'mintosystray'))
            config['downcover'] = int(cfg.get('pqmusic', 'downcover'))
            config['savevolume'] = int(cfg.get('pqmusic', 'savevolume'))
            config['saveplaylist'] = int(cfg.get('pqmusic', 'saveplaylist'))

        except configparser.NoOptionError:
            print('Error')

        return config

    def save(self):
        cfg = configparser.ConfigParser()
        cfg.read([configfile])

        cfg.set('pqmusic', 'musicfolder', self.ui.musicFolderEdit.text())

        if self.ui.notifyOnChange.isChecked():
            cfg.set('pqmusic', 'shownotify', '1')
        else:
            cfg.set('pqmusic', 'shownotify', '0')

        if self.ui.minimizeToTray.isChecked():
            cfg.set('pqmusic', 'mintosystray', '1')
        else:
            cfg.set('pqmusic', 'mintosystray', '0')

        if self.ui.cbDownCover.isChecked():
            cfg.set('pqmusic', 'downcover', '1')
        else:
            cfg.set('pqmusic', 'downcover', '0')

        if self.ui.cbSaveVolume.isChecked():
            cfg.set('pqmusic', 'savevolume', '1')
        else:
            cfg.set('pqmusic', 'savevolume', '0')
            
        if self.ui.cbSavePlaylist.isChecked():
            cfg.set('pqmusic', 'saveplaylist', '1')
        else:
            cfg.set('pqmusic', 'saveplaylist', '0')

        with open(configfile, "w") as file:
            cfg.write(file)
            file.close()

        self.parent.config = self.loadConf()
        self.close()

    def __selFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            _translate('Config_Dialog', 'Select music folder'),
            self.config['musicfolder'],
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if folder:
            self.ui.musicFolderEdit.setText(folder)
