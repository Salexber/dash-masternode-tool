#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Bertrand256
# Created on: 2017-03
import hashlib
from functools import partial
from io import BytesIO
from typing import Optional, Tuple, List, ByteString, Dict, cast
import sys

import trezorlib
import trezorlib.btc
import trezorlib.exceptions
import trezorlib.misc
import keepkeylib.client
import usb1
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QWidget
from trezorlib.tools import Address

import dash_utils
from dash_utils import bip32_path_n_to_string
from hw_common import HWType, HWDevice, HWPinException, get_hw_type_from_client, HWNotConnectedException, \
    DEFAULT_HW_BUSY_TITLE, DEFAULT_HW_BUSY_MESSAGE, HWSessionBase
import logging
from wallet_common import UtxoType, TxOutputType
from wnd_utils import WndUtils
import hw_intf_ledgernano as ledger
import hw_intf_keepkey as keepkey
import hw_intf_trezor as trezor
from app_defs import get_note_url
from app_utils import SHA256
from common import CancelException
from thread_utils import EnhRLock

# Dict[str <hd tree ident>, Dict[str <bip32 path>, Tuple[str <address>, int <db id>]]]
bip32_address_map: Dict[str, Dict[str, Tuple[str, int]]] = {}

hd_tree_db_map: Dict[str, int] = {}  # Dict[str <hd tree ident>, int <db id>]

log = logging.getLogger('dmt.hw_intf')


# todo: verify if it's still needed
def control_trezor_keepkey_libs(connecting_to_hw):
    """
    Check if trying to switch between Trezor and Keepkey on Linux. It's not allowed because Trezor/Keepkey's client
    libraries use objects with the same names (protobuf), which causes errors when switching between them.
    :param connecting_to_hw: type of the hardware wallet we are going to connect to.
    :return:
    """
    if sys.platform == 'linux' and ((connecting_to_hw == HWType.trezor and 'keepkeylib' in sys.modules.keys()) or
                                    (connecting_to_hw == HWType.keepkey and 'trezorlib' in sys.modules.keys())):
        raise Exception('On linux OS switching between Trezor/Keepkey wallets requires restarting the '
                        'application.\n\nPlease restart the application to continue.')


def control_hw_call(func):
    """
    Decorator for some of the hardware wallet functions. It ensures, that hw client connection is open (and if is not, 
    it makes attempt to open it). The s econt thing is to catch OSError exception as a result of disconnecting 
    hw cable. After this, connection has to be closed and opened again, otherwise 'read error' occurrs. 
    :param func: function decorated. First argument of the function has to be the reference to the MainWindow object.
    """

    def catch_hw_client(*args, **kwargs):
        hw_session: HwSessionInfo = args[0]
        client = hw_session.hw_client
        if not client:
            client = hw_session.hw_connect()
        if not client:
            raise HWNotConnectedException()
        try:
            try:
                # protect against simultaneous access to the same device from different threads
                hw_session.acquire_client()

                control_trezor_keepkey_libs(hw_session.hw_type)
                if hw_session.hw_type == HWType.trezor:

                    try:
                        ret = func(*args, **kwargs)
                    except trezorlib.exceptions.PinException as e:
                        raise HWPinException(e.args[1])

                elif hw_session.hw_type == HWType.keepkey:

                    try:
                        ret = func(*args, **kwargs)
                    except keepkeylib.client.PinException as e:
                        raise HWPinException(e.args[1])

                elif hw_session.hw_type == HWType.ledger_nano:

                    ret = func(*args, **kwargs)

                else:
                    raise Exception('Uknown hardware wallet type: ' + str(hw_session.hw_type))
            finally:
                hw_session.release_client()

        except (OSError, usb1.USBErrorNoDevice) as e:
            logging.exception('Exception calling %s function' % func.__name__)
            logging.info('Disconnecting HW after OSError occurred')
            hw_session.hw_disconnect()
            raise HWNotConnectedException('The hardware wallet device has been disconnected with the '
                                          'following error: ' + str(e))

        except HWPinException:
            raise

        except CancelException:
            raise

        except Exception:
            logging.exception('Exception calling %s function' % func.__name__)
            raise

        return ret

    return catch_hw_client


def get_device_list(hw_types: Tuple[HWType, ...], return_clients: bool = True, allow_bootloader_mode: bool = False,
                    use_webusb=True, use_bridge=True, use_udp=True, use_hid=True, passphrase_encoding='NFC') \
        -> List[HWDevice]:
    dev_list = []

    if HWType.trezor in hw_types:
        devs = trezor.get_device_list(return_clients, allow_bootloader_mode=allow_bootloader_mode,
                                      use_webusb=use_webusb, use_bridge=use_bridge, use_udp=use_udp, use_hid=use_hid)
        dev_list.extend(devs)

    if HWType.keepkey in hw_types:
        devs = keepkey.get_device_list(return_clients, passphrase_encoding, allow_bootloader_mode=allow_bootloader_mode)
        dev_list.extend(devs)

    if HWType.ledger_nano in hw_types:
        devs = ledger.get_device_list(return_clients, allow_bootloader_mode=allow_bootloader_mode)
        dev_list.extend(devs)

    return dev_list


def cancel_hw_thread_dialog(hw_client):
    try:
        hw_type = get_hw_type_from_client(hw_client)
        if hw_type == HWType.trezor:
            hw_client.cancel()
        elif hw_type == HWType.keepkey:
            hw_client.cancel()
        elif hw_type == HWType.ledger_nano:
            return False
        raise CancelException('Cancel')
    except CancelException:
        raise
    except Exception as e:
        logging.warning('Error when canceling hw session. Details: %s', str(e))
        return True


def cancel_hw_operation(hw_client):
    try:
        hw_type = get_hw_type_from_client(hw_client)
        if hw_type in (HWType.trezor, HWType.keepkey):
            hw_client.cancel()
    except Exception as e:
        logging.error('Error when cancelling hw operation: %s', str(e))


def get_hw_label(hw_client):
    hw_type = get_hw_type_from_client(hw_client)
    if hw_type in (HWType.trezor, HWType.keepkey):
        return hw_client.features.label
    elif hw_type == HWType.ledger_nano:
        return 'Ledger Nano S'


