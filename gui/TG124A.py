
from collections import OrderedDict as OD

from util import Data, control_cb, dev_io_cb
from util.columns import *

def reset_cb(ctrl):
    ctrl.cmdio('TG124A.reset')

def write_cb(ctrl):
    ctrl.write_cb()

def get_menu(dev):
    return OD([('Control', control_cb)])

def columns():
    return get_columns()

def get_ctrl(dev):
    ctrl_buttons = OD([('Reset', reset_cb), ('Write', write_cb)])
    data = Data(buttons=ctrl_buttons, io_cb=dev_io_cb)
    data.add_page('Generator', send=True)
    data.add('freq', label='Frequency, MHz', wdgt='spin', value={'min':0.1, 'max':12400, 'step':0.1}, text='1451')
    data.add('amp', label='Amplitude, dBm', wdgt='spin', value={'min':-40, 'max':-6, 'step':0.5}, text='-40')
    return data

