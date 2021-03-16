import sys
import time
import threading

from math_calc import MathCalc
from motor import Motor
from extruder import Extruder
from loggers import *
from CONSTANTS import *
from trace_manager import TraceManager


class Carriage:

    DATA = {
        'INITIALIZED': False,                   # First run and calibration should change it to True

        'HYP_L': 0,
        'HYP_R': 0,

        'CUR_POS_DIST_S': {'X': 0, 'Y': 0},     # Distance in STEPS
        'CUR_POS_DIST_M': {'X': 0, 'Y': 0},     # Distance in MILLIMETERS

        'STPS_AMT': {'L': 0, 'R': 0},
        'STPS_TIM': 0
    }

    MOT_L = Motor()
    MOT_R = Motor()

    def __class_getitem__(cls, item):
        return cls.DATA[item]

    @classmethod
    def dis_mtrs(cls):
        Motor.dis_mtrs()

    @classmethod
    def init_calibration(cls):
        if START_POINT == 'middle':
            cls.DATA['HYP_L'] = MathCalc.get_hypotenuse(WALL_X / 2, WALL_Y)
            cls.DATA['HYP_R'] = MathCalc.get_hypotenuse(WALL_X / 2, WALL_Y)

        if START_POINT == 'begin':
            cls.DATA['HYP_L'] = WALL_Y
            cls.DATA['HYP_R'] = MathCalc.get_hypotenuse(WALL_X, WALL_Y)

        cls.DATA['INITIALIZED'] = True

    @classmethod
    def set_position(cls, mes: str, x_set: int, y_set: int, stps_l: int, stps_r: int):
        if mes == 'stp':
            r_pos_x, r_pos_y = TraceManager.steps_to_xy(stps_l + 1, stps_r + 1)

            cls.DATA['CUR_POS_DIST_S'] = {'X': r_pos_x, 'Y': r_pos_y}

            logger['P_INF'].info(f'I should be in position X:{x_set}[mm]|{x_set / STP_DST}[stp],'
                                 f' Y:{y_set}[mm]|{y_set / STP_DST}[stp]')

            logger['P_INF'].info(f'I really am in position X: {r_pos_x * STP_DST}[mm]|{r_pos_x}[stp], '
                                 f'Y: {r_pos_y * STP_DST}[mm]|{r_pos_y}[stp]\n')

    @classmethod
    def get_position(cls, mes: str):
        if mes == 'stp':
            return cls.DATA['CUR_POS_DIST_S'], cls.DATA['CUR_POS_DIST_M']

    @classmethod
    def stps_to_move(cls, o_hyp, n_hyp):
        hyp = abs(o_hyp - n_hyp)
        return int(MathCalc.steps_amt(hyp))

    @classmethod
    def start_motor_thread(cls):
        if DEV_MOTOR_AMT == 1:
            mot_l_thr = threading.Thread(target=cls.MOT_L.mov_mtr, args=(cls.DATA['STPS_AMT']['L'], cls.DATA['STPS_TIM']))
            threads = [mot_l_thr]
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]

        if DEV_MOTOR_AMT == 2:
            mot_l_thr = threading.Thread(target=cls.MOT_L.mov_mtr, args=(cls.DATA['STPS_AMT']['L'], cls.DATA['STPS_TIM']))
            mot_r_thr = threading.Thread(target=cls.MOT_R.mov_mtr, args=(cls.DATA['STPS_AMT']['R'], cls.DATA['STPS_TIM']))
            threads = [mot_l_thr, mot_r_thr]
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]

    @classmethod
    def move_to_point(cls, **kwargs):
        x_lt, x_rt, y_lo = 0, 0, 0

        if kwargs['G'] == 80:
            cls.init_calibration()      # Calculate start point hypotenuses, TBD change format of calling that kind fun

            stps_l = int(round(MathCalc.steps_amt(cls.DATA['HYP_L'])))
            stps_r = int(round(MathCalc.steps_amt(cls.DATA['HYP_R'])))

            if START_POINT == 'begin':
                cls.set_position('stp', 0, 0, stps_l, stps_r)
            if START_POINT == 'middle':
                cls.set_position('stp', 500, 0, stps_l, stps_r)

            cls.MOT_L.set_pos(stps_l)
            cls.MOT_R.set_pos(stps_r)
            return 0

        if kwargs['X'] > -1:
            # if START_POINT == 'middle':
            #     x_lt = WALL_X / 2 - kwargs['X']
            #     x_rt = WALL_X / 2 + kwargs['X']
            #
            # if START_POINT == 'begin':
            x_lt = kwargs['X']
            x_rt = WALL_X - kwargs['X']

        if kwargs['Y'] > -1:
            y_lo = WALL_Y - kwargs['Y']

        if kwargs['E'] > -1:
            Extruder.extrude_marker(int(kwargs['E']))
            print(kwargs['E'])

        else:
            sys.exit('Value of GCODE can not be negative')

        hyp_diff_l = abs(MathCalc.get_hypotenuse(x_lt, y_lo)) - cls.DATA['HYP_L']
        hyp_diff_r = abs(MathCalc.get_hypotenuse(x_rt, y_lo)) - cls.DATA['HYP_R']

        # Hypotenuses calc (output value in the same unit as WALL_X and WALL_Y -> mm for now)
        cls.DATA['HYP_L'] = abs(MathCalc.get_hypotenuse(x_lt, y_lo))
        cls.DATA['HYP_R'] = abs(MathCalc.get_hypotenuse(x_rt, y_lo))

        cls.DATA['STPS_AMT']['L'] = int(round(MathCalc.steps_amt(hyp_diff_l)))
        cls.DATA['STPS_AMT']['R'] = int(round(MathCalc.steps_amt(hyp_diff_r)))

        logger['P_INF'].info(f"I have to move: "
                             f"MOT_L: {hyp_diff_l}[mm]|{cls.DATA['STPS_AMT']['L']}[steps] && "
                             f"MOT_R: {hyp_diff_r}[mm]|{cls.DATA['STPS_AMT']['R']}[steps]\n")

        # Steps time calc
        cls.DATA['STPS_TIM'] = max(MathCalc.steps_tim(abs(amt)) for amt in cls.DATA['STPS_AMT'].values())

        # FULLY SOFTWARE TESTING LOW LEVEL FUNCTIONS
        if MODEL == 'SIL':
            cls.start_motor_thread()

        if MODEL == 'HIL':
            cls.MOT_L.mov_mtr(cls.DATA['STPS_AMT']['L'], cls.DATA['STPS_TIM'])
            cls.MOT_R.mov_mtr(cls.DATA['STPS_AMT']['R'], cls.DATA['STPS_TIM'])
            time.sleep(cls.DATA['STPS_TIM'])

        print(' ')
        logger['P_INF'].info(f'END POSITIONS FOR: @MOT_L -> {cls.MOT_L.get_pos()}[stp] && '
                             f'@MOT_R -> {cls.MOT_R.get_pos()}[stp]\n')

        cls.set_position('stp', kwargs['X'], kwargs['Y'], cls.MOT_L.get_pos(), cls.MOT_R.get_pos())
        return 0