@control_hw_call
def get_hw_firmware_version(hw_session: 'HwSessionInfo'):
    hw_type = get_hw_type_from_client(hw_session.hw_client)
    if hw_type in (HWType.trezor, HWType.keepkey):

        return str(hw_session.hw_client.features.major_version) + '.' + \
               str(hw_session.hw_client.features.minor_version) + '.' + \
               str(hw_session.hw_client.features.patch_version)

    elif hw_type == HWType.ledger_nano:

        return hw_session.hw_client.getFirmwareVersion().get('version')


def firmware_update(hw_client, raw_data: bytes):
    hw_type = get_hw_type_from_client(hw_client)
    if hw_type == HWType.trezor:
        trezor.firmware_update(hw_client, raw_data)
    elif HWType.keepkey:
        hw_client.firmware_update(fp=BytesIO(raw_data))
    elif hw_type == HWType.ledger_nano:
        raise Exception('Ledger Nano S is not supported.')


@control_hw_call
def sign_tx(hw_session: 'HwSessionInfo', utxos_to_spend: List[UtxoType],
            tx_outputs: List[TxOutputType], tx_fee):
    """
    Creates a signed transaction.
    :param hw_session:
    :param utxos_to_spend: list of utxos to send
    :param tx_outputs: destination addresses. Fields: 0: dest Dash address. 1: the output value in satoshis,
        2: the bip32 path of the address if the output is the change address or None otherwise
    :param tx_fee: transaction fee
    :return: tuple (serialized tx, total transaction amount in satoshis)
    """

    def sign(ctrl):
        ctrl.dlg_config_fun(dlg_title="Confirm transaction signing.", show_progress_bar=False)
        ctrl.display_msg_fun('<b>Click the confirmation button on your hardware wallet<br>'
                             'and wait for the transaction to be signed...</b>')

        if hw_session.hw_type == HWType.trezor:

            return trezor.sign_tx(hw_session, utxos_to_spend, tx_outputs, tx_fee)

        elif hw_session.hw_type == HWType.keepkey:

            return keepkey.sign_tx(hw_session, utxos_to_spend, tx_outputs, tx_fee)

        elif hw_session.hw_type == HWType.ledger_nano:

            return ledger.sign_tx(hw_session, utxos_to_spend, tx_outputs, tx_fee)

        else:
            logging.error('Invalid HW type: ' + str(hw_session.hw_type))

    # execute the 'prepare' function, but due to the fact that the call blocks the UI until the user clicks the HW
    # button, it's done inside a thread within a dialog that shows an appropriate message to the user
    sig = WndUtils.run_thread_dialog(sign, (), True,
                                     force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_session.hw_client))
    return sig


@control_hw_call
def hw_sign_message(hw_session: 'HwSessionInfo', bip32path, message, display_label: str = None):
    def sign(ctrl, display_label_):
        ctrl.dlg_config_fun(dlg_title="Confirm message signing.", show_progress_bar=False)
        if not display_label_:
            if hw_session.hw_type == HWType.ledger_nano:
                message_hash = hashlib.sha256(message.encode('ascii')).hexdigest().upper()
                display_label_ = '<b>Click the confirmation button on your hardware wallet to sign the message...</b>' \
                                 '<br><br><b>Message:</b><br><span>' + message + '</span><br><br><b>SHA256 hash</b>:' \
                                                                                 '<br>' + message_hash
            else:
                display_label_ = '<b>Click the confirmation button on your hardware wallet to sign the message...</b>'
        ctrl.display_msg_fun(display_label_)

        if hw_session.hw_type == HWType.trezor:

            return trezor.sign_message(hw_session, bip32path, message)

        elif hw_session.hw_type == HWType.keepkey:

            return keepkey.sign_message(hw_session, bip32path, message)

        elif hw_session.hw_type == HWType.ledger_nano:

            return ledger.sign_message(hw_session, bip32path, message)
        else:
            logging.error('Invalid HW type: ' + str(hw_session.hw_type))

    # execute the 'sign' function, but due to the fact that the call blocks the UI until the user clicks the HW
    # button, it's done inside a thread within a dialog that shows an appropriate message to the user
    sig = WndUtils.run_thread_dialog(sign, (display_label,), True,
                                     force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_session.hw_client))
    return sig


def change_pin(hw_client, remove=False):
    hw_type = get_hw_type_from_client(hw_client)
    if hw_type == HWType.trezor:

        return trezor.change_pin(hw_client, remove)

    elif hw_type == HWType.keepkey:

        return keepkey.change_pin(hw_client, remove)

    elif hw_type == HWType.ledger_nano:

        raise Exception('Ledger Nano S is not supported.')

    else:
        logging.error('Invalid HW type: ' + str(hw_type))


def action_on_device_message(message=DEFAULT_HW_BUSY_MESSAGE, title=DEFAULT_HW_BUSY_TITLE):
    def decorator_f(func):
        def wrapped_f(*args, **kwargs):
            hw_client = None
            hw_client_names = ('MyTrezorClient', 'KeepkeyClient')

            # look for hw client:
            for arg in args:
                name = type(arg).__name__
                if name in hw_client_names:
                    hw_client = arg
                    break

            if not hw_client:
                for arg_name in kwargs:
                    name = type(kwargs[arg_name]).__name__
                    if name in hw_client_names:
                        hw_client = kwargs[arg_name]
                        break

            def thread_dialog(ctrl):
                if ctrl:
                    ctrl.dlg_config_fun(dlg_title=title, show_progress_bar=False)
                    ctrl.display_msg_fun(message)

                return func(*args, **kwargs)

            return WndUtils.run_thread_dialog(thread_dialog, (), True, show_window_delay_ms=1000,
                                              force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_client))

        return wrapped_f

    return decorator_f


@action_on_device_message()
def enable_passphrase(hw_client, passphrase_enabled):
    hw_type = get_hw_type_from_client(hw_client)
    if hw_type == HWType.trezor:
        trezor.enable_passphrase(hw_client, passphrase_enabled)
    elif hw_type == HWType.keepkey:
        hw_client.apply_settings(use_passphrase=passphrase_enabled)
    elif hw_type == HWType.ledger_nano:
        raise Exception('Ledger Nano S is not supported.')
    else:
        logging.error('Invalid HW type: ' + str(hw_type))


