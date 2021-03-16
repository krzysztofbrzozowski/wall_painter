import time
from prettytable import PrettyTable
from serial_encoder import SerialEncoder
from math_calc import TrigoCalc
from gcode_parser import  TraceManager

s_encoder = SerialEncoder('/dev/ttyS0', 115200)

MOTORS = [0, 1]
# WALL_X = 2000
WALL_X = 1600
WALL_Y = 785

MOVE_TIME_CONST = 1000 / 250
STEPS = 1000
STEPS_TIME_MS = STEPS * MOVE_TIME_CONST

DATA = {'curr_pos': [0, 0], 'hyp_l': 0, 'hyp_r': 0}

data_t = PrettyTable(['STEP', 'CURRENT POSITION', 'ROLL L',
                      'ROLL R', 'DESTINATION', 'HYP_L', 'HYP_R'])
data_to_print = []


def print_table(table):
    for idx, data in enumerate(table):
        if idx:
            data[0] = idx - 1
        data_t.add_row(data)
    print(data_t)


def insert_to_table(idx: ' - ', curr_pos: [0, 0], roll_l: 0, roll_r: 0, dest_pos: [0, 0], hyp_l=0, hyp_r=0):
    data_to_print.append([idx, f'X: {curr_pos[0]:.3f}, Y: {curr_pos[1]:.3f}',
                          roll_l, roll_r, f'X: {dest_pos[0]:.3f}, Y: {dest_pos[1]:.3f}', hyp_l, hyp_r])


# def trigo_calc(size_x, size_y):
#     tangent = size_y / size_x
#
#     tangent_alpha = math.degrees(math.atan(tangent))
#     sinus_alpha = math.sin(math.radians(tangent_alpha))
#
#     hypotenuse = size_y / sinus_alpha
#
#     return hypotenuse


def start_data(wall_size_x, wall_size_y):
    DATA['hyp_l'] = TrigoCalc.get_hypotenuse(wall_size_x / 2, wall_size_y)
    DATA['hyp_r'] = TrigoCalc.get_hypotenuse(wall_size_x / 2, wall_size_y)
    DATA['curr_pos'] = [0, 0]

    insert_to_table(idx=' - ',
                    curr_pos=[0, 0],
                    roll_l=' - ',
                    roll_r=' - ',
                    dest_pos=[0, 0],
                    hyp_l=DATA['hyp_l'],
                    hyp_r=DATA['hyp_r'])


def move_motor(steps_l, steps_r, time_ms):
    for mtr in MOTORS:
        mtr = mtr << 5

        if not mtr:
            msg = s_encoder.encode(0x88 | mtr) if steps_l >= 0 else s_encoder.encode(0x89 | mtr)
        else:
            msg = s_encoder.encode(0x89 | mtr) if steps_r >= 0 else s_encoder.encode(0x88 | mtr)
        
        msg = s_encoder.encode(0x80 | mtr)                # ON
        msg = s_encoder.encode(0x90 | mtr | 7)            # 1/32

        if not mtr:
            msg = s_encoder.encode(0x86 | mtr, abs(steps_l))         # stpamt
        else:
            msg = s_encoder.encode(0x86 | mtr, abs(steps_r))         # stpamt

        msg = s_encoder.encode(0x85 | mtr, int(time_ms / 15)) # stptim

    for mtr in MOTORS:
        msg = s_encoder.encode(mtr + 1)   # START


def disable_motor():
    for mtr in MOTORS:
        mtr = mtr << 5
        s_encoder.encode(0x81 | mtr)


def move_p(**arg):
    curr_pos = DATA['curr_pos']
    dest_pos = [arg['x_movement'], arg['y_movement']]

    x_l = WALL_X / 2 + arg['x_movement']
    x_r = WALL_X / 2 - arg['x_movement']

    y_b = arg['y_movement']
    y_t = WALL_Y - arg['y_movement']

    next_hyp_l = TrigoCalc.get_hypotenuse(x_l, y_t)
    next_hyp_r = TrigoCalc.get_hypotenuse(x_r, y_t)

    roll_l = DATA['hyp_l'] - next_hyp_l
    roll_r = DATA['hyp_r'] - next_hyp_r

    steps = lambda distance: int(distance * (10000 / 97))
    steps_time = abs(int(steps(roll_l) * MOVE_TIME_CONST)) if steps(roll_l) > steps(roll_r) else abs(int(steps(roll_r) * MOVE_TIME_CONST))
    print('steps_time: ', steps_time)
    move_motor(steps(roll_l), steps(roll_r), steps_time)

    # time.sleep(steps_time / 1000)
    # disable_motor()

    DATA['hyp_l'] = next_hyp_l
    DATA['hyp_r'] = next_hyp_r
    DATA['curr_pos'] = dest_pos

    insert_to_table(idx=' - ',
                    curr_pos=curr_pos,
                    roll_l=roll_l,
                    roll_r=roll_r,
                    dest_pos=dest_pos,
                    hyp_l=DATA['hyp_l'],
                    hyp_r=DATA['hyp_r'])
    
    print('done')


