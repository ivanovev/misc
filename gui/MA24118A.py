
from util.mainwnd import control_cb, monitor_cb
from collections import OrderedDict as OD
from util import Data, dev_serial_io_cb, alarm_trace_cb
from util.columns import *

def get_menu(dev):
    return OD([('Control', control_cb), ('Monitor', monitor_cb)])

def columns():
    return get_columns([c_serial])

def get_mntr(dev):
    mntr = Data('mntr', send=True, io_cb=dev_serial_io_cb)
    mntr.add('pwr', wdgt='entry', state='readonly', msg='current power reading (in dBm)')
    mntr.add('temp', wdgt='entry', state='readonly', msg='current temperature reading')
    return mntr

def get_ctrl(dev):
    ctrl = Data('ctrl', send=True, io_cb=dev_serial_io_cb)
    ctrl.add('freq', label='Frequency, GHz', wdgt='spin', value=Data.spn(0.010, 18, 0.0001))
    ctrl.add('chold', label='Sensor state', wdgt='radio', value=OD([('Run', '0'), ('Hold', '1')]))
    return ctrl