@action_on_device_message()
def set_passphrase_always_on_device(hw_client, enabled):
    hw_type = get_hw_type_from_client(hw_client)
    if hw_type == HWType.trezor:
        trezor.set_passphrase_always_on_device(hw_client, enabled)
    elif hw_type == HWType.keepkey:
        raise Exception('Keepkey not supported.')
    elif hw_type == HWType.ledger_nano:
        raise Exception('Ledger Nano S is not supported.')
    else:
        logging.error('Invalid HW type: ' + str(hw_type))


@action_on_device_message()
def set_wipe_code(hw_client, enabled):
    hw_type = get_hw_type_from_client(hw_client)
    if hw_type == HWType.trezor:
        trezor.set_wipe_code(hw_client, enabled)
    elif hw_type == HWType.keepkey:
        raise Exception('Keepkey not supported.')
    elif hw_type == HWType.ledger_nano:
        raise Exception('Ledger Nano S is not supported.')
    else:
        logging.error('Invalid HW type: ' + str(hw_type))


@control_hw_call
def get_address(hw_session: 'HwSessionInfo', bip32_path: str, show_display: bool = False,
                message_to_display: str = None):
    def _get_address(ctrl, hw_session_: HwSessionInfo, bip32_path_: str, show_display_: bool = False,
                     message_to_display_: str = None):
        if ctrl:
            ctrl.dlg_config_fun(dlg_title=DEFAULT_HW_BUSY_TITLE, show_progress_bar=False)
            if message_to_display_:
                ctrl.display_msg_fun(message_to_display_)
            else:
                ctrl.display_msg_fun('<b>Click the confirmation button on your hardware wallet to exit...</b>')

        client = hw_session_.hw_client
        if client:
            if isinstance(bip32_path_, str):
                bip32_path_.strip()
                if bip32_path_.lower().find('m/') >= 0:
                    # removing m/ prefix because of keepkey library
                    bip32_path_ = bip32_path_[2:]

            if hw_session_.hw_type == HWType.trezor:

                try:
                    if isinstance(bip32_path_, str):
                        bip32_path_ = dash_utils.bip32_path_string_to_n(bip32_path_)
                    ret = trezorlib.btc.get_address(client, hw_session_.hw_coin_name, bip32_path_, show_display_)
                    return ret
                except (CancelException, trezorlib.exceptions.Cancelled):
                    raise CancelException()

            elif hw_session_.hw_type == HWType.keepkey:

                try:
                    if isinstance(bip32_path_, str):
                        bip32_path_ = dash_utils.bip32_path_string_to_n(bip32_path_)
                    return client.get_address(hw_session_.hw_coin_name, bip32_path_, show_display_)
                except keepkeylib.client.CallException as e:
                    if isinstance(e.args, tuple) and len(e.args) >= 2 and isinstance(e.args[1], str) and \
                            e.args[1].find('cancel') >= 0:
                        raise CancelException('Cancelled')

            elif hw_session_.hw_type == HWType.ledger_nano:

                if isinstance(bip32_path_, list):
                    # ledger requires bip32 path argument as a string
                    bip32_path_ = bip32_path_n_to_string(bip32_path_)

                adr_pubkey = ledger.get_address_and_pubkey(client, bip32_path_, show_display_)
                return adr_pubkey.get('address')
            else:
                raise Exception('Unknown hardware wallet type: ' + str(hw_session_.hw_type))
        else:
            raise Exception('HW client not open.')

    if message_to_display or show_display:
        msg_delay = 0
    else:
        msg_delay = 1000
        message_to_display = DEFAULT_HW_BUSY_MESSAGE

    return WndUtils.run_thread_dialog(_get_address, (hw_session, bip32_path, show_display, message_to_display),
                                      True, show_window_delay_ms=msg_delay,
                                      force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_session.hw_client))


@control_hw_call
def get_address_and_pubkey(hw_session: 'HwSessionInfo', bip32_path):
    client = hw_session.hw_client
    if client:
        if isinstance(bip32_path, str):
            bip32_path.strip()
            if bip32_path.lower().find('m/') >= 0:
                # removing m/ prefix because of keepkey library
                bip32_path = bip32_path[2:]

        if hw_session.hw_type == HWType.trezor:

            if isinstance(bip32_path, str):
                bip32_path = dash_utils.bip32_path_string_to_n(bip32_path)
            return {
                'address': trezorlib.btc.get_address(client, hw_session.hw_coin_name, bip32_path, False),
                'publicKey': trezorlib.btc.get_public_node(client, bip32_path).node.public_key
            }

        elif hw_session.hw_type == HWType.keepkey:
            if isinstance(bip32_path, str):
                bip32_path = dash_utils.bip32_path_string_to_n(bip32_path)
            return {
                'address': client.get_address(hw_session.hw_coin_name, bip32_path, False),
                'publicKey': client.get_public_node(bip32_path).node.public_key
            }

        elif hw_session.hw_type == HWType.ledger_nano:

            if isinstance(bip32_path, list):
                # ledger requires bip32 path argument as a string
                bip32_path = bip32_path_n_to_string(bip32_path)

            return ledger.get_address_and_pubkey(client, bip32_path)
        else:
            raise Exception('Unknown hardware wallet type: ' + str(hw_session.hw_type))


@control_hw_call
def get_xpub(hw_session: 'HwSessionInfo', bip32_path):
    client = hw_session.hw_client
    if client:
        if isinstance(bip32_path, str):
            bip32_path.strip()
            if bip32_path.lower().find('m/') >= 0:
                bip32_path = bip32_path[2:]

        if hw_session.hw_type == HWType.trezor:
            if isinstance(bip32_path, str):
                bip32_path = dash_utils.bip32_path_string_to_n(bip32_path)

            return trezorlib.btc.get_public_node(client, bip32_path).xpub

        elif hw_session.hw_type == HWType.keepkey:
            if isinstance(bip32_path, str):
                bip32_path = dash_utils.bip32_path_string_to_n(bip32_path)

            return client.get_public_node(bip32_path).xpub

        elif hw_session.hw_type == HWType.ledger_nano:

            if isinstance(bip32_path, list):
                # ledger requires bip32 path argument as a string
                bip32_path = bip32_path_n_to_string(bip32_path)

            return ledger.get_xpub(client, bip32_path)
        else:
            raise Exception('Unknown hardware wallet type: ' + str(hw_session.hw_type))
    else:
        raise Exception('HW client not open.')


