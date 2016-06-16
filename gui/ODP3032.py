
from collections import OrderedDict as OD

from util.columns import *
from util import Data, control_cb, dev_io_cb

def odp_fmt_cb(val, read=True):
    if read:
        v = float(val)
        return '%g' % v
    else:
        return val

def common_fmt_cb(val, read=True):
    if read and val == 'DUALCHANNEL':
        return 'DOUBLE'
    else:
        return val

def columns():
    return get_columns()

def get_menu(dev):
    return OD([('Control', control_cb)])

def reset_cb(ctrl):
    ctrl.cmdio('ODP3032.reset')

def write_cb(ctrl):
    ctrl.write_cb()

def read_cb(ctrl):
    ctrl.read_cb()

def get_ctrl(dev):
    ctrl_buttons = OD([('Reset', reset_cb), ('Read', read_cb), ('Write', write_cb)])
    data = Data(buttons=ctrl_buttons, io_cb=dev_io_cb)
    data.add_page('Mode', send=True)
    data.add('COMMON', label='Mode', wdgt='combo', state='readonly', value=['INDEPENDENT', 'PARALLEL', 'SERIES', 'DOUBLE'], fmt_cb=common_fmt_cb)
    data.add_page('Independent', send=True)
    data.add('SCH1V', label='Channel1, V', wdgt='spin', value=Data.spn(0,30,.01), fmt_cb=odp_fmt_cb)
    data.add('SCH1C', label='Channel1, A', wdgt='spin', value=Data.spn(0,3,.01), fmt_cb=odp_fmt_cb)
    data.add('SW1', label='Output1 enable', wdgt='combo', state='readonly', value=OD([('ON','0'), ('OFF','1')]))
    data.add('SCH2V', label='Channel2, V', wdgt='spin', value=Data.spn(0,30,.01), fmt_cb=odp_fmt_cb)
    data.add('SCH2C', label='Channel2, A', wdgt='spin', value=Data.spn(0,3,.01), fmt_cb=odp_fmt_cb)
    data.add('SW2', label='Output2 enable', wdgt='combo', state='readonly', value=OD([('ON','0'), ('OFF','1')]))
    data.add_page('Parallel', send=True)
    data.add('SPARAV', label='Output, V', wdgt='spin', value=Data.spn(0,30,.01), fmt_cb=odp_fmt_cb)
    data.add('SPARAC', label='Output, A', wdgt='spin', value=Data.spn(0,6,.01), fmt_cb=odp_fmt_cb)
    data.add('SW1', label='Output enable', wdgt='combo', state='readonly', value=OD([('ON','0'), ('OFF','1')]))
    data.add_page('Series', send=True)
    data.add('SSERIV', label='Output, V', wdgt='spin', value=Data.spn(0,60,.01), fmt_cb=odp_fmt_cb)
    data.add('SSERIC', label='Output, A', wdgt='spin', value=Data.spn(0,3,.01), fmt_cb=odp_fmt_cb)
    data.add('SW1', label='Output enable', wdgt='combo', state='readonly', value=OD([('ON','0'), ('OFF','1')]))
    data.add_page('PlusMinus', send=True)
    data.add('SDUAL1V', label='Output1, V', wdgt='spin', value=Data.spn(0,30,.01), fmt_cb=odp_fmt_cb)
    data.add('SDUAL1C', label='Output1, A', wdgt='spin', value=Data.spn(0,3,.01), fmt_cb=odp_fmt_cb)
    data.add('SDUAL2V', label='Output2, V', wdgt='spin', value=Data.spn(0,30,.01), fmt_cb=odp_fmt_cb)
    data.add('SDUAL2C', label='Output2, A', wdgt='spin', value=Data.spn(0,3,.01), fmt_cb=odp_fmt_cb)
    data.add('SW1', label='Output enable', wdgt='combo', state='readonly', value=OD([('ON','0'), ('OFF','1')]))
    return data
