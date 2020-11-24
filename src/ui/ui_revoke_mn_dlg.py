# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/blogin/Documents/Projects/dash-masternode-tool/src/ui/ui_revoke_mn_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RevokeMnDlg(object):
    def setupUi(self, RevokeMnDlg):
        RevokeMnDlg.setObjectName("RevokeMnDlg")
        RevokeMnDlg.resize(619, 265)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RevokeMnDlg.sizePolicy().hasHeightForWidth())
        RevokeMnDlg.setSizePolicy(sizePolicy)
        RevokeMnDlg.setStyleSheet("a{text-decoration:none}")
        self.verticalLayout = QtWidgets.QVBoxLayout(RevokeMnDlg)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblDescription = QtWidgets.QLabel(RevokeMnDlg)
        self.lblDescription.setStyleSheet("")
        self.lblDescription.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblDescription.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lblDescription.setWordWrap(True)
        self.lblDescription.setOpenExternalLinks(True)
        self.lblDescription.setObjectName("lblDescription")
        self.verticalLayout.addWidget(self.lblDescription)
        self.line = QtWidgets.QFrame(RevokeMnDlg)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.stackedWidget = QtWidgets.QStackedWidget(RevokeMnDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page0 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page0.sizePolicy().hasHeightForWidth())
        self.page0.setSizePolicy(sizePolicy)
        self.page0.setObjectName("page0")
        self.gridLayout = QtWidgets.QGridLayout(self.page0)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.layReason = QtWidgets.QHBoxLayout()
        self.layReason.setSpacing(8)
        self.layReason.setObjectName("layReason")
        self.cboReason = QtWidgets.QComboBox(self.page0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboReason.sizePolicy().hasHeightForWidth())
        self.cboReason.setSizePolicy(sizePolicy)
        self.cboReason.setObjectName("cboReason")
        self.cboReason.addItem("")
        self.cboReason.addItem("")
        self.cboReason.addItem("")
        self.cboReason.addItem("")
        self.layReason.addWidget(self.cboReason)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layReason.addItem(spacerItem)
        self.gridLayout.addLayout(self.layReason, 1, 1, 1, 1)
        self.lblIP = QtWidgets.QLabel(self.page0)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblIP.setFont(font)
        self.lblIP.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblIP.setObjectName("lblIP")
        self.gridLayout.addWidget(self.lblIP, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.page0)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.line_2 = QtWidgets.QFrame(RevokeMnDlg)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.lblManualCommands = QtWidgets.QLabel(RevokeMnDlg)
        self.lblManualCommands.setStyleSheet("")
        self.lblManualCommands.setText("")
        self.lblManualCommands.setObjectName("lblManualCommands")
        self.verticalLayout.addWidget(self.lblManualCommands)
        self.edtManualCommands = QtWidgets.QTextBrowser(RevokeMnDlg)
        self.edtManualCommands.setOpenExternalLinks(True)
        self.edtManualCommands.setOpenLinks(True)
        self.edtManualCommands.setObjectName("edtManualCommands")
        self.verticalLayout.addWidget(self.edtManualCommands)
        self.frame = QtWidgets.QFrame(RevokeMnDlg)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnCancel = QtWidgets.QPushButton(self.frame)
        self.btnCancel.setAutoDefault(False)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.lblDocumentation = QtWidgets.QLabel(self.frame)
        self.lblDocumentation.setText("")
        self.lblDocumentation.setOpenExternalLinks(True)
        self.lblDocumentation.setObjectName("lblDocumentation")
        self.horizontalLayout.addWidget(self.lblDocumentation)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnSendRevokeTx = QtWidgets.QPushButton(self.frame)
        self.btnSendRevokeTx.setAutoDefault(False)
        self.btnSendRevokeTx.setObjectName("btnSendRevokeTx")
        self.horizontalLayout.addWidget(self.btnSendRevokeTx)
        self.btnClose = QtWidgets.QPushButton(self.frame)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(RevokeMnDlg)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RevokeMnDlg)
        RevokeMnDlg.setTabOrder(self.edtManualCommands, self.btnSendRevokeTx)
        RevokeMnDlg.setTabOrder(self.btnSendRevokeTx, self.btnClose)
        RevokeMnDlg.setTabOrder(self.btnClose, self.btnCancel)

    def retranslateUi(self, RevokeMnDlg):
        _translate = QtCore.QCoreApplication.translate
        RevokeMnDlg.setWindowTitle(_translate("RevokeMnDlg", "Revoke operator"))
        self.lblDescription.setText(_translate("RevokeMnDlg", "The transaction type associated with this action (ProUpRevTx) is used by the operator to terminate service or signal the owner that a new BLS key is required (<a href=\"https://docs.dash.org/en/stable/masternodes/maintenance.html#prouprevtx\">details</a>)."))
        self.cboReason.setItemText(0, _translate("RevokeMnDlg", "0: Not Specified"))
        self.cboReason.setItemText(1, _translate("RevokeMnDlg", "1: Termination of Service"))
        self.cboReason.setItemText(2, _translate("RevokeMnDlg", "2: Compromised Keys"))
        self.cboReason.setItemText(3, _translate("RevokeMnDlg", "3: Change of Keys (Not compromised)"))
        self.lblIP.setText(_translate("RevokeMnDlg", "Revocation reason"))
        self.btnCancel.setText(_translate("RevokeMnDlg", "Cancel"))
        self.btnSendRevokeTx.setText(_translate("RevokeMnDlg", "Send Revoke Transaction"))
        self.btnClose.setText(_translate("RevokeMnDlg", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RevokeMnDlg = QtWidgets.QDialog()
    ui = Ui_RevokeMnDlg()
    ui.setupUi(RevokeMnDlg)
    RevokeMnDlg.show()
    sys.exit(app.exec_())