def wipe_device(hw_type: HWType, hw_device_id: Optional[str], parent_window=None) -> Tuple[Optional[str], bool]:
    """
    Wipes the hardware wallet device.
    :param hw_type: app_config.HWType
    :param hw_device_id: id of the device selected by the user (TrezorClient, KeepkeyClient)
    :param parent_window: ref to a window according to which will be centered message dialogs created here
    :return: Tuple
        Ret[0]: Device id. After wiping a new device id is generated, which is returned to the caller.
        Ret[1]: True, if the user cancelled the operation. In this situation we deliberately don't raise the 'cancelled'
            exception, because in the case of changing of the device id (when wiping) we want to pass it back to
            the caller.
    """

    def wipe(ctrl):
        ctrl.dlg_config_fun(dlg_title="Confirm wiping device.", show_progress_bar=False)
        ctrl.display_msg_fun('<b>Read the messages displyed on your hardware wallet <br>'
                             'and click the confirmation button when necessary...</b>')

        if hw_type == HWType.trezor:

            return trezor.wipe_device(hw_device_id)

        elif hw_type == HWType.keepkey:

            return keepkey.wipe_device(hw_device_id)

        elif hw_type == HWType.ledger_nano:

            raise Exception('Not supported by Ledger Nano S.')

        else:
            raise Exception('Invalid HW type: ' + str(hw_type))

    # execute the 'wipe' inside a thread to avoid blocking UI
    return WndUtils.run_thread_dialog(wipe, (), True, center_by_window=parent_window)


def load_device_by_mnemonic(hw_type: HWType, hw_device_id: Optional[str], mnemonic_words: str,
                            pin: str, passphrase_enabled: bool, hw_label: str, passphrase: str,
                            secondary_pin: str) -> Tuple[Optional[str], bool]:
    """
    Initializes hardware wallet with a mnemonic words. For security reasons use this function only on an offline
    system, that will never be connected to the Internet.
    :param hw_type: app_config.HWType
    :param hw_device_id: id of the device selected by the user (TrezorClient, KeepkeyClient); None for Ledger Nano S
    :param mnemonic_words: string of 12/18/24 mnemonic words (separeted by spaces)
    :param pin: string with a new pin
    :param passphrase_enabled: if True, hw will have passphrase enabled (Trezor/Keepkey)
    :param hw_label: label for device (Trezor/Keepkey)
    :param passphrase: passphrase to be saved in the device (Ledger Nano S)
    :param secondary_pin: PIN securing passphrase (Ledger Nano S)
    :return: Tuple
        Ret[0]: Device id. If a device is wiped before initializing with mnemonics, a new device id is generated. It's
            returned to the caller.
        Ret[1]: True, if the user cancelled the operation. In this situation we deliberately don't raise the 'cancelled'
            exception, because in the case of changing of the device id (when wiping) we want to pass it back to
            the caller.
        Ret[0] and Ret[1] are None for Ledger devices.
    """

    def load(ctrl, hw_device_id_: str, mnemonic_: str, pin_: str, passphrase_enbled_: bool, hw_label_: str) -> \
            Tuple[Optional[str], bool]:

        ctrl.dlg_config_fun(dlg_title="Please confirm", show_progress_bar=False)
        ctrl.display_msg_fun('<b>Read the messages displyed on your hardware wallet <br>'
                             'and click the confirmation button when necessary...</b>')

        if hw_device_id_:
            if hw_type == HWType.trezor:
                raise Exception('Feature no longer available for Trezor')
            elif hw_type == HWType.keepkey:
                return keepkey.load_device_by_mnemonic(hw_device_id_, mnemonic_, pin_, passphrase_enbled_, hw_label_)
            else:
                raise Exception('Not supported by Ledger Nano S.')
        else:
            raise HWNotConnectedException()

    if hw_type == HWType.ledger_nano:

        ledger.load_device_by_mnemonic(mnemonic_words, pin, passphrase, secondary_pin)
        return hw_device_id, False

    else:
        return WndUtils.run_thread_dialog(load, (hw_device_id, mnemonic_words, pin, passphrase_enabled, hw_label),
                                          True)


def recover_device(hw_type: HWType, hw_device_id: str, word_count: int, passphrase_enabled: bool, pin_enabled: bool,
                   hw_label: str, parent_window=None) -> Tuple[Optional[str], bool]:
    """
    :param hw_type: app_config.HWType
    :param hw_device_id: id of the device selected by the user (TrezorClient, KeepkeyClient); None for Ledger Nano S
    :param word_count: number of recovery words (12/18/24)
    :param passphrase_enabled: if True, hw will have passphrase enabled (Trezor/Keepkey)
    :param pin_enabled: if True, hw will have pin enabled (Trezor/Keepkey)
    :param hw_label: label for device (Trezor/Keepkey)
    :param parent_window: ref to a window according to which will be centered message dialogs created here
    :return: Tuple
        Ret[0]: Device id. If a device is wiped before recovering seed, a new device id is generated. It's
            returned to the caller.
        Ret[1]: True, if the user cancelled the operation. In this situation we deliberately don't raise the
            'cancelled' exception, because in the case of changing of the device id (when wiping) we want to pass
            it back to the caller function.
        Ret[0] and Ret[1] are None for Ledger devices.
    """

    def load(ctrl, hw_type_: HWType, hw_device_id_: str, word_count_: int, passphrase_enabled_: bool,
             pin_enabled_: bool, hw_label_: str) -> Tuple[Optional[str], bool]:

        ctrl.dlg_config_fun(dlg_title="Please confirm", show_progress_bar=False)
        ctrl.display_msg_fun('<b>Read the messages displyed on your hardware wallet <br>'
                             'and click the confirmation button when necessary...</b>')

        if hw_device_id_:
            if hw_type_ == HWType.trezor:

                return trezor.recover_device(hw_device_id_, word_count_, passphrase_enabled_, pin_enabled_, hw_label_)

            elif hw_type_ == HWType.keepkey:

                return keepkey.recover_device(hw_device_id_, word_count_, passphrase_enabled_, pin_enabled_, hw_label_)

            else:
                raise Exception('Not supported by Ledger Nano S.')
        else:
            raise HWNotConnectedException()

    if hw_type == HWType.ledger_nano:
        raise Exception('Not supported by Ledger Nano S.')
    else:
        return WndUtils.run_thread_dialog(load, (hw_type, hw_device_id, word_count, passphrase_enabled, pin_enabled,
                                                 hw_label), True, center_by_window=parent_window)


