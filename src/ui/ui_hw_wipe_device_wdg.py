# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file ui_hw_wipe_device_wdg.ui
#
# Created by: PyQt5 UI code generator
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WdgWipeHwDevice(object):
    def setupUi(self, WdgWipeHwDevice):
        WdgWipeHwDevice.setObjectName("WdgWipeHwDevice")
        WdgWipeHwDevice.resize(505, 357)
        self.verticalLayout = QtWidgets.QVBoxLayout(WdgWipeHwDevice)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblMessage = QtWidgets.QLabel(WdgWipeHwDevice)
        self.lblMessage.setMinimumSize(QtCore.QSize(0, 0))
        self.lblMessage.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lblMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lblMessage.setObjectName("lblMessage")
        self.verticalLayout.addWidget(self.lblMessage)

        self.retranslateUi(WdgWipeHwDevice)
        QtCore.QMetaObject.connectSlotsByName(WdgWipeHwDevice)

    def retranslateUi(self, WdgWipeHwDevice):
        _translate = QtCore.QCoreApplication.translate
        WdgWipeHwDevice.setWindowTitle(_translate("WdgWipeHwDevice", "Form"))
        self.lblMessage.setText(_translate("WdgWipeHwDevice", "..."))