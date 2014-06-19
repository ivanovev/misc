
from util.serial import query_serial
from time import time

def TH1951_fetch(port='ttyUSB1'):
    """
    Fetch latest reading
    @param port - serial port
    @return value
    """
    ret = query_serial(port, 9600, 8, 'N', 1, 'FETC?\r', '\n')
    ret = ret.strip()
    if ret:
        f = float(ret)
        ret = '%.5f' % f
    return ret

tprev = time()
data = 0
dt = 10
def TH1951_diff(port='ttyUSB1'):
    global tprev, data, dt
    ret = TH1951_fetch(port)
    t1 = time()
    dt1 = t1 - tprev
    tprev = t1
    if dt1 > dt:
        data = ret
        return '0'
    ret1 = '%.5f' % (float(ret) - float(data))
    print(ret1, data, ret)
    data = ret
    return ret1

