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

        self.exec_()

    @staticmethod
    def loadConf():
        if not path.isfile(configfile):
            f = open(configfile, 'w')
            f.write(
                "[pqmusic]\nmusicfolder={}\nshownotify=0\nmintosystray=0"
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
