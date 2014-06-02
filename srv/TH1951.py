
from util.serial import query_serial

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
        ret = '%.3f' % f
    return ret