def reset_device(hw_type: HWType, hw_device_id: str, word_count: int, passphrase_enabled: bool, pin_enabled: bool,
                 hw_label: str, parent_window=None) -> Tuple[Optional[str], bool]:
    """
    Initialize device with a newly generated words.
    :param hw_type: app_config.HWType
    :param hw_device_id: id of the device selected by the user (TrezorClient, KeepkeyClient); None for Ledger Nano S
    :param word_count: number of words (12/18/24)
    :param passphrase_enabled: if True, hw will have passphrase enabled (Trezor/Keepkey)
    :param pin_enabled: if True, hw will have pin enabled (Trezor/Keepkey)
    :param hw_label: label for device (Trezor/Keepkey)
    :param parent_window: ref to a window according to which will be centered message dialogs created here
    :return: Tuple
        Ret[0]: Device id. If a device is wiped before initializing with mnemonics, a new device id is generated. It's
            returned to the caller.
        Ret[1]: True, if the user cancelled the operation. In this situation we deliberately don't raise the
            'cancelled' exception, because in the case of changing of the device id (when wiping) we want to pass
            it back to the caller function.
        Ret[0] and Ret[1] are None for Ledger devices.
    """

    def load(ctrl, hw_type_: HWType, hw_device_id_: str, strength_: int, passphrase_enabled_: bool, pin_enabled_: bool,
             hw_label_: str) -> Tuple[Optional[str], bool]:

        ctrl.dlg_config_fun(dlg_title="Please confirm", show_progress_bar=False)
        ctrl.display_msg_fun('<b>Read the messages displyed on your hardware wallet <br>'
                             'and click the confirmation button when necessary...</b>')
        if hw_device_id_:
            if hw_type_ == HWType.trezor:

                return trezor.reset_device(hw_device_id_, strength_, passphrase_enabled_, pin_enabled_, hw_label_)

            elif hw_type_ == HWType.keepkey:

                return keepkey.reset_device(hw_device_id_, strength_, passphrase_enabled_, pin_enabled_, hw_label_)

            else:
                raise Exception('Not supported by Ledger Nano S.')
        else:
            raise HWNotConnectedException()

    if hw_type == HWType.ledger_nano:
        raise Exception('Not supported by Ledger Nano S.')
    else:
        if word_count not in (12, 18, 24):
            raise Exception('Invalid word count.')
        strength = {24: 32, 18: 24, 12: 16}.get(word_count) * 8

        return WndUtils.run_thread_dialog(load, (hw_type, hw_device_id, strength, passphrase_enabled, pin_enabled,
                                                 hw_label), True, center_by_window=parent_window)


@control_hw_call
def hw_encrypt_value(hw_session: 'HwSessionInfo', bip32_path_n: List[int], label: str,
                     value: ByteString, ask_on_encrypt=True, ask_on_decrypt=True) -> Tuple[bytearray, bytearray]:
    """Encrypts a value with a hardware wallet.
    :param hw_session:
    :param bip32_path_n: bip32 path of the private key used for encryption
    :param label: key (in the meaning of key-value) used for encryption
    :param value: value being encrypted
    :param ask_on_encrypt: see Trezor doc
    :param ask_on_decrypt: see Trezor doc
    """

    def encrypt(ctrl, hw_session_: HwSessionInfo, bip32_path_n_: List[int], label_: str,
                value_: bytearray):
        ctrl.dlg_config_fun(dlg_title="Data encryption", show_progress_bar=False)
        ctrl.display_msg_fun(f'<b>Encrypting \'{label_}\'...</b>'
                             f'<br><br>Enter the hardware wallet PIN/passphrase (if needed) to encrypt data.<br><br>'
                             f'<b>Note:</b> encryption passphrase is independent from the wallet passphrase  <br>'
                             f'and can vary for each encrypted file.')

        if hw_session_.hw_type == HWType.trezor:
            try:
                client = hw_session_.hw_client
                data = trezorlib.misc.encrypt_keyvalue(client, cast(Address, bip32_path_n_), label_, value_,
                                                       ask_on_encrypt, ask_on_decrypt)
                pub_key = trezorlib.btc.get_public_node(client, bip32_path_n_).node.public_key
                return data, pub_key
            except (CancelException, trezorlib.exceptions.Cancelled):
                raise CancelException()

        elif hw_session_.hw_type == HWType.keepkey:

            client = hw_session_.hw_client
            data = client.encrypt_keyvalue(bip32_path_n_, label_, value_, ask_on_encrypt, ask_on_decrypt)
            pub_key = client.get_public_node(bip32_path_n_).node.public_key
            return data, pub_key

        elif hw_session_.hw_type == HWType.ledger_nano:

            raise Exception('Feature not available for Ledger Nano S.')

        else:
            raise Exception('Invalid HW type: ' + str(hw_session_))

    if len(value) != 32:
        raise ValueError("Invalid password length (<> 32).")

    return WndUtils.run_thread_dialog(encrypt, (hw_session, bip32_path_n, label, value), True,
                                      force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_session.hw_client),
                                      show_window_delay_ms=200)


