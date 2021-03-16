import configparser
import math
import sys
import RPiToSTM
import time

DEBUG = True
MODEL = 'HIL'

# Set the start point of the carriage
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

# DESIRED_DISTANCE = 113.09733552923255
DESIRED_DISTANCE = 296


WND_MAX_SPEED_SEC = 40       # [mm/s]

WND_PUL_THT = 60        # Winding pulley teeth amount
WND_PUL_DIA = 39
WND_PUL_LNT = 2 * math.pi * (WND_PUL_DIA / 2)   # Winding pulley circumference [mm]

MTR_PUL_THT = 16        # Motor pulley teeth amount
MTR_PUL_STP_360 = 200   # Motor pulley steps for 360deg

# ----------------------------------------------------------------------------
RTO_PUL = round(WND_PUL_THT / MTR_PUL_THT, 4)   # Ratio of pulleys

# Motor steps [stp] needed to move desired distance
WND_STPS_DIST = MTR_PUL_STP_360 * RTO_PUL * (DESIRED_DISTANCE / WND_PUL_LNT)

# Time in seconds [s] needed to move desired distance regarding WND_MAX_SPEED_SEC
TIM_WND_DSR_DIS_SEC = DESIRED_DISTANCE / WND_MAX_SPEED_SEC

# Speed of WINDING pulley to achieve in [stp/s]
WND_MAX_SPEED_STP = WND_STPS_DIST / TIM_WND_DSR_DIS_SEC

# Speed of MOTOR pulley to achieve in [stp/s]
MTR_MAX_SPEED_STP = WND_MAX_SPEED_STP * RTO_PUL

# Time needed for motor to move desired distance in [s]
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
    WALL_X = 1000  # Whole WIDTH of printing area [mm] (1000mm -> 1m)
    WALL_Y = 1000  # Whole HEIGHT of printing area [mm] (1000mm -> 1m)

    if MODEL == 'HIL':
        STP_DST = DESIRED_DISTANCE / WND_STPS_DIST


if __name__ == '__main__':
    print(f'I have to move {WND_STPS_DIST}[step] in {MTR_TIM}[second]')

#     RPiToSTM.cmd['enb'](0)
#     RPiToSTM.cmd['dir'](0, 'CW')
#     RPiToSTM.cmd['div'](0, GEAR)
#     RPiToSTM.cmd['tim'](0, int(MTR_TIM * 1000))
#     RPiToSTM.cmd['amt'](0, int(WND_STPS_DIST))
#     RPiToSTM.cmd['mov'](0, 1)
#     time.sleep(MTR_TIM + 0.1)
#     RPiToSTM.cmd['dsb'](0)