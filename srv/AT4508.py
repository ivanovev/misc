
from util.serial import query_serial
from util.cache import CachedDict

def AT4508_cmd(port='ttyUSB0', cmd='IDN?'):
    """
    Send cmd, return reply
    @param port - serial port
    @param cmd - command
    @return reply
    """
    cmd += '\n'
    ret = query_serial(port, 9600, 8, 'N', 1, cmd, '\n')
    ret = ret.strip()
    ret = ret.strip(',')
    return ret

def AT4508_fetch(port='ttyUSB0'):
    """
    Fetch latest reading
    @param port - serial port
    @return list of temperatures, space separated
    """
    ret = AT4508_fetch.cd.get(lambda: AT4508_cmd(port, 'FETCh?'), port, 'fetch', duration=5)
    if ret:
        rr = ret.split(',')
        out = []
        for r in rr:
            out.append('%.1f' % float(r))
        ret = ' '.join(out)
    return ret
AT4508_fetch.cd = CachedDict()

def AT4508_CHn(port='COM5', ch='1'):
    ch = int(ch)
    if ch < 1: ch = 1
    if ch > 8: ch = 8
    ret = AT4508_fetch(port)
    if ret:
        rr = ret.split(' ')
        ret = rr[ch - 1]
        if ret == '-100000.0':
            ret = 'N/A'
        return ret
    
def AT4508_CH1(port='COM5'):
    return AT4508_CHn(port, '1')

def AT4508_CH2(port='COM5'):
    return AT4508_CHn(port, '2')

def AT4508_CH3(port='COM5'):
    return AT4508_CHn(port, '3')

def AT4508_CH4(port='COM5'):
    return AT4508_CHn(port, '4')

def AT4508_CH5(port='COM5'):
    return AT4508_CHn(port, '5')

def AT4508_CH6(port='COM5'):
    return AT4508_CHn(port, '6')

def AT4508_CH7(port='COM5'):
    return AT4508_CHn(port, '7')

def AT4508_CH8(port='COM5'):
    return AT4508_CHn(port, '8')

