import sys

from serial_encoder import *


def verity_check(value):
    if 0 > value:
        sys.exit('Serial argument value can not be negative')
    if not isinstance(value, int):
        sys.exit('Serial argument value has to be integer')


class RPiToSTM:
    s_encoder = SerialEncoder('/dev/ttyS0', 115200)

    # MOTOR ENABLE
    @classmethod
    def mtr_enb_cmd(cls, mtr, enb_cmd):
        verity_check(enb_cmd)
        if enb_cmd:
            cls.s_encoder.encode(0x80 | mtr << 5)
        elif not enb_cmd:
            cls.s_encoder.encode(0x81 | mtr << 5)

    # STEP DIVISION
    @classmethod
    def mtr_stp_div(cls, mtr, stp_div):
        verity_check(stp_div)
        cls.s_encoder.encode(0x90 | mtr << 5 | stp_div)

    # STEPS DIRECTION
    @classmethod
    def mtr_stps_dir(cls, mtr, stps_dir):
        if stps_dir == 'CW':
            cls.s_encoder.encode(0x88 | mtr << 5)
        elif stps_dir == 'CCW':
            cls.s_encoder.encode(0x89 | mtr << 5)

    # STEPS TIME
    @classmethod
    def mtr_stps_tim(cls, mtr, stps_tim):
        verity_check(stps_tim)
        cls.s_encoder.encode(0x85 | mtr << 5, int(stps_tim / 15))

    # STEPS AMOUNT
    @classmethod
    def mtr_stps_amt(cls, mtr, stps_amt):
        verity_check(stps_amt)
        cls.s_encoder.encode(0x86 | mtr << 5, stps_amt)

    @classmethod
    def mtr_mov_cmd(cls, mtr, mov_cmd):
        if mov_cmd:
            cls.s_encoder.encode(mtr + 1)

    rpi_stm_send_cmd = {
        'ENB': mtr_enb_cmd,
        'DIV': mtr_stp_div,
        'DIR': mtr_stps_dir,
        'TIM': mtr_stps_tim,
        'AMT': mtr_stps_amt,
        'MOV': mtr_mov_cmd
    }
