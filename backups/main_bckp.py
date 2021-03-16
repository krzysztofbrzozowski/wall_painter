import time
import serial
from operator import xor

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def encode(*args):
    key = None
    tmp = []

    for n in args:
        tx = n
        bytes_amount = 0 if n else 1
        while n != 0:
            n = n >> 8
            bytes_amount += 1

        tmp.extend([((0xFF << idx * 8) & tx) >> 8 * idx for idx, _ in enumerate(range(bytes_amount))][::-1])

    for n in range(1, 255 + 1):
        if n not in tmp:
            key = n
            break

    serial_msg = [xor(n, key) for n in tmp]
    serial_msg.insert(0, key)
    serial_msg.append(0)

    # ser.open()
    for msg in serial_msg:
        ser.write(serial.to_bytes([msg]))
    # ser.close()

    return serial_msg
    time.sleep(0.3)

MOTORS = [0, 1]


def move(direction, steps, time_ms):

    for mtr in MOTORS:
        mtr = mtr << 5

        if not mtr:
            msg = encode(0x88 | mtr) if direction == 'UP' else encode(0x89 | mtr) 
        else:
            msg = encode(0x89 | mtr) if direction == 'UP' else encode(0x88 | mtr)
        
        msg = encode(0x80 | mtr)                # ON
        msg = encode(0x90 | mtr | 7)            # 1/1
        msg = encode(0x86 | mtr, steps)         # stpamt
        msg = encode(0x85 | mtr, int(time_ms / 20)) # stptim

    for mtr in MOTORS:
        msg = encode(mtr + 1)   # START
        # msg = encode(0x90 | mtr | 7)            # 1/1

    time.sleep(time_ms / 1000)

    for mtr in MOTORS:
        mtr = mtr << 5
        encode(0x81 | mtr)


def move_s(direction, steps, time_ms):

    for mtr in MOTORS:
        mtr = mtr << 5

        if not mtr:
            msg = encode(0x88 | mtr) if direction == 'RIGHT' else encode(0x89 | mtr) 
        else:
            msg = encode(0x88 | mtr) if direction == 'RIGHT' else encode(0x89 | mtr)
        
        msg = encode(0x80 | mtr)                # ON
        msg = encode(0x90 | mtr | 7)            # 1/1
        msg = encode(0x86 | mtr, steps)         # stpamt
        msg = encode(0x85 | mtr, int(time_ms / 20)) # stptim

    for mtr in MOTORS:
        msg = encode(mtr + 1)   # START
        # msg = encode(0x90 | mtr | 7)            # 1/1

    # time.sleep(time_ms / 1000)

    # for mtr in MOTORS:
    #     mtr = mtr << 5
    #     encode(0x81 | mtr)


def move_down(steps, time):
    pass


MOVE_CONST = 2
STEPS = 10000

if __name__ == '__main__':
    move('UP', STEPS, STEPS * MOVE_CONST)
    # move_s('RIGHT', 90000, 25000)
    # move_s('LEFT', 90000, 50000)


    # move('DOWN', 40000, 3000)

