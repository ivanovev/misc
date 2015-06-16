
from util.serial import query_serial

def AT4508_cmd(port='ttyUSB0', cmd='IDN?'):
    """
    Send cmd, return reply
    @param port - serial port
    @param cmd - command
    @return reply
    """
    cmd += '\n'
    return query_serial(port, 9600, 8, 'N', 1, cmd, '\n')

def AT4508_fetch(port='ttyUSB0'):
    """
    Fetch latest reading
    @param port - serial port
    @return list of temperatures, space separated
    """
    ret = AT4508_cmd(port, 'FETCh?')
    ret = ret.strip()
    ret = ret.strip(',')
    if ret:
        rr = ret.split(',')
        out = []
        for r in rr:
            out.append('%.1f' % float(r))
        ret = ' '.join(out)
    return ret