@control_hw_call
def hw_decrypt_value(hw_session: 'HwSessionInfo', bip32_path_n: List[int], label: str,
                     value: ByteString, ask_on_encrypt=True, ask_on_decrypt=True) -> Tuple[bytearray, bytearray]:
    """
    :param hw_session:
    :param bip32_path_n: bip32 path of the private key used for encryption
    :param label: key (in the meaning of key-value) used for encryption
    :param value: encrypted value to be decrypted,
    :param ask_on_encrypt: see Trezor doc
    :param ask_on_decrypt: see Trezor doc
    """

    def decrypt(ctrl, hw_session_: HwSessionInfo, bip32_path_n_: List[int], label_: str, value_: bytearray):
        ctrl.dlg_config_fun(dlg_title="Data decryption", show_progress_bar=False)
        ctrl.display_msg_fun(f'<b>Decrypting \'{label_}\'...</b><br><br>Enter the hardware wallet PIN/passphrase '
                             f'(if needed)<br> and click the confirmation button to decrypt data.')

        if hw_session_.hw_type == HWType.trezor:

            try:
                client = hw_session_.hw_client
                data = trezorlib.misc.decrypt_keyvalue(client, cast(Address, bip32_path_n_), label_, value_,
                                                       ask_on_encrypt, ask_on_decrypt)
                pub_key = trezorlib.btc.get_public_node(client, bip32_path_n_).node.public_key
                return data, pub_key
            except (CancelException, trezorlib.exceptions.Cancelled):
                raise CancelException()

        elif hw_session_.hw_type == HWType.keepkey:

            client = hw_session_.hw_client
            data = client.decrypt_keyvalue(bip32_path_n_, label_, value_, ask_on_encrypt, ask_on_decrypt)
            pub_key = client.get_public_node(bip32_path_n_).node.public_key
            return data, pub_key

        elif hw_session_.hw_type == HWType.ledger_nano:

            raise Exception('Feature not available for Ledger Nano S.')

        else:
            raise Exception('Invalid HW type: ' + str(hw_session_))

    if len(value) != 32:
        raise ValueError("Invalid password length (<> 32).")

    return WndUtils.run_thread_dialog(decrypt, (hw_session, bip32_path_n, label, value), True,
                                      force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_session.hw_client))


class HWDevices(object):
    """
    Manages information about all hardware wallet devices connected to the computer.
    """
    __instance = None

    @staticmethod
    def get_instance():
        return HWDevices.__instance

    def __init__(self, use_webusb=True, use_bridge=True, use_udp=True, use_hid=True, passphrase_encoding='NFC'):
        if HWDevices.__instance is not None:
            raise Exception('Internal error: cannot create another instance of this class')
        self.__hw_devices: List[HWDevice] = []
        self.__hw_device_id_selected: Optional[str] = None  # device id of the hw client selected
        self.__devices_fetched = False
        self.__use_webusb = use_webusb
        self.__use_bridge = use_bridge
        self.__use_udp = use_udp
        self.__use_hid = use_hid
        self.__hw_types_allowed: Tuple[HWType, ...] = (HWType.trezor, HWType.keepkey, HWType.ledger_nano)
        self.__passphrase_encoding: Optional[str] = passphrase_encoding

    def load_hw_devices(self, force_fetch: bool = False):
        """
        Load all instances of the selected hardware wallet type. If there is more than one, user has to select which
        one he is going to use.
        """
        if force_fetch or not self.__devices_fetched:
            self.clear_devices()
            self.__hw_devices = get_device_list(
                hw_types=self.__hw_types_allowed, return_clients=False, use_webusb=self.__use_webusb,
                use_bridge=self.__use_bridge, use_udp=self.__use_udp, use_hid=self.__use_hid,
                passphrase_encoding=self.__passphrase_encoding)

            self.__devices_fetched = True
            if self.__hw_device_id_selected:
                if self.get_selected_device_index() is None:
                    self.__hw_device_id_selected = None

    def close_all_hw_clients(self):
        try:
            for idx, hw_inst in enumerate(self.__hw_devices):
                if hw_inst.client:
                    hw_inst.client.close()
                    hw_inst.client = None
        except Exception as e:
            logging.exception(str(e))

    def clear_devices(self):
        self.close_all_hw_clients()
        self.__hw_devices.clear()

    def clear(self):
        self.clear_devices()
        self.__hw_device_id_selected = None

    def set_hw_types_allowed(self, allowed: Tuple[HWType]):
        self.__hw_types_allowed = allowed[:]

    def get_selected_device_index(self):
        return next((i for i, device in enumerate(self.__hw_devices)
                     if device.device_id == self.__hw_device_id_selected), -1)

    def get_devices(self) -> List[HWDevice]:
        return self.__hw_devices

    def get_selected_device(self) -> Optional[HWDevice]:
        idx = self.get_selected_device_index()
        if idx >= 0:
            return self.__hw_devices[idx]
        else:
            return None

    def select_device(self, device: HWDevice):
        if device in self.__hw_devices:
            self.__hw_device_id_selected = device.device_id
        else:
            raise Exception('Non existent hw device object.')

    def select_device_by_index(self, index: int):
        if 0 <= index < len(self.__hw_devices):
            self.__hw_device_id_selected = self.__hw_devices[index].device_id
        else:
            raise Exception('Device index out of bounds.')

    @staticmethod
    def open_hw_client_for_device(hw_device: HWDevice):
        if not hw_device.client:
            if hw_device.hw_type == HWType.trezor:
                hw_device.client = trezor.open_trezor_client(hw_device.transport)
            elif hw_device.hw_type == HWType.keepkey:
                hw_device.client = keepkey.open_keepkey_client(hw_device.transport)
            elif hw_device.hw_type == HWType.ledger_nano:
                hw_device.client = ledger.open_ledgernano_client(hw_device.transport)
            else:
                raise Exception('Invalid HW type: ' + str(hw_device.hw_type))

    @staticmethod
    def close_hw_client_for_device(hw_device: HWDevice):
        if hw_device.client:
            try:
                if hw_device.hw_type in (HWType.trezor, HWType.keepkey):
                    hw_device.client.close()
                elif hw_device.hw_type == HWType.ledger_nano:
                    hw_device.client.close()

                del hw_device.client
                hw_device.client = None
            except Exception:
                # probably already disconnected
                logging.exception('Disconnect HW error')


