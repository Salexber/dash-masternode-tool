#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Bertrand256
# Created on: 2017-12
import logging
from typing import Optional

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, QVariant, Qt, QPoint, QItemSelection, QItemSelectionModel, \
    QEventLoop
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QMenu, QApplication, QLineEdit, QShortcut, QMessageBox, QTableWidgetItem
import app_cache
import app_defs
import hw_intf
from app_config import AppConfig
from hw_settings_wdg import WdgHwSettings
from recover_hw_wdg import WdgRecoverHw
from select_hw_device_wdg import SelectHwDeviceWdg
from ui import ui_wallet_tools_dlg
from wallet_tools_common import ActionPageBase
from hw_intf import HWDevices
from wnd_utils import WndUtils

ACTION_NONE = 0
ACTION_HW_SETTINGS = 1
ACTION_RECOVER_HW = 2
ACTION_INITIALIZE_HW = 3
ACTION_WIPE_HW = 4
ACTION_UPDATE_HW_FIRMWARE = 5
ACTION_SPLIT_MERGE_SEED = 6

log = logging.getLogger('dmt.wallet_tools_dlg')


class WalletToolsDlg(QDialog, ui_wallet_tools_dlg.Ui_WalletToolsDlg, WndUtils):
    def __init__(self, parent) -> None:
        QDialog.__init__(self, parent)
        ui_wallet_tools_dlg.Ui_WalletToolsDlg.__init__(self)
        WndUtils.__init__(self, parent.app_config)
        self.main_ui = parent
        self.app_config: AppConfig = parent.app_config
        self.current_action = ACTION_NONE
        self.action_widget: Optional[ActionPageBase] = None
        self.action_layout: Optional[QtWidgets.QVBoxLayout] = None
        self.hw_devices = HWDevices(self.main_ui, self.app_config.hw_type)
        self.wdg_select_hw_device = SelectHwDeviceWdg(self, self.hw_devices)
        self.setupUi(self)

    def setupUi(self, dlg):
        ui_wallet_tools_dlg.Ui_WalletToolsDlg.setupUi(self, self)
        self.setWindowTitle("Wallet tools")
        self.activate_menu_page()

        lay = self.layout()
        lay.insertWidget(1, self.wdg_select_hw_device)  # hardware wallet selection panel is inserted just below the
                                                     # main title

        self.action_layout = QtWidgets.QVBoxLayout(self.tabActionContainer)
        self.action_layout.setContentsMargins(0, 0, 0, 0)
        self.action_layout.setSpacing(3)
        self.action_layout.setObjectName("action_layout")

    @pyqtSlot(bool)
    def on_btnCancel_clicked(self):
        try:
            if self.action_widget:
                if self.action_widget.on_btn_cancel_clicked() is False:
                    # the action widget decided not to close
                    return
            self.close()
        except Exception as e:
            self.errorMsg(str(e), True)

    @pyqtSlot(bool)
    def on_btnBack_clicked(self):
        try:
            if self.action_widget:
                self.action_widget.on_btn_back_clicked()
        except Exception as e:
            self.errorMsg(str(e), True)

    @pyqtSlot(bool)
    def on_btnContinue_clicked(self):
        try:
            if self.action_widget:
                self.action_widget.on_btn_continue_clicked()
        except Exception as e:
            self.errorMsg(str(e), True)

    @pyqtSlot(bool)
    def on_actHwSettings_clicked(self):
        try:
            self.setup_action_widget(ACTION_HW_SETTINGS)
        except Exception as e:
            self.errorMsg(str(e), True)

    @pyqtSlot(bool)
    def on_actRecoverHw_clicked(self):
        try:
            self.setup_action_widget(ACTION_RECOVER_HW)
        except Exception as e:
            self.errorMsg(str(e), True)

    def activate_menu_page(self):
        self.tabsMain.setCurrentIndex(0)
        self.lblTitle.setText('<a>Choose action</a>')
        self.btnCancel.setText('Close')
        self.btnCancel.setVisible(True)
        self.btnCancel.setEnabled(True)
        self.btnBack.setText('Back')
        self.btnBack.setVisible(False)
        self.btnBack.setEnabled(True)
        self.btnContinue.setText('Continue')
        self.btnContinue.setVisible(False)
        self.btnContinue.setEnabled(True)
        self.wdg_select_hw_device.setVisible(False)
        self.current_action = ACTION_NONE

    def set_action_title(self, title: str):
        self.lblTitle.setText(title)

    def set_btn_cancel_visible(self, visible: bool):
        self.btnCancel.setVisible(visible)

    def set_btn_cancel_enabled(self, enabled: bool):
        self.btnCancel.setVisible(enabled)

    def set_btn_cancel_text(self, label: str, tool_tip: Optional[str]):
        self.btnCancel.setText(label)
        if tool_tip:
            self.btnCancel.setToolTip(tool_tip)

    def set_btn_back_visible(self, visible: bool):
        self.btnBack.setVisible(visible)

    def set_btn_back_enabled(self, enabled: bool):
        self.btnBack.setVisible(enabled)

    def set_btn_back_text(self, label: str, tool_tip: Optional[str]):
        self.btnBack.setText(label)
        if tool_tip:
            self.btnBack.setToolTip(tool_tip)

    def set_btn_continue_visible(self, visible: bool):
        self.btnContinue.setVisible(visible)

    def set_btn_continue_enabled(self, enabled: bool):
        self.btnContinue.setVisible(enabled)

    def set_btn_continue_text(self, label: str, tool_tip: Optional[str]):
        self.btnContinue.setText(label)
        if tool_tip:
            self.btnContinue.setToolTip(tool_tip)

    def set_hw_panel_visible(self, visible: bool):
        if visible:
            self.wdg_select_hw_device.update()

        self.wdg_select_hw_device.setVisible(visible)

    def get_widget_action_type(self) -> int:
        # returns one of action type constants based on the widget class type in self.action_widget
        if self.action_widget:
            if isinstance(self.action_widget, WdgHwSettings):
                return ACTION_HW_SETTINGS
            elif isinstance(self.action_widget, WdgRecoverHw):
                return ACTION_RECOVER_HW
            else:
                raise Exception('Internal error: not supported type of the action widget')
        else:
            return ACTION_NONE

    def setup_action_widget(self, action: int):
        try:
            if self.get_widget_action_type() != action:
                if self.action_widget is not None:
                    self.action_layout.removeWidget(self.action_widget)
                    del self.action_widget
                    self.action_widget = None

                if action == ACTION_HW_SETTINGS:
                    self.action_widget = WdgHwSettings(self.tabActionContainer, self.hw_devices)
                    self.action_layout.addWidget(self.action_widget)
                elif action == ACTION_RECOVER_HW:
                    self.action_widget = WdgRecoverHw(self.tabActionContainer)
                    self.action_layout.addWidget(self.action_widget)
                else:
                    raise Exception('Internal error: not supported action type')

                self.action_widget.set_control_functions(
                    fn_exit_page=self.activate_menu_page,
                    fn_set_action_title=self.set_action_title,
                    fn_set_btn_cancel_visible=self.set_btn_cancel_visible,
                    fn_set_btn_cancel_enabled=self.set_btn_cancel_enabled,
                    fn_set_btn_cancel_text=self.set_btn_cancel_text,
                    fn_set_btn_back_visible=self.set_btn_back_visible,
                    fn_set_btn_back_enabled=self.set_btn_back_enabled,
                    fn_set_btn_back_text=self.set_btn_back_text,
                    fn_set_btn_continue_visible=self.set_btn_continue_visible,
                    fn_set_btn_continue_enabled=self.set_btn_continue_enabled,
                    fn_set_btn_continue_text=self.set_btn_continue_text,
                    fn_set_hw_panel_visible=self.set_hw_panel_visible
                )

            self.current_action = action
            self.tabsMain.setCurrentIndex(1)
            self.action_widget.initialize()

        except Exception as e:
            self.errorMsg(str(e), True)