def extrude(percentage):
    msg = s_encoder.encode(0x83, 100 - percentage)


def test_motor(motor, steps, s_time):
    mtr = motor << 5
    msg = s_encoder.encode(0x80 | mtr)                # ON
    msg = s_encoder.encode(0x88 | mtr)
    msg = s_encoder.encode(0x90 | mtr | 7)            # 1/32
    # msg = s_encoder.encode(0x90 | mtr | 0)            # 1/1

    msg = s_encoder.encode(0x86 | mtr, abs(steps))         # stpamt
    # print(msg)
    msg = s_encoder.encode(0x85 | mtr, s_time) # stptim

    msg = s_encoder.encode(motor + 1)   # START

    if steps > s_time * 20:
        print(f'hit max speed for MOTOR {motor}')
    steps_time = steps / 2250 if steps > s_time * 20 else int((s_time * 20) / steps) * (1 / 2250) * steps

    # devider = int(s_time * 20 / steps)
    # print(f'time in seconds: {devider * 20}')
    print(f'time in seconds for MOTOR {motor}: {steps_time}')


    # msg = s_encoder.encode(0x81 | mtr)

def find_equalizer(steps_0, steps_1, s_time):
    steps_list = [steps_0, steps_1]
    new_time = [0, 0]

    for idx, steps in enumerate(steps_list):
        if steps > s_time * 20:
            print(f'hit max speed for MOTOR {idx}')
            new_time[idx] = round(steps / 2250, 2)
        else:
            new_time[idx] = round(int((s_time * 20) / steps) * (1 / 2250) * steps, 2)

    print(new_time)

    i = 0
    while abs(new_time[0] - new_time[1]) > 0.5:
        s_time = s_time + i
        new_time[0] = round(int((s_time * 20) / steps_0) * (1 / 2250) * steps_0, 2)
        print(s_time, new_time[0])

        i += 1
        time.sleep(0.1)

    # if abs(new_time[0] - new_time[1]) > 0.1:
    #     print('dupa')


    # if steps > s_time * 20:
    #     print(f'hit max speed for MOTOR {motor}')

    # steps_time = steps / 2250 if steps > s_time * 20 else int((s_time * 20) / steps) * (1 / 2250) * steps

    # return new_time_0, new_time_1

STEPS_0 = 40252
STEPS_1 = 20001
TIME = 3000

if __name__ == '__main__':

    #     move_p(x_movement=0, y_movement=100)
    #     time.sleep(2)


    # disable_motor()
    # extrude(50)

    # s_encoder.start_serial_listen_thread()
    # test_motor(0, 30252, 3000)
    # test_motor(1, 20000, 3000)

    # find_equalizer(STEPS_0, STEPS_1, TIME)

    # print(int((1000 * 20) / 3200) * (1 / 2250) * 3200)




    # start_data(WALL_X, WALL_Y)
    # move_p(x_movement=0, y_movement=10)

    # print_table(data_to_print)

    # while(True):
    #     pass

    # extrude(100)
    # start_data(WALL_X, WALL_Y)
    # move_p(x_movement=0, y_movement=100)
    # time.sleep(10)
    # move_p(x_movement=0, y_movement=200)
    # time.sleep(10)
    # move_p(x_movement=0, y_movement=300)

    # move_p(x_movement=300, y_movement=300)
    # move_p(x_movement=100, y_movement=0)
    # move_p(x_movement=0, y_movement=0)



    # move_p(x_movement=20, y_movement=20)
    # move_p(x_movement=30, y_movement=30)
    # move_p(x_movement=1, y_movement=500)

    # print_table(data_to_print)

    # extrude(50)
    # for n in range(100):
    #     if not n % 2:
    #         print(n)
    #         extrude(50)
    #     else:
    #         extrude(100)
        
    #     time.sleep(1)

    TM = TraceManager()
    TM.safe_trace()