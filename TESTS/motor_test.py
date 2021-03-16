import time

import RPiToSTM


if __name__ == '__main__':
    MOV_TIM_MS = 200000

    # RPiToSTM.mtr_enb_cmd(0)
    # RPiToSTM.mtr_enb_cmd(1)

    # RPiToSTM.mtr_stps_tim(0, MOV_TIM_MS)
    # RPiToSTM.mtr_stps_tim(1, MOV_TIM_MS)

    # RPiToSTM.mtr_stps_amt(0, 200)
    # RPiToSTM.mtr_stps_amt(1, 200)

    # RPiToSTM.mtr_mov_cmd(0, 1)
    # RPiToSTM.mtr_mov_cmd(1, 1)

    # time.sleep((MOV_TIM_MS / 1000) + 0.1)

    # RPiToSTM.mtr_dsb_cmd(0)
    # RPiToSTM.mtr_dsb_cmd(1)

    # DICTIONARY TEST

    RPiToSTM.cmd['enb'](0)
    RPiToSTM.cmd['enb'](1)

    RPiToSTM.cmd['tim'](0, MOV_TIM_MS)
    RPiToSTM.cmd['tim'](1, MOV_TIM_MS)

    # RPiToSTM.cmd['div'](0, 0)
    # RPiToSTM.cmd['div'](1, 0)

    RPiToSTM.cmd['amt'](0, int(MOV_TIM_MS / 10))
    RPiToSTM.cmd['amt'](1, int(MOV_TIM_MS / 10))

    RPiToSTM.cmd['mov'](0, 1)
    RPiToSTM.cmd['mov'](1, 1)

    for n in range(7):
        print(f'GEAR: {n}')
        RPiToSTM.cmd['div'](0, n)
        RPiToSTM.cmd['div'](1, n)
        time.sleep(5)

    time.sleep((MOV_TIM_MS / 1000) + 0.1)

    RPiToSTM.cmd['dsb'](0)
    RPiToSTM.cmd['dsb'](1)