# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/blogin/PycharmProjects/DMT-git/src/ui/ui_config_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConfigDlg(object):
    def setupUi(self, ConfigDlg):
        ConfigDlg.setObjectName("ConfigDlg")
        ConfigDlg.setWindowModality(QtCore.Qt.NonModal)
        ConfigDlg.resize(683, 463)
        ConfigDlg.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfigDlg)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(ConfigDlg)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tabDashd = QtWidgets.QWidget()
        self.tabDashd.setObjectName("tabDashd")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabDashd)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(self.tabDashd)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutConnList = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.layoutConnList.setContentsMargins(0, 0, 0, 0)
        self.layoutConnList.setSpacing(2)
        self.layoutConnList.setObjectName("layoutConnList")
        self.frame = QtWidgets.QFrame(self.layoutWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 2)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnNewConn = QtWidgets.QToolButton(self.frame)
        self.btnNewConn.setMinimumSize(QtCore.QSize(16, 16))
        self.btnNewConn.setText("")
        self.btnNewConn.setObjectName("btnNewConn")
        self.horizontalLayout.addWidget(self.btnNewConn)
        self.btnDeleteConn = QtWidgets.QToolButton(self.frame)
        self.btnDeleteConn.setMinimumSize(QtCore.QSize(20, 20))
        self.btnDeleteConn.setText("")
        self.btnDeleteConn.setObjectName("btnDeleteConn")
        self.horizontalLayout.addWidget(self.btnDeleteConn)
        self.btnMoveUpConn = QtWidgets.QToolButton(self.frame)
        self.btnMoveUpConn.setMinimumSize(QtCore.QSize(20, 20))
        self.btnMoveUpConn.setText("")
        self.btnMoveUpConn.setObjectName("btnMoveUpConn")
        self.horizontalLayout.addWidget(self.btnMoveUpConn)
        self.btnMoveDownConn = QtWidgets.QToolButton(self.frame)
        self.btnMoveDownConn.setMinimumSize(QtCore.QSize(20, 20))
        self.btnMoveDownConn.setText("")
        self.btnMoveDownConn.setObjectName("btnMoveDownConn")
        self.horizontalLayout.addWidget(self.btnMoveDownConn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.layoutConnList.addWidget(self.frame)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.layoutConnList.addWidget(self.label)
        self.lstConns = QtWidgets.QListWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstConns.sizePolicy().hasHeightForWidth())
        self.lstConns.setSizePolicy(sizePolicy)
        self.lstConns.setBaseSize(QtCore.QSize(150, 0))
        self.lstConns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lstConns.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lstConns.setObjectName("lstConns")
        self.layoutConnList.addWidget(self.lstConns)
        self.detailsFrame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailsFrame.sizePolicy().hasHeightForWidth())
        self.detailsFrame.setSizePolicy(sizePolicy)
        self.detailsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.detailsFrame.setMidLineWidth(0)
        self.detailsFrame.setObjectName("detailsFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.detailsFrame)
        self.verticalLayout_4.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.splitter)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.chbRandomConn = QtWidgets.QCheckBox(self.tabDashd)
        self.chbRandomConn.setObjectName("chbRandomConn")
        self.verticalLayout_5.addWidget(self.chbRandomConn)
        self.verticalLayout_3.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tabDashd, "")
        self.tabMisc = QtWidgets.QWidget()
        self.tabMisc.setObjectName("tabMisc")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabMisc)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layHardwareWallet = QtWidgets.QHBoxLayout()
        self.layHardwareWallet.setObjectName("layHardwareWallet")
        self.label_3 = QtWidgets.QLabel(self.tabMisc)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.layHardwareWallet.addWidget(self.label_3)
        self.chbHwTrezor = QtWidgets.QRadioButton(self.tabMisc)
        self.chbHwTrezor.setMinimumSize(QtCore.QSize(60, 0))
        self.chbHwTrezor.setMaximumSize(QtCore.QSize(70, 16777215))
        self.chbHwTrezor.setChecked(True)
        self.chbHwTrezor.setObjectName("chbHwTrezor")
        self.layHardwareWallet.addWidget(self.chbHwTrezor)
        self.chbHwKeepKey = QtWidgets.QRadioButton(self.tabMisc)
        self.chbHwKeepKey.setMinimumSize(QtCore.QSize(70, 0))
        self.chbHwKeepKey.setMaximumSize(QtCore.QSize(90, 16777215))
        self.chbHwKeepKey.setObjectName("chbHwKeepKey")
        self.layHardwareWallet.addWidget(self.chbHwKeepKey)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layHardwareWallet.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.layHardwareWallet)
        self.chbCheckForUpdates = QtWidgets.QCheckBox(self.tabMisc)
        self.chbCheckForUpdates.setObjectName("chbCheckForUpdates")
        self.verticalLayout_2.addWidget(self.chbCheckForUpdates)
        self.chbBackupConfigFile = QtWidgets.QCheckBox(self.tabMisc)
        self.chbBackupConfigFile.setObjectName("chbBackupConfigFile")
        self.verticalLayout_2.addWidget(self.chbBackupConfigFile)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabWidget.addTab(self.tabMisc, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.lblStatus = QtWidgets.QLabel(ConfigDlg)
        self.lblStatus.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblStatus.setText("")
        self.lblStatus.setOpenExternalLinks(True)
        self.lblStatus.setObjectName("lblStatus")
        self.verticalLayout.addWidget(self.lblStatus)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfigDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConfigDlg)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(ConfigDlg.accept)
        self.buttonBox.rejected.connect(ConfigDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigDlg)

    def retranslateUi(self, ConfigDlg):
        _translate = QtCore.QCoreApplication.translate
        ConfigDlg.setWindowTitle(_translate("ConfigDlg", "Dialog"))
        self.btnNewConn.setToolTip(_translate("ConfigDlg", "Add New Connection"))
        self.btnDeleteConn.setToolTip(_translate("ConfigDlg", "Delete Current Connection"))
        self.btnMoveUpConn.setToolTip(_translate("ConfigDlg", "Move Up Current Connection"))
        self.btnMoveDownConn.setToolTip(_translate("ConfigDlg", "Move Down Current Connection"))
        self.label.setText(_translate("ConfigDlg", "Connections:"))
        self.chbRandomConn.setToolTip(_translate("ConfigDlg", "Pick random connection to distribute clients\' load over multiple nodes."))
        self.chbRandomConn.setText(_translate("ConfigDlg", "Pick random connection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDashd), _translate("ConfigDlg", "Dash network"))
        self.label_3.setText(_translate("ConfigDlg", "Hardware wallet:"))
        self.chbHwTrezor.setText(_translate("ConfigDlg", "Trezor"))
        self.chbHwKeepKey.setText(_translate("ConfigDlg", "KeepKey"))
        self.chbCheckForUpdates.setText(_translate("ConfigDlg", "Check for updates"))
        self.chbBackupConfigFile.setToolTip(_translate("ConfigDlg", "If checked, old config file will be saved when changing configuration"))
        self.chbBackupConfigFile.setText(_translate("ConfigDlg", "Backup config file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMisc), _translate("ConfigDlg", "Miscellaneous"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigDlg = QtWidgets.QDialog()
    ui = Ui_ConfigDlg()
    ui.setupUi(ConfigDlg)
    ConfigDlg.show()
    sys.exit(app.exec_())

