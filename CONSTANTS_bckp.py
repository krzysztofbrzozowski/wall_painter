import configparser
import math
import sys
import RPiToSTM
import time

DEBUG = True
MODEL = 'HIL'

# START_POINT = 'middle'  # Carriage in point [WALL_X / 2, Y0]
START_POINT = 'begin'   # Carriage in point [X0, Y0]

DEV_MOTOR_AMT = 2
# BASE_TIME = 'stp_time'
BASE_TIME = 'vel_time'



# if not DEBUG:
#     WALL_X = 1000                   # Whole WIDTH of printing area
#     WALL_Y = 1000                   # Whole HEIGHT of printing area
#
#     MOV_TIM_CONST = 1000 / 250
#     STP_MUL_CONST = 10000 / 97
#
#     STP_DST = 1000                    # Distance for one step in um (TBD)
#     STP_TIM = 0.0001                  # One time step (TBD) -> need to be updated by calculation
#
#     MAX_SPD = 100                     # Max speed in mm/s (TBD)

# ABSOLUTE MAX SPEEDS TO ACHIEVE BY MOTOR PER 'GEAR' [stp/s]
# MAX_MTR_SPD_S_CONST = {'0': 430,    # 1/1
#                        '1': 410,    # 1/2
#                        '2': 200,    # 1/4
#                        '3': 200,    # 1/8
#                        '4': 200,    # 1/16
#                        '5': 200     # 1/32
#                        }

MAX_MTR_SPD_S_CONST = {'0': 480,    # 1/1
                       '1': 500,    # 1/2
                       '2': 250,    # 1/4
                       '3': 125,    # 1/8
                       '4': 62.5,   # 1/16
                       '5': 31.25   # 1/32
                       }

# MOTOR PULLEY CONSTANTS
MTR_PUL_THT = 16                                # Motor pulley teeth amount
MTR_PUL_STP_360 = 200                           # Motor pulley steps on GEAR 0 to make 360 deg turn

# WINDING PULLEY CONSTANTS
WND_PUL_THT = 60                                # Winding pulley teeth amount
WND_PUL_DIA = 36                                # Winding pulley diameter [mm]
WND_PUL_LNT = 2 * math.pi * (WND_PUL_DIA / 2)   # Winding pulley circumference [mm]

RTO_PUL = round(WND_PUL_THT / MTR_PUL_THT, 4)   # Ratio of pulleys



# USER DEFINED MAX SPEEDS
MAX_WND_PUL_SPD_D = 1                          # Max speed of winding pulley [mm/s]
MAX_WND_PUL_SPD_S = None                        # Max speed of winding pulley [stp/s]

MAX_MTR_PUL_SPD_S = None                        # Max speed of motor pulley [stp/s]
GEAR = None

if MAX_WND_PUL_SPD_S is not None:
    MAX_MTR_PUL_SPD_S = MAX_WND_PUL_SPD_S * RTO_PUL
    for k, v in sorted(MAX_MTR_SPD_S_CONST.items(), reverse=True):
        if MAX_MTR_PUL_SPD_S <= v:
            GEAR = int(k)
            break
    if GEAR is None:
        sys.exit('Calculated motor pulley speed is grater than possible max speed')


if MAX_WND_PUL_SPD_D:
    WND_CALCULATED_SECTION = MAX_WND_PUL_SPD_D / WND_PUL_LNT
    MAX_WND_PUL_SPD_S = MTR_PUL_STP_360 * RTO_PUL * WND_CALCULATED_SECTION
    MAX_MTR_PUL_SPD_S = MAX_WND_PUL_SPD_S * RTO_PUL
    for k, v in sorted(MAX_MTR_SPD_S_CONST.items(), reverse=True):
        if MAX_MTR_PUL_SPD_S <= v:
            GEAR = int(k)
            break
    if GEAR is None:
        sys.exit('Calculated motor pulley speed is grater than possible max speed')

    # WND_MOV_TIM_MS_PER_LAP_D = WND_PUL_LNT / MAX_WND_PUL_SPD_D
    # WND_MOV_TIM_MS_PER_LAP_S = (WND_PUL_LNT / WND_PUL_STP_360) * WND_MOV_TIM_MS_PER_LAP_D
    # MTR_MOV_TIM_MS_PER_LAP_S

WND_PUL_STP_360 = MTR_PUL_STP_360 * RTO_PUL * (1 << GEAR)  # Winding pulley steps on GEAR 0 to make 360 deg turn

if DEBUG:
    WALL_X = 10  # Whole WIDTH of printing area [mm] (1000mm -> 1m)
    WALL_Y = 10  # Whole HEIGHT of printing area [mm] (1000mm -> 1m)

    if MODEL == 'SIL':
        MAX_SPD_D = 100  # Max speed [mm/s] -> not used right now (TBD)
        MAX_SPD_S = 1000  # Max speed [steps/s]

        MOV_TIM_CONST = 0.001           # Min time for movement for one step [s]
        STP_MUL_CONST = 100             # Const to calculate needed steps for move

        STP_DST = 1                     # Distance for one step in mm (TBD)
        STP_TIM = 0.0001                # One time step (TBD) -> need to be updated by calculation

    if MODEL == 'HIL':
        MAX_SPD_D = 100  # Max speed [mm/s] -> not used right now (TBD)
        MAX_SPD_S = 150  # Max speed [steps/s]

        MOV_TIM_CONST = 1000 / 250
        STP_MUL_CONST = 10000 / 97

        STP_DST = WND_PUL_LNT / WND_PUL_STP_360
        STP_TIM = 0.01                  # One time step (TBD) -> need to be updated by calculation


if __name__ == '__main__':
    print(f'STEP DISTANCE: {WND_PUL_STP_360, STP_DST, MTR_PUL_STP_360 / MAX_MTR_PUL_SPD_S, WND_PUL_LNT}')

    RPiToSTM.cmd['enb'](0)
    RPiToSTM.cmd['div'](0, GEAR)
    RPiToSTM.cmd['tim'](0, int(MTR_PUL_STP_360 / MAX_MTR_PUL_SPD_S))
    RPiToSTM.cmd['amt'](0, int(WND_PUL_STP_360))
    RPiToSTM.cmd['mov'](0, 1)
    time.sleep(MTR_PUL_STP_360 / MAX_MTR_PUL_SPD_S)
    RPiToSTM.cmd['dsb'](0)
