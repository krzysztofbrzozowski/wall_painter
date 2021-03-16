import logging

"""
class SetupLogger:

    def __init__(self):
        self.logger = None
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        print(self.logger)

    def setup_logger(self, name=None, log_file=None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if log_file:
            handler = logging.FileHandler(log_file)
            handler.setFormatter(self.formatter)
            self.logger.addHandler(handler)

        print(self.logger)

        return self.logger

logger = {}
tst = SetupLogger()
logger['GCODE'] = tst.setup_logger('test')

if __name__ == '__main__':
    for n in range(5):
        logger['GCODE'].info(n)


# first file logger
logger = setup_logger('first_logger', 'first_logfile.log')
logger.info('This is just info message')

# second file logger
super_logger = setup_logger('second_logger', 'second_logfile.log')
super_logger.error('This is an error message')

def another_method():
   # using logger defined above also works here
   logger.info('Inside method')

"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerManager:
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_logger(name=None):
        if not name:
            logging.basicConfig()
            return logging.getLogger()
        elif name not in LoggerManager._loggers.keys():
            logging.basicConfig()
            LoggerManager._loggers[name] = logging.getLogger(str(name))
        return LoggerManager._loggers[name]


logger = {'GCODE': LoggerManager().get_logger('GCODE'),
          'HYPEN': LoggerManager().get_logger('HYPEN'),
          'P_INF': LoggerManager().get_logger('P_INF'),

          'STP_INFO': LoggerManager().get_logger('STP_INFO'),
          'TIM_INFO': LoggerManager().get_logger('TIM_INFO')}


logger['GCODE'].setLevel(level=logging.DEBUG)
logger['HYPEN'].setLevel(level=logging.DEBUG)
logger['P_INF'].setLevel(level=logging.INFO)

logger['STP_INFO'].setLevel(level=logging.DEBUG)
logger['TIM_INFO'].setLevel(level=logging.DEBUG)
