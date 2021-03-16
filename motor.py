import time

from CONSTANTS import *
from loggers import *
import RPiToSTM


class Motor:

    MOTOR_OBJ_LST = []

    def __init__(self):
        self.motor_info = {
            'number': Motor.MOTOR_OBJ_LST.__len__(),
            'position': 0,
            'clockwise': True,

            'tmp': 0,
        }

        Motor.MOTOR_OBJ_LST.append(self.motor_info)

    @classmethod
    def get_motor_list(cls):
        return sorted(cls.MOTOR_OBJ_LST, key=lambda motor: motor['number'])

    def get_pos(self):
        return self.motor_info['position']

    def set_pos(self, position):
        self.motor_info['position'] = position

    def upd_pos(self, value):
        self.motor_info['position'] += value
        # if sign == '+':
        #     self.motor_info['position'] += value
        # if sign == '-':
        #     self.motor_info['position'] -= value

    def get_num(self):
        return self.motor_info['number']

    def set_mtr_dir(self, sign):
        mtr = self.get_num()

        if not mtr:
            RPiToSTM.cmd['dir'](mtr, 'CW' if sign == '+' else 'CCW')
        else:
            RPiToSTM.cmd['dir'](mtr, 'CCW' if sign == '+' else 'CW')

        # RPiToSTM.cmd['dir'](mtr, 'CW' if sign == '+' and mtr else 'CCW')
        # RPiToSTM.cmd['dir'](mtr, 'CCW' if sign == '-' and mtr else 'CW')

    def mov_mtr(self, stps_amt, stps_tim):
        logger['STP_INFO'].info(f'MOT NO: {self.get_num()} | STEPS AMOUNT = {stps_amt}[steps]')
        logger['TIM_INFO'].info(f'MOT NO: {self.get_num()} | STEPS TIME   = {stps_tim}[seconds]')
        sign = '+' if stps_amt > 0 else '-'

        # FULLY SOFTWARE TESTING
        if MODEL == 'SIL':
            for stp in range(abs(stps_amt)):                          # Verify if not change to other loop
                self.upd_pos(STP_DST)

                if not stp % 10:
                    logger['P_INF'].info(f'MOT NO: {self.get_num()}, {self.get_pos()}')

                if DEBUG:
                    time.sleep(abs(stps_tim / stps_amt))
                    continue
                time.sleep(abs(stps_tim / stps_amt))

        # HARDWARE TESTING
        if MODEL == 'HIL':
            RPiToSTM.cmd['enb'](self.get_num())
            RPiToSTM.cmd['div'](self.get_num(), GEAR)
            self.set_mtr_dir(sign)
            RPiToSTM.cmd['tim'](self.get_num(), int(stps_tim * 1000))
            RPiToSTM.cmd['amt'](self.get_num(), abs(stps_amt))
            RPiToSTM.cmd['mov'](self.get_num(), 1)
            # self.set_pos(stps_amt * STP_DST)
            self.upd_pos(stps_amt)

            # print(f'distnace: {stps_amt * STP_DST}')

    @classmethod
    def dis_mtrs(cls):
        RPiToSTM.cmd['dsb'](0)
        RPiToSTM.cmd['dsb'](1)

