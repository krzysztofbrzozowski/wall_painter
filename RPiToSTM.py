import sys
import platform

from serial_encoder import *

if platform.system() == 'Darwin':
    s_encoder = SerialEncoder('/dev/cu.usbserial-FT9JARY8', 115200)
if platform.system() == 'Linux':
    s_encoder = SerialEncoder('/dev/ttyS0', 115200)

print('Hi I am inited')


def verity_check(value):
    if 0 > value:
        sys.exit('Serial argument value can not be negative')
    if not isinstance(value, int):
        sys.exit('Serial argument value has to be integer')


# MOTOR ENABLE
def mtr_enb_cmd(mtr):
    verity_check(mtr)
    s_encoder.encode(0x80 | mtr << 5)


# MOTOR DISABLE
def mtr_dsb_cmd(mtr):
    verity_check(mtr)
    s_encoder.encode(0x81 | mtr << 5)


# STEP DIVISION
def mtr_stp_div(mtr, stp_div):
    verity_check(stp_div)
    s_encoder.encode(0x90 | mtr << 5 | stp_div)


# STEPS DIRECTION
def mtr_stps_dir(mtr, stps_dir):
    if stps_dir == 'CW':
        s_encoder.encode(0x88 | mtr << 5)
    elif stps_dir == 'CCW':
        s_encoder.encode(0x89 | mtr << 5)


# STEPS TIME
def mtr_stps_tim(mtr, stps_tim):
    verity_check(stps_tim)
    s_encoder.encode(0x85 | mtr << 5, int(stps_tim / 20))


# STEPS AMOUNT
def mtr_stps_amt(mtr, stps_amt):
    verity_check(stps_amt)
    s_encoder.encode(0x86 | mtr << 5, stps_amt)


# MOTOR START MOVING
def mtr_mov_cmd(mtr, mov_cmd):
    if mov_cmd:
        s_encoder.encode(mtr + 1)


# EXTRUDE MARKER
def ext_mkr_cmd(percentage):
    # if percentage > -1:
    s_encoder.encode(0x83, 100 - percentage)


# SEND RAW CMD
def raw_val_cmd(raw_cmd):
    s_encoder.encode(raw_cmd)


cmd = {
    'enb': mtr_enb_cmd,
    'dsb': mtr_dsb_cmd,
    'div': mtr_stp_div,
    'dir': mtr_stps_dir,
    'tim': mtr_stps_tim,
    'amt': mtr_stps_amt,
    'mov': mtr_mov_cmd,
    'ext': ext_mkr_cmd,
    'raw': raw_val_cmd
}
