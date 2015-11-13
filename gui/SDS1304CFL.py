
from collections import OrderedDict as OD

from util import process_cb
from util.columns import *

from ..srv.SDS1304CFL import get_data
from ..tools import Scdp

def columns():
    return get_columns()

def startup_cb(apps, mode, dev):
    if mode == 'scdp':
        return Scdp(dev=dev, get_data=lambda: get_data(dispose_dev=True))

def get_menu(dev):
    menu = OD()
    menu['Screenshot'] = lambda dev: process_cb('scdp', dev)
    return menu

