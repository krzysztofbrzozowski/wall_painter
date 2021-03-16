import time

import RPiToSTM


if __name__ == '__main__':
    LAPS_NO = 1
    MOV_TIM_MS_PER_LAP = 400
    # GEAR = 0          # (1/1) MODE0 = 0, MODE1 = 0, MODE2 = 0 | OK
    GEAR = 1          # (1/2) MODE0 = 1, MODE1 = 0, MODE2 = 0 | OK
    # GEAR = 2          # (1/4) MODE0 = 0, MODE1 = 1, MODE2 = 0 | OK
    # GEAR = 3          # (1/8) MODE0 = 1, MODE1 = 1, MODE2 = 0 | OK
    # GEAR = 4          # (1/16) MODE0 = 0, MODE1 = 0, MODE2 = 1 | OK
    # GEAR = 5          # (1/32) MODE0 = 1, MODE1 = 0, MODE2 = 1 | OK

    RPiToSTM.cmd['enb'](1)

    RPiToSTM.cmd['tim'](1, MOV_TIM_MS_PER_LAP * (LAPS_NO << GEAR))
    RPiToSTM.cmd['div'](1, GEAR)
    RPiToSTM.cmd['amt'](1, 200 * (LAPS_NO << GEAR))
    # print(LAPS_NO << GEAR)
    RPiToSTM.cmd['mov'](1, 1)
    START = time.time()
    print(f'STARTED: {START}')
    #
    time.sleep((MOV_TIM_MS_PER_LAP * (LAPS_NO << GEAR) / 1000))
    #
    print(f'FINISHED: {time.time() - START}')
    RPiToSTM.cmd['dsb'](1)

    STEPS_FOR_SECOND = (1000 / MOV_TIM_MS_PER_LAP) * 200 * (LAPS_NO << GEAR)
    print(f'{int(STEPS_FOR_SECOND)} [stp/s]')


    # RPiToSTM.cmd['amt'](1, 200 * 32)
    # CMD = 0x86 | 1 << 5 | 6400
    # RPiToSTM.cmd['raw'](CMD)
    # print(CMD, hex(CMD), bin(CMD))

