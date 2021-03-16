import time
import serial
from threading import Thread
from operator import xor


class SerialEncoder():
    def __init__(self, port, speed):
        self.ser = serial.Serial(
            port=port,
            baudrate=speed,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.rx_buf = []
        self.timer = None
    

    def encode(self, *args):
        key = None
        tmp = []

        for n in args:
            tx = n
            bytes_amount = 0 if n else 1
            while n != 0:
                n = n >> 8
                bytes_amount += 1

            # print(bytes_amount)

            tmp.extend([((0xFF << idx * 8) & tx) >> 8 * idx for idx, _ in enumerate(range(bytes_amount))][::-1])

        for n in range(1, 255 + 1):
            if n not in tmp:
                key = n
                break

        # print(tmp)
        serial_msg = [xor(n, key) for n in tmp]
        serial_msg.insert(0, key)
        serial_msg.append(0)

        # ser.open()
        for msg in serial_msg:
            self.ser.write(serial.to_bytes([msg]))
        # ser.close()

        # time.sleep(0.01)
        return serial_msg


    def decode(self, rx_msg):
        key = rx_msg[0]
        return [xor(ord(key), ord(n)) for n in rx_msg[1:]]


    def serial_listner(self):
        while True:
            readed = self.ser.read()
            if readed != bytes() and readed != b'\x00':
                self.rx_buf.append(readed)

            if readed == b'\x00':
                if any(x in self.decode(self.rx_buf) for x in [100, 101]):
                # if 100 or 101 in self.:
                    self.timer = time.time()
                if any(x in self.decode(self.rx_buf) for x in [200, 201]):
                # if 200 or 201 in self.decode(self.rx_buf):
                    print(f'motor spin time: {time.time() - self.timer}')

                self.rx_buf = []
                


    def start_serial_listen_thread(self):
        if not self.ser.isOpen():
            self.ser.open()
        Thread(target=self.serial_listner, args=()).start()
