def OpenRelay(channel):
    mybytes0=0x01
    mybytes1=0x05
    mybytes2=0x00
    mybytes4=0xff
    mybytes5=0x00
    if channel==0:
        mybytes3=0x00
        mybytes6=0x8c
        mybytes7=0x3a
    elif channel==1:
        mybytes3=0x01
        mybytes6=0xdd
        mybytes7=0xfa
    elif channel==2:
        mybytes3=0x02
        mybytes6=0x2d
        mybytes7=0xfa
    elif channel==3:
        mybytes3=0x03
        mybytes6=0x7c
        mybytes7=0x3a
    elif channel==4:
        mybytes3=0x04
        mybytes6=0xcd
        mybytes7=0xfb
    elif channel==5:
        mybytes3=0x05
        mybytes6=0x9c
        mybytes7=0x3b
    elif channel==6:
        mybytes3=0x06
        mybytes6=0x6c
        mybytes7=0x3b
    elif channel==7:
        mybytes3=0x07
        mybytes6=0x3d
        mybytes7=0xfb
    return [mybytes0,mybytes1,mybytes2,mybytes3,mybytes4,mybytes5,mybytes6,mybytes7]
def CloseRelay(channel):
    mybytes0=0x01
    mybytes1=0x05
    mybytes2=0x00
    mybytes4=0x00
    mybytes5=0x00
    if channel==0:
        mybytes3=0x00
        mybytes6=0xcd
        mybytes7=0xca
    elif channel==1:
        mybytes3=0x01
        mybytes6=0x9c
        mybytes7=0x0a
    elif channel==2:
        mybytes3=0x02
        mybytes6=0x6c
        mybytes7=0x0a
    elif channel==3:
        mybytes3=0x03
        mybytes6=0x3d
        mybytes7=0xca
    elif channel==4:
        mybytes3=0x04
        mybytes6=0x8c
        mybytes7=0x0b
    elif channel==5:
        mybytes3=0x05
        mybytes6=0xdd
        mybytes7=0xcb
    elif channel==6:
        mybytes3=0x06
        mybytes6=0x2d
        mybytes7=0xcb
    elif channel==7:
        mybytes3=0x07
        mybytes6=0x7c
        mybytes7=0x0b
    return [mybytes0,mybytes1,mybytes2,mybytes3,mybytes4,mybytes5,mybytes6,mybytes7]
def GetStatus(channel=8):
    mybytes0=0x01
    mybytes1=0x01
    mybytes2=0x00
    mybytes4=0x00
    mybytes5=0x01
    if channel==0:
        mybytes3=0x00
        mybytes6=0xfd
        mybytes7=0xca
    elif channel==1:
        mybytes3=0x01
        mybytes6=0xac
        mybytes7=0x0a
    elif channel==2:
        mybytes3=0x02
        mybytes6=0x5c
        mybytes7=0x0a
    elif channel==3:
        mybytes3=0x03
        mybytes6=0x0d
        mybytes7=0xca
    elif channel==4:
        mybytes3=0x04
        mybytes6=0xbc
        mybytes7=0x0b
    elif channel==5:
        mybytes3=0x05
        mybytes6=0xed
        mybytes7=0xcb
    elif channel==6:
        mybytes3=0x06
        mybytes6=0x1d
        mybytes7=0xcb
    elif channel==7:
        mybytes3=0x07
        mybytes6=0x4c
        mybytes7=0x0b
    elif channel==8:
        mybytes3=0x00
        mybytes5=0x08
        mybytes6=0x3d
        mybytes7=0xcc
    return [mybytes0,mybytes1,mybytes2,mybytes3,mybytes4,mybytes5,mybytes6,mybytes7]