class HwSessionInfo(HWSessionBase):
    sig_hw_connected = QtCore.pyqtSignal(HWDevice)
    sig_hw_disconnected = QtCore.pyqtSignal()
    sig_hw_connection_error = QtCore.pyqtSignal(str)

    def __init__(self, main_dlg, app_config: object, dashd_intf: object):
        super().__init__(app_config)

        self.__locks = {}  # key: hw_client, value: EnhRLock
        self.__main_dlg = main_dlg
        self.__dashd_intf = dashd_intf
        self.__base_bip32_path: str = ''
        self.__base_public_key: bytes = b''
        self.__hd_tree_ident: str = ''
        self.__use_webusb = self._app_config.trezor_webusb
        self.__use_bridge = self._app_config.trezor_bridge
        self.__use_udp = self._app_config.trezor_udp
        self.__use_hid = self._app_config.trezor_hid
        self.__passphrase_encoding: Optional[str] = self._app_config.hw_keepkey_psw_encoding

        self.__hw_devices = HWDevices(use_webusb=self.__use_webusb, use_bridge=self.__use_bridge,
                                      use_udp=self.__use_udp, use_hid=self.__use_hid,
                                      passphrase_encoding=self.__passphrase_encoding)

    def signal_hw_connected(self):
        self.sig_hw_connected.emit(self.hw_device)

    def signal_hw_disconnected(self):
        self.sig_hw_disconnected.emit()

    def signal_hw_connection_error(self, message):
        self.sig_hw_disconnected.emit(message)

    @property
    def hw_device(self):
        return self.__hw_devices.get_selected_device()

    def get_hw_client(self) -> Optional[object]:
        hw_device = self.hw_device
        if hw_device:
            return hw_device.client
        return None

    @property
    def hw_type(self):
        hw_device = self.hw_device
        if hw_device:
            return hw_device.hw_type
        else:
            return None

    def acquire_client(self):
        cli = self.hw_client
        if cli:
            lock = self.__locks.get(cli)
            if not lock:
                lock = EnhRLock()
                self.__locks[cli] = lock
            lock.acquire()

    def release_client(self):
        cli = self.hw_client
        if cli:
            lock = self.__locks.get(cli)
            if not lock:
                raise Exception(f'Lock for client {str(cli)} not acquired before.')
            lock.release()

    def set_base_info(self, bip32_path: str, public_key: bytes):
        self.__base_bip32_path = bip32_path
        self.__base_public_key = public_key
        self.__hd_tree_ident = SHA256.new(public_key).digest().hex()

    @property
    def base_bip32_path(self):
        return self.__base_bip32_path

    @property
    def base_public_key(self):
        return self.__base_public_key

    def get_hd_tree_ident(self, coin_name: str):
        if not coin_name:
            raise Exception('Missing coin name')
        if not self.__hd_tree_ident:
            raise HWNotConnectedException()
        return self.__hd_tree_ident + bytes(coin_name, 'ascii').hex()

    def select_device(self) -> Optional[HWDevice]:
        dlg = SelectHWDeviceDlg(self.__main_dlg, "Select hardware wallet device", self.__hw_devices)
        if dlg.exec_():
            self.__hw_devices.select_device(dlg.selected_hw_device)
            return dlg.selected_hw_device
        return None

    def initiate_hw_session(self):
        """
        Read this information from the hw device, that will cause it to ask the user for a BIP39 passphrase, if
        necessary. The point is to make sure that the device is fully initiated and ready for next calls.
        """

        def get_session_info_trezor(get_public_node_fun, hw_device_):
            def call_get_public_node(_, get_public_node_fun_, path_n_):
                pk = get_public_node_fun_(path_n_).node.public_key
                return pk

            path_ = dash_utils.get_default_bip32_base_path(self.dash_network)
            path_n = dash_utils.bip32_path_string_to_n(path_)

            # show message for Trezor device while waiting for the user to choose the passphrase input method
            pub = WndUtils.run_thread_dialog(
                call_get_public_node, (get_public_node_fun, path_n),
                title=DEFAULT_HW_BUSY_TITLE, text=DEFAULT_HW_BUSY_MESSAGE,
                force_close_dlg_callback=partial(cancel_hw_thread_dialog, hw_device_.client),
                show_window_delay_ms=1000)

            if pub:
                self.set_base_info(path_, pub)
            else:
                raise Exception('Couldn\'t read data from the hardware wallet.')

        hw_device = self.hw_device
        if not hw_device:
            raise Exception('Internal error: hw device not ready')
        self.__hw_devices.open_hw_client_for_device(hw_device)

        try:
            if hw_device.hw_type == HWType.trezor:
                try:
                    fun = partial(trezorlib.btc.get_public_node, hw_device.client)
                    get_session_info_trezor(fun, hw_device)
                except trezorlib.exceptions.Cancelled:
                    raise CancelException()
                except trezorlib.exceptions.PinException as e:
                    raise HWPinException(e.args[1])

            elif hw_device.hw_type == HWType.keepkey:
                try:
                    get_session_info_trezor(hw_device.client.get_public_node, hw_device.client)
                except keepkeylib.client.PinException as e:
                    raise HWPinException(e.args[1])

            elif hw_device.hw_type == HWType.ledger_nano:
                path = dash_utils.get_default_bip32_base_path(self.dash_network)
                ap = ledger.get_address_and_pubkey(hw_device.client, path)
                self.set_base_info(path, ap['publicKey'])

        except CancelException:
            cancel_hw_operation(hw_device.client)
            self.__hw_devices.close_hw_client_for_device(hw_device)
            raise
        except Exception:
            # in the case of error close the session
            self.__hw_devices.close_hw_client_for_device(hw_device)
            raise

    def connect_hardware_wallet_main_th(self, reload_devices: bool = False) -> Optional[object]:
        """
        Connects to hardware wallet device if not connected before. It must be called from the main thread.
        :return: Reference to hw client or None if not connected.
        """
        ret = None
        if self.hw_client and self._app_config.hw_type is not None and self._app_config.hw_type != self.hw_type:
            self.disconnect_hardware_wallet()

        reload_devices_ = reload_devices
        if (not reload_devices_ and not self.__hw_devices.get_devices()) or not self.hw_client:
            # (re)load hardware wallet devices connected to the computer, if they haven't been loaded yet
            # or there is no session currently open to a hw device
            reload_devices_ = True

        self.__hw_devices.load_hw_devices(reload_devices_)

        if not self.hw_client:
            if len(self.__hw_devices.get_devices()) == 1:
                self.__hw_devices.select_device_by_index(0)
            elif len(self.__hw_devices.get_devices()) > 1:
                device = self.select_device()
                if not device:
                    raise CancelException('Cancelled')
            else:
                raise Exception("No hardware wallet device detected.")

            try:
                try:
                    self.initiate_hw_session()

                    if self.dash_network == 'TESTNET':
                        # check if Dash testnet is supported by this hardware wallet
                        found_testnet_support = False
                        if self.hw_type in (HWType.trezor, HWType.keepkey):
                            try:
                                path = dash_utils.get_default_bip32_base_path(self.dash_network)
                                path += "/0'/0/0"
                                path_n = dash_utils.bip32_path_string_to_n(path)
                                addr = self.hw_intf.get_address(self.hw_session, path_n, False)
                                if addr and dash_utils.validate_address(addr, self.dash_network):
                                    found_testnet_support = True
                            except Exception as e:
                                if str(e).find('Invalid coin name') < 0:
                                    logging.exception('Failed when looking for Dash testnet support')

                        elif self.hw_type == HWType.ledger_nano:
                            addr = self.hw_intf.get_address(self.hw_session,
                                                            dash_utils.get_default_bip32_path(self.dash_network))
                            if dash_utils.validate_address(addr, self.dash_network):
                                found_testnet_support = False

                        if not found_testnet_support:
                            url = get_note_url('DMT0002')
                            msg = f'Your hardware wallet device does not support Dash TESTNET ' \
                                  f'(<a href="{url}">see details</a>).'
                            try:
                                self.disconnect_hardware_wallet()
                            except Exception:
                                pass
                            self.signal_hw_connection_error(msg)
                            return
                    self.signal_hw_connected()

                except CancelException:
                    raise
                except Exception as e:
                    logging.exception('Exception while connecting hardware wallet')
                    try:
                        self.disconnect_hardware_wallet()
                    except Exception:
                        pass
                    self.signal_hw_connection_error(str(e))

                ret = self.hw_client
            except CancelException:
                raise
            except HWPinException as e:
                self.errorMsg(e.msg)
                if self.hw_client:
                    self.hw_client.clear_session()
            except OSError:
                self.errorMsg('Cannot open %s device.' % self.getHwName(), True)
            except Exception:
                if self.hw_client:
                    self.hw_client.init_device()
        else:
            ret = self.hw_client
        return ret

    def connect_hardware_wallet(self) -> Optional[object]:
        """
        Connects to hardware wallet device if not connected before.
        :return: Reference to hw client or None if not connected.
        """
        client = WndUtils.call_in_main_thread(self.connect_hardware_wallet_main_th)
        return client

    def disconnect_hardware_wallet(self) -> None:
        if self.hw_client:
            self.__hw_devices.close_hw_client_for_device(self.hw_device)
            # hw_intf.disconnect_hw(self.hw_client)
            # self.set_status_text2('<b>HW status:</b> idle', 'black')
            self.signal_hw_disconnected()


