# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/blogin/Documents/Projects/dash-masternode-tool/src/ui/ui_wdg_wallet_txes_filter.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WdgWalletTxesFilter(object):
    def setupUi(self, WdgWalletTxesFilter):
        WdgWalletTxesFilter.setObjectName("WdgWalletTxesFilter")
        WdgWalletTxesFilter.resize(637, 201)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WdgWalletTxesFilter.sizePolicy().hasHeightForWidth())
        WdgWalletTxesFilter.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(WdgWalletTxesFilter)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(WdgWalletTxesFilter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chbTypeIncoming = QtWidgets.QCheckBox(self.groupBox)
        self.chbTypeIncoming.setObjectName("chbTypeIncoming")
        self.horizontalLayout_2.addWidget(self.chbTypeIncoming)
        self.chbTypeCoinbase = QtWidgets.QCheckBox(self.groupBox)
        self.chbTypeCoinbase.setObjectName("chbTypeCoinbase")
        self.horizontalLayout_2.addWidget(self.chbTypeCoinbase)
        self.chbTypeOutgoing = QtWidgets.QCheckBox(self.groupBox)
        self.chbTypeOutgoing.setObjectName("chbTypeOutgoing")
        self.horizontalLayout_2.addWidget(self.chbTypeOutgoing)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.edtRecipientAddress = QtWidgets.QLineEdit(self.frame)
        self.edtRecipientAddress.setClearButtonEnabled(True)
        self.edtRecipientAddress.setObjectName("edtRecipientAddress")
        self.horizontalLayout_5.addWidget(self.edtRecipientAddress)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.edtSenderAddress = QtWidgets.QLineEdit(self.frame)
        self.edtSenderAddress.setClearButtonEnabled(True)
        self.edtSenderAddress.setObjectName("edtSenderAddress")
        self.horizontalLayout_5.addWidget(self.edtSenderAddress)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.cboAmountOper = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboAmountOper.sizePolicy().hasHeightForWidth())
        self.cboAmountOper.setSizePolicy(sizePolicy)
        self.cboAmountOper.setObjectName("cboAmountOper")
        self.cboAmountOper.addItem("")
        self.cboAmountOper.setItemText(0, "")
        self.cboAmountOper.addItem("")
        self.cboAmountOper.addItem("")
        self.cboAmountOper.addItem("")
        self.horizontalLayout_6.addWidget(self.cboAmountOper)
        self.edtAmountValue = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAmountValue.sizePolicy().hasHeightForWidth())
        self.edtAmountValue.setSizePolicy(sizePolicy)
        self.edtAmountValue.setClearButtonEnabled(True)
        self.edtAmountValue.setObjectName("edtAmountValue")
        self.horizontalLayout_6.addWidget(self.edtAmountValue)
        self.label_5 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.cboDateOper = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cboDateOper.sizePolicy().hasHeightForWidth())
        self.cboDateOper.setSizePolicy(sizePolicy)
        self.cboDateOper.setObjectName("cboDateOper")
        self.cboDateOper.addItem("")
        self.cboDateOper.setItemText(0, "")
        self.cboDateOper.addItem("")
        self.cboDateOper.addItem("")
        self.cboDateOper.addItem("")
        self.horizontalLayout_6.addWidget(self.cboDateOper)
        self.edtDate = QtWidgets.QDateEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setCalendarPopup(True)
        self.edtDate.setObjectName("edtDate")
        self.horizontalLayout_6.addWidget(self.edtDate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.rbFilterTypeOr = QtWidgets.QRadioButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbFilterTypeOr.sizePolicy().hasHeightForWidth())
        self.rbFilterTypeOr.setSizePolicy(sizePolicy)
        self.rbFilterTypeOr.setChecked(True)
        self.rbFilterTypeOr.setObjectName("rbFilterTypeOr")
        self.horizontalLayout_8.addWidget(self.rbFilterTypeOr)
        self.rbFilterTypeAnd = QtWidgets.QRadioButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbFilterTypeAnd.sizePolicy().hasHeightForWidth())
        self.rbFilterTypeAnd.setSizePolicy(sizePolicy)
        self.rbFilterTypeAnd.setObjectName("rbFilterTypeAnd")
        self.horizontalLayout_8.addWidget(self.rbFilterTypeAnd)
        self.horizontalLayout_7.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.btnApply = QtWidgets.QToolButton(self.frame)
        self.btnApply.setObjectName("btnApply")
        self.horizontalLayout_9.addWidget(self.btnApply)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(WdgWalletTxesFilter)
        QtCore.QMetaObject.connectSlotsByName(WdgWalletTxesFilter)

    def retranslateUi(self, WdgWalletTxesFilter):
        _translate = QtCore.QCoreApplication.translate
        WdgWalletTxesFilter.setWindowTitle(_translate("WdgWalletTxesFilter", "Form"))
        self.label.setText(_translate("WdgWalletTxesFilter", "Type:"))
        self.chbTypeIncoming.setText(_translate("WdgWalletTxesFilter", "Incoming"))
        self.chbTypeCoinbase.setText(_translate("WdgWalletTxesFilter", "Incoming (new coins)"))
        self.chbTypeOutgoing.setText(_translate("WdgWalletTxesFilter", "Outgoing"))
        self.label_2.setText(_translate("WdgWalletTxesFilter", "Recipient:"))
        self.label_3.setText(_translate("WdgWalletTxesFilter", "Sender:"))
        self.label_4.setText(_translate("WdgWalletTxesFilter", "Amount:"))
        self.cboAmountOper.setItemText(1, _translate("WdgWalletTxesFilter", ">="))
        self.cboAmountOper.setItemText(2, _translate("WdgWalletTxesFilter", "<="))
        self.cboAmountOper.setItemText(3, _translate("WdgWalletTxesFilter", "="))
        self.label_5.setText(_translate("WdgWalletTxesFilter", "Date:"))
        self.cboDateOper.setItemText(1, _translate("WdgWalletTxesFilter", ">="))
        self.cboDateOper.setItemText(2, _translate("WdgWalletTxesFilter", "<="))
        self.cboDateOper.setItemText(3, _translate("WdgWalletTxesFilter", "="))
        self.rbFilterTypeOr.setText(_translate("WdgWalletTxesFilter", "Any condition is met (OR)"))
        self.rbFilterTypeAnd.setText(_translate("WdgWalletTxesFilter", "All conditions are met (AND)"))
        self.btnApply.setText(_translate("WdgWalletTxesFilter", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WdgWalletTxesFilter = QtWidgets.QWidget()
    ui = Ui_WdgWalletTxesFilter()
    ui.setupUi(WdgWalletTxesFilter)
    WdgWalletTxesFilter.show()
    sys.exit(app.exec_())
