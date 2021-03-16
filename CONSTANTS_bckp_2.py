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


MAX_MTR_SPD_S_CONST = {'0': 1000,    # 1/1
                       '1': 500,    # 1/2  | OK
                       '2': 250,    # 1/4  | OK
                       '3': 125,    # 1/8  | OK
                       '4': 62.5,   # 1/16 | OK
                       '5': 31.25   # 1/32 | OK
                       }

DESIRED_DISTANCE = 113.09733552923255
# DESIRED_DISTANCE = 100


WND_MAX_SPEED_SEC = 40       # [mm/s]

WND_PUL_THT = 60        # Winding pulley teeth amount
WND_PUL_DIA = 36
WND_PUL_LNT = 2 * math.pi * (WND_PUL_DIA / 2)   # Winding pulley circumference [mm]

MTR_PUL_THT = 16        # Motor pulley teeth amount
MTR_PUL_STP_360 = 200   # Motor pulley steps for 360deg

# ----------------------------------------------------------------------------
RTO_PUL = round(WND_PUL_THT / MTR_PUL_THT, 4)   # Ratio of pulleys

# Motor steps [stp] needed to move desired distance
WND_STPS_360 = MTR_PUL_STP_360 * RTO_PUL
WND_STPS_DIST = MTR_PUL_STP_360 * RTO_PUL * (DESIRED_DISTANCE / WND_PUL_LNT)

# Time in seconds [s] needed to move desired distance regarding WND_MAX_SPEED_SEC
TIM_WND_360_SEC = WND_PUL_LNT / WND_MAX_SPEED_SEC
TIM_WND_DSR_DIS_SEC = DESIRED_DISTANCE / WND_MAX_SPEED_SEC

# Speed of WINDING pulley to achieve in [stp/s]
# WND_MAX_SPEED_STP = WND_STPS_360 / TIM_WND_360_SEC
WND_MAX_SPEED_STP = WND_STPS_DIST / TIM_WND_DSR_DIS_SEC

# Speed of MOTOR pulley to achieve in [stp/s]
MTR_MAX_SPEED_STP = WND_MAX_SPEED_STP * RTO_PUL

# Time needed for motor to move desired distance in [s]
# MTR_TIM = WND_STPS_360 / MTR_MAX_SPEED_STP
# MTR_TIM = WND_STPS_DIST / MTR_MAX_SPEED_STP
MTR_TIM = WND_STPS_DIST / WND_MAX_SPEED_STP

GEAR = None
for k, v in sorted(MAX_MTR_SPD_S_CONST.items(), reverse=True):
    if MTR_MAX_SPEED_STP <= v:
        GEAR = int(k)
        break
if GEAR is None:
    sys.exit('Calculated motor pulley speed is grater than possible max speed')

# Updated values after select GEAR
WND_STPS_DIST = WND_STPS_DIST * (1 << GEAR)

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

        STP_DST = DESIRED_DISTANCE / WND_STPS_DIST
        STP_TIM = 0.01                  # One time step (TBD) -> need to be updated by calculation

