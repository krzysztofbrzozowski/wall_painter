from CONSTANTS import *
from math_calc import MathCalc


class TraceManager:

    @staticmethod
    def steps_to_xy(hyp_l_s: int, hyp_r_s: int):
        # height = MathCalc.herons_calc(hyp_l, hyp_r, WALL_X * STP_MUL_CONST)
        height = MathCalc.herons_calc(hyp_l_s, hyp_r_s, MathCalc.steps_amt(WALL_X))
        r_pos_y = MathCalc.steps_amt(WALL_X) - height
        r_pos_x = MathCalc.pythagoras_calc_hh(hyp_l_s, height)
        return r_pos_x, r_pos_y

