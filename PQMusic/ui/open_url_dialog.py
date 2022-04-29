from PyQt5 import QtWidgets
from PyQt5.QtCore import (
    pyqtSignal,
    QThread,
    Qt
)
from . import Ui_add_url_dialog
import requests


class addUrlThread(QThread):
    """Thread for add a url to the playlist"""
    stream = pyqtSignal(str, str)

    def __init__(self, parent, url=None, data=None):
        """ Init addPodcasts class and thread
            Parameters
            ----------
            parent : object
                The MainWindow object (default is None)
            url : string
                Url to the audio stream
        """
        super(addUrlThread, self).__init__(parent)
        self.url = url

    def run(self):
        resp = requests.head(self.url, allow_redirects=True)

        if (
            resp.status_code == 200 and
            resp.headers['Content-Type'].startswith('audio')
        ):
            self.stream.emit(self.url, resp.headers['Content-Type'])

    def stop(self):
        self.quit()
        self.wait()


class addDialog(QtWidgets.QDialog):
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
        self.ui = Ui_add_url_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.callback = callback
        self.addThread = None

        self.setWindowFlags(
            Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowTitleHint
        )

        self.ui.buttonBox.accepted.connect(self.ok_callback)

    def ok_callback(self):
        text = self.ui.urlsTextEdit.toPlainText()
        if text:
            for url in text.splitlines():
                self.addThread = addUrlThread(self, url)
                self.addThread.stream.connect(self.callback)
                self.addThread.start()
