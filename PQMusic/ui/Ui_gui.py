# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/son_link/proyectos/PQMusic/PQMusic/ui/gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(435, 420)
        MainWindow.setMinimumSize(QtCore.QSize(435, 0))
        MainWindow.setWindowTitle("PQMusic")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWhatsThis("")
        MainWindow.setStyleSheet("")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.optionsLayout = QtWidgets.QHBoxLayout()
        self.optionsLayout.setObjectName("optionsLayout")
        self.playlistButton = QtWidgets.QPushButton(self.centralwidget)
        self.playlistButton.setText("")
        icon = QtGui.QIcon.fromTheme("view-media-playlist")
        self.playlistButton.setIcon(icon)
        self.playlistButton.setCheckable(True)
        self.playlistButton.setChecked(False)
        self.playlistButton.setFlat(True)
        self.playlistButton.setObjectName("playlistButton")
        self.optionsLayout.addWidget(self.playlistButton)
        self.repeatButton = QtWidgets.QPushButton(self.centralwidget)
        self.repeatButton.setEnabled(False)
        self.repeatButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-playlist-repeat")
        self.repeatButton.setIcon(icon)
        self.repeatButton.setCheckable(True)
        self.repeatButton.setFlat(True)
        self.repeatButton.setObjectName("repeatButton")
        self.optionsLayout.addWidget(self.repeatButton)
        self.suffleButton = QtWidgets.QPushButton(self.centralwidget)
        self.suffleButton.setEnabled(False)
        self.suffleButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-playlist-shuffle")
        self.suffleButton.setIcon(icon)
        self.suffleButton.setCheckable(True)
        self.suffleButton.setFlat(True)
        self.suffleButton.setObjectName("suffleButton")
        self.optionsLayout.addWidget(self.suffleButton)
        self.menuButton = QtWidgets.QToolButton(self.centralwidget)
        self.menuButton.setText("")
        icon = QtGui.QIcon.fromTheme("application-menu")
        self.menuButton.setIcon(icon)
        self.menuButton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.menuButton.setAutoRaise(True)
        self.menuButton.setArrowType(QtCore.Qt.NoArrow)
        self.menuButton.setObjectName("menuButton")
        self.optionsLayout.addWidget(self.menuButton)
        self.iconVol = QtWidgets.QLabel(self.centralwidget)
        self.iconVol.setText("")
        self.iconVol.setObjectName("iconVol")
        self.optionsLayout.addWidget(self.iconVol)
        self.volumeSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.optionsLayout.addWidget(self.volumeSlider)
        self.gridLayout.addLayout(self.optionsLayout, 2, 1, 1, 1)
        self.playerLayout = QtWidgets.QHBoxLayout()
        self.playerLayout.setObjectName("playerLayout")
        self.queuePrevButton = QtWidgets.QPushButton(self.centralwidget)
        self.queuePrevButton.setEnabled(False)
        self.queuePrevButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-skip-backward")
        self.queuePrevButton.setIcon(icon)
        self.queuePrevButton.setIconSize(QtCore.QSize(22, 16))
        self.queuePrevButton.setAutoDefault(False)
        self.queuePrevButton.setDefault(False)
        self.queuePrevButton.setFlat(True)
        self.queuePrevButton.setObjectName("queuePrevButton")
        self.playerLayout.addWidget(self.queuePrevButton)
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setEnabled(False)
        self.playButton.setMinimumSize(QtCore.QSize(0, 0))
        self.playButton.setBaseSize(QtCore.QSize(0, 0))
        self.playButton.setStyleSheet("")
        self.playButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.playButton.setIcon(icon)
        self.playButton.setIconSize(QtCore.QSize(32, 32))
        self.playButton.setFlat(True)
        self.playButton.setObjectName("playButton")
        self.playerLayout.addWidget(self.playButton)
        self.queueNextButton = QtWidgets.QPushButton(self.centralwidget)
        self.queueNextButton.setEnabled(False)
        self.queueNextButton.setText("")
        icon = QtGui.QIcon.fromTheme("media-skip-forward")
        self.queueNextButton.setIcon(icon)
        self.queueNextButton.setFlat(True)
        self.queueNextButton.setObjectName("queueNextButton")
        self.playerLayout.addWidget(self.queueNextButton)
        self.gridLayout.addLayout(self.playerLayout, 2, 0, 1, 1)
        self.labelCover = QtWidgets.QLabel(self.centralwidget)
        self.labelCover.setMinimumSize(QtCore.QSize(0, 128))
        self.labelCover.setMaximumSize(QtCore.QSize(128, 128))
        self.labelCover.setText("")
        self.labelCover.setPixmap(QtGui.QPixmap(":/icon.svg"))
        self.labelCover.setScaledContents(True)
        self.labelCover.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCover.setObjectName("labelCover")
        self.gridLayout.addWidget(self.labelCover, 0, 0, 1, 1)
        self.infoWidget = QtWidgets.QWidget(self.centralwidget)
        self.infoWidget.setMaximumSize(QtCore.QSize(340, 16777215))
        self.infoWidget.setObjectName("infoWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.infoWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.titleLabel = QtWidgets.QLabel(self.infoWidget)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout_2.addWidget(self.titleLabel)
        self.artistLabel = QtWidgets.QLabel(self.infoWidget)
        self.artistLabel.setObjectName("artistLabel")
        self.verticalLayout_2.addWidget(self.artistLabel)
        self.albumLabel = QtWidgets.QLabel(self.infoWidget)
        self.albumLabel.setObjectName("albumLabel")
        self.verticalLayout_2.addWidget(self.albumLabel)
        self.timeLayout = QtWidgets.QHBoxLayout()
        self.timeLayout.setContentsMargins(0, -1, 0, -1)
        self.timeLayout.setSpacing(2)
        self.timeLayout.setObjectName("timeLayout")
        self.timeLabel = QtWidgets.QLabel(self.infoWidget)
        self.timeLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.timeLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.timeLabel.setSizeIncrement(QtCore.QSize(50, 0))
        self.timeLabel.setBaseSize(QtCore.QSize(0, 0))
        self.timeLabel.setStyleSheet("QLabel {\n"
"    width: 200px\n"
"}")
        self.timeLabel.setText("0:00:00")
        self.timeLabel.setObjectName("timeLabel")
        self.timeLayout.addWidget(self.timeLabel)
        self.timeSlider = QtWidgets.QSlider(self.infoWidget)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.timeLayout.addWidget(self.timeSlider)
        self.totalTimeLabel = QtWidgets.QLabel(self.infoWidget)
        self.totalTimeLabel.setText("0:00:00")
        self.totalTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.timeLayout.addWidget(self.totalTimeLabel)
        self.verticalLayout_2.addLayout(self.timeLayout)
        self.gridLayout.addWidget(self.infoWidget, 0, 1, 1, 1)
        self.playListFrame = QtWidgets.QFrame(self.centralwidget)
        self.playListFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.playListFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.playListFrame.setObjectName("playListFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.playListFrame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.playlistView = QtWidgets.QListView(self.playListFrame)
        self.playlistView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.playlistView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.playlistView.setObjectName("playlistView")
        self.verticalLayout.addWidget(self.playlistView)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.playlistBtnLayout = QtWidgets.QHBoxLayout()
        self.playlistBtnLayout.setObjectName("playlistBtnLayout")
        self.listRemoveButton = QtWidgets.QPushButton(self.playListFrame)
        self.listRemoveButton.setText("")
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.listRemoveButton.setIcon(icon)
        self.listRemoveButton.setFlat(True)
        self.listRemoveButton.setObjectName("listRemoveButton")
        self.playlistBtnLayout.addWidget(self.listRemoveButton)
        self.listClearButton = QtWidgets.QPushButton(self.playListFrame)
        self.listClearButton.setText("")
        icon = QtGui.QIcon.fromTheme("edit-clear-all")
        self.listClearButton.setIcon(icon)
        self.listClearButton.setFlat(True)
        self.listClearButton.setObjectName("listClearButton")
        self.playlistBtnLayout.addWidget(self.listClearButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.playlistBtnLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.playlistBtnLayout, 1, 0, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout.addWidget(self.playListFrame, 3, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.titleLabel.setText(_translate("MainWindow", "Track Title"))
        self.artistLabel.setText(_translate("MainWindow", "Artist"))
        self.albumLabel.setText(_translate("MainWindow", "Album"))
from . import images_rc
