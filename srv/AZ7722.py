
from serial import Serial
from time import sleep
from threading import Thread

azth = None
azport = ''
azco2 = ''
aztemp = ''
azrh = ''

def az_parse_data(s):
    global azco2, aztemp, azrh
    s = s.strip()
    data = s.split(':')
    if 'RH' in data:
        return
    for i in data:
        if i[0] == 'C':
            azco2 = i[1:]
            azco2 = azco2.replace('ppm', '')
        elif i[0] == 'T':
            aztemp = i[1:]
            aztemp = aztemp.replace('C', '')
        elif i[0] == 'H':
            azrh = i[1:]
            azrh = azrh.replace('%', '')
    #print(azco2, aztemp, azrh)

def az_listen_thread_func(port):
    global azth, azport
    if port[:3] != 'COM':
        if port.find('/dev/') == -1:
            port = '/dev/' + port
    try:
        ser = Serial(port, 9600, 8, 'N', 1, timeout=2)
        ser.setDTR(1)
        ser.setRTS(1)
        s = ''
        while azth:
            ch = ser.read()
            if len(ch):
                chr0 = chr(ch[0])
                if chr0 == '\r':
                    az_parse_data(s)
                    s = ''
                else:
                    s += chr0
    except:
        azth = None
    print('azthread stop')

def AZ7722_listen(port='ttyUSB0'):
    global azth, azport
    if port == '':
        return azport
    if azth:
        return azport
    azth = Thread(target=az_listen_thread_func, args=(port,))
    azth.start()
    azport = port
    for i in range(0, 10):
        sleep(.1)
        if azco2:
            break
    return azport

def AZ7722_stop():
    global azth, azport
    if azth:
        print('az stop')
        a = azth
        azth = None
        azco2 = ''
        a.join()
    return azport

def AZ7722_CO2(port='ttyUSB0'):
    """
    Fetch latest reading
    @param port - serial port
    @return value
    """
    global azth, azco2
    if not azth:
        AZ7722_listen(port)
    return azco2

def AZ7722_TEMP(port='ttyUSB0'):
    """
    Fetch latest reading
    @param port - serial port
    @return value
    """
    global azth, aztemp
    if not azth:
        AZ7722_listen(port)
    return aztemp

def AZ7722_RH(port='ttyUSB0'):
    """
    Fetch latest reading
    @param port - serial port
    @return value
    """
    global azth, azrh
    if not azth:
        AZ7722_listen(port)
    return azrh

