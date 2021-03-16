import sys

from CONSTANTS import *
import math


class MathCalc:

    @staticmethod
    def get_hypotenuse(x: int, y: int):
        tangent_alpha = math.degrees(math.atan(y / x)) if x else math.degrees(math.atan(y / 1))
        sinus_alpha = math.sin(math.radians(tangent_alpha))
        if not sinus_alpha:
            sys.exit('Temporary not possible to achieve this GCODE point')
        hypotenuse = y / sinus_alpha
        return hypotenuse

    @staticmethod
    def steps_amt(distance: float):
        if DEBUG:
            if MODEL == 'HIL':
                stps = MTR_PUL_STP_360 * RTO_PUL * (distance / WND_PUL_LNT)
                return stps * (1 << GEAR)

    @staticmethod
    def steps_tim(steps: int):
        if DEBUG:
            if BASE_TIME == 'stp_time':
                return steps * MOV_TIM_CONST
            if BASE_TIME == 'vel_time':
                return steps / WND_MAX_SPEED_STP

        return int(steps * MOV_TIM_CONST)

    @staticmethod
    def herons_calc(hyp_l: int, hyp_r: int, wall_x: int):
        h = 0.5 * math.sqrt((hyp_l + wall_x + hyp_r) * (-hyp_l + wall_x + hyp_r) * (hyp_l - wall_x + hyp_r) *
                            (hyp_l + wall_x - hyp_r)) / wall_x
        return h

    @staticmethod
    def pythagoras_calc_hh(hyp: int, h: int):
        base = math.sqrt(pow(hyp, 2) - pow(h, 2))
        return base

    @staticmethod
    def round_stp(stps: float):
        return int(round(stps))
