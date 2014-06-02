
import usbtmc
from ..gui.DG1022U import freq_fmt_cb
from time import sleep

def get_instr():
    try:
        if hasattr(get_instr, 'instr'):
            return get_instr.instr
        instr = usbtmc.Instrument(0x400, 0x9C4)
        sleep(.3)
        get_instr.instr = instr
        return instr
    except:
        pass

def usbtmc_io(cmd, read):
    instr = get_instr()
    if instr:
        sleep(.1)
        instr.write(cmd)
        sleep(.1)
        if read:
            return instr.read()
    return ''

'''
def usbtmc_io(cmd, read):
    f = open('/dev/usbtmc0', 'w')
    f.write(cmd + '\n')
    f.close()
    if not read:
        return ''
    sleep(.3)
    f = open('/dev/usbtmc0', 'r')
    ret = f.readline()
    f.close()
    ret = ret.strip()
    return ret
'''

def DG1022U_cmd(cmd, *args):
    """
    DG1022U input/output
    """
    if len(args):
        cmd += ' ' + ' '.join(args)
    read = cmd[-1] == '?'
    val = cmd.split(' ')[-1]
    ret = usbtmc_io(cmd, read)
    return ret if read else val

def DG1022U_qfreq(freq):
    """
    DG1022U quadrature freq
    @param freq - Frequency, kHz [0.001..25000]
    @return freq
    """
    if type(freq) == int:
        freq = '%d' % freq;
    elif type(freq) == float:
        freq = '%f' % freq;
    freq = freq_fmt_cb(freq, False)
    cmds = ['FREQ %s' % freq, 'PHAS 0', 'FUNC SIN', 'SYST:BEEP:STAT OFF']
    cmds += ['COUP ON', 'COUP:CHANNC 1>2', 'COUP:BASE:CH1', 'COUP:PHASEDEV 90']
    for c in cmds:
        print(c)
        usbtmc_io(c, False)
        sleep(.3)
    return freq

def main():
    print(usbtmc_io('*IDN?'))

if __name__ == '__main__':
    main()