class HWDevicesListWdg(QWidget):
    sig_device_toggled = QtCore.pyqtSignal(HWDevice, bool)

    def __init__(self, parent, hw_devices: HWDevices):
        QWidget.__init__(self, parent=parent)
        self.hw_devices: HWDevices = hw_devices
        self.layout_main: Optional[QtWidgets] = None
        self.setupUi(self)

    def setupUi(self, dlg):
        dlg.setObjectName("HWDevicesListWdg")
        self.layout_main = QtWidgets.QVBoxLayout(dlg)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(6)
        self.layout_main.setObjectName("verticalLayout")
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_main.addItem(spacer)
        self.retranslateUi(dlg)
        QtCore.QMetaObject.connectSlotsByName(dlg)
        self.devices_to_ui()

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("SelectHwDeviceWdg", "Form"))

    def devices_to_ui(self):
        selected_device = self.hw_devices.get_selected_device()
        for ctrl in self.layout_main.children():
            if ctrl is QtWidgets.QRadioButton:
                del ctrl

        for dev in self.hw_devices.get_devices():
            ctrl = QtWidgets.QRadioButton(self)
            ctrl.setText(dev.get_description(True))
            self.layout_main.insertWidget(0, ctrl)
            ctrl.toggled.connect(partial(self.on_device_rb_toggled, dev))
            if selected_device == dev:
                ctrl.setChecked(True)

    def on_device_rb_toggled(self, hw_device: HWDevice, checked: bool):
        self.sig_device_toggled.emit(hw_device, checked)

    def update(self):
        try:
            pass
        except Exception as e:
            logging.exception(str(e))


class SelectHWDeviceDlg(QDialog):
    def __init__(self, parent, label: str, hw_devices: HWDevices):
        QDialog.__init__(self, parent=parent)
        self.hw_devices: HWDevices = hw_devices
        self.selected_hw_device: Optional[HWDevice] = None
        self.label = label
        self.lay_main: Optional[QtWidgets.QVBoxLayout] = None
        self.device_list_wdg: Optional[HWDevicesListWdg] = None
        self.lbl_title: Optional[QtWidgets.QLabel] = None
        self.btnbox_main: Optional[QtWidgets.QDialogButtonBox] = None
        self.setupUi(self)

    def setupUi(self, dialog):
        dialog.setObjectName("SelectHWDevice")
        self.lay_main = QtWidgets.QVBoxLayout(dialog)
        self.lay_main.setContentsMargins(12, 12, 12, 3)
        self.lay_main.setSpacing(12)
        self.lay_main.setObjectName("lay_main")
        self.device_list_wdg = HWDevicesListWdg(self.parent(), self.hw_devices)
        self.device_list_wdg.sig_device_toggled.connect(self.on_device_toggled)
        self.lbl_title = QtWidgets.QLabel(dialog)
        self.lbl_title.setText('<b>Select your hardware wallet device</b>')
        self.lay_main.addWidget(self.lbl_title)
        self.lay_main.addWidget(self.device_list_wdg)
        self.btnbox_main = QtWidgets.QDialogButtonBox(dialog)
        self.btnbox_main.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.btnbox_main.setObjectName("btn_main")
        self.lay_main.addWidget(self.btnbox_main)
        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        self.setFixedSize(self.sizeHint())
        self.update_buttons_state()

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle('Select hardware wallet device')

    @pyqtSlot(HWDevice, bool)
    def on_device_toggled(self, device: HWDevice, selected: bool):
        if not selected:
            if device == self.selected_hw_device:
                self.selected_hw_device = None
        else:
            self.selected_hw_device = device
        self.update_buttons_state()

    def update_buttons_state(self):
        b = self.btnbox_main.button(QtWidgets.QDialogButtonBox.Ok)
        if b:
            b.setEnabled(self.selected_hw_device is not None)

    def on_btn_main_accepted(self):
        if self.selected_hw_device is not None:
            self.accept()

    def on_btn_main_rejected(self):
        self.reject()
