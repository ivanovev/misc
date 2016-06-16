
from collections import OrderedDict as OD
from copy import deepcopy

from tkinter import messagebox

from util.columns import *
from util import Data, control_cb

def dg_io_cb(dev, cmd):
    l = len(cmd.split())
    cmd = ' '.join(['DG1022U.cmd', cmd])
    if l == 1:
        return cmd + '?'
    else:
        return cmd

def func_fmt_cb(val, read=True):
    if read:
        return val.split(':')[-1]
    else:
        return val

def freq_fmt_cb(val, read=True):
    if read:
        val = val.split(':')[-1]
        val = float(val)/1e3
        return '%.3f' % val
    else:
        val = float(val)*1e3
        return '%d' % val

def volt_fmt_cb(val, read=True):
    if read:
        val = float(val.split(':')[-1])
        return '%.1f' % val
    else:
        return val

def info_fmt_cb(val, read=True):
    if read:
        vv = val.split(',')
        ii = ['Manufacturer', 'Model', 'Serial number', 'Model number']
        ii = [i + ': ' for i in ii]
        if len(vv) == len(ii):
            ll = [i for t in zip(ii,vv) for i in t]
            l = '\n'.join(ll)
            messagebox.showinfo(title='Info', message=l)

def columns():
    return get_columns()

def get_menu(dev):
    return OD([('Control', control_cb)])

def get_ctrl(dev):
    data = Data(io_cb=dg_io_cb)
    data.add_page('Channel 1', send=True)
    data.add('FUNC', label='Function (select SIN)', wdgt='combo', state='readonly', value=['SIN','SQU','RAMP','PULS','NOIS','DC','USER'], fmt_cb=func_fmt_cb)
    data.add('FREQ', label='Frequency, kHz', wdgt='spin', value={'min':0.001, 'max':25000, 'step':0.001}, fmt_cb=freq_fmt_cb)
    data.add('VOLT:UNIT', label='Voltage units (select VPP)', wdgt='combo', state='readonly', value=['VPP','VRMS','DBM'], fmt_cb=func_fmt_cb)
    data.add('VOLT', label='Voltage, V', wdgt='spin', value={'min':0.2, 'max':5, 'step':0.1}, text='0.2', fmt_cb=volt_fmt_cb)
    data.add('VOLT:OFFS', label='Voltage offset, V', wdgt='spin', value={'min':0, 'max':5, 'step':0.1}, fmt_cb=volt_fmt_cb)
    data.add('PHAS', label='Phase, deg', wdgt='spin', value={'min':-180, 'max':180, 'step':1})
    data.add('OUTP', label='Output enable', wdgt='combo', state='readonly', value=['ON', 'OFF'])

    data.add_page('Channel 2', cmds=OD((k+':CH2',deepcopy(v)) for k,v in data.cmds.items()))
    data.add_page('DUAL')
    data.add('qfreq', label='Frequency, kHz', wdgt='spin', value={'min':0.001, 'max':25000, 'step':0.001}, send=True)
    data.add('PHAS', label='PHASE:CH2 - PHASE:CH1 = 90', send=False)

    return data

