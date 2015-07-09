
from util.serial import query_serial

def MA24118A_cmd(port='ttyACM0', cmd='IDN?'):
    """
    Send cmd, return reply
    @param port - serial port
    @param cmd - command
    @return reply
    """
    cmd += '\n'
    ret = query_serial(port, 9600, 8, 'N', 1, cmd, endstr='\n', timeout=1)
    if ret:
        ret = ret.strip()
    return ret

def MA24118A_freq(port='ttyACM0', freq=''):
    """
    Fetch latest reading
    @param port - serial port
    @param freq - current calibration factor frequency
    """
    if freq:
        return MA24118A_cmd(port, 'FREQ ' + freq)
    else:
        ret = MA24118A_cmd(port, 'FREQ?')
        if ret:
            ret = '%g' % float(ret)
        return ret

def MA24118A_chold(port='ttyACM0', chold=''):
    """
    Fetch latest reading
    @param port - serial port
    @param chold - 0 - Run, 1 - Hold
    """
    if chold:
        return MA24118A_cmd(port, 'CHOLD ' + chold)
    else:
        return MA24118A_cmd(port, 'CHOLD?')

def MA24118A_pwr(port='ttyACM0'):
    """
    Fetch latest reading
    @param port - serial port
    @return current power reading (in dBm)
    """
    ret = MA24118A_cmd(port, 'PWR?')
    if ret:
        ret = '%.1f' % float(ret)
    return ret

def MA24118A_temp(port='ttyACM0'):
    """
    Fetch latest reading
    @param port - serial port
    @return current temperature reading
    """
    ret = MA24118A_cmd(port, 'TMP?')
    if ret:
        ret = '%.1f' % float(ret)
    return ret

