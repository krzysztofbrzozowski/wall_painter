from gcode_parser import GCODEParser
from carriage import Carriage
from CONSTANTS import *
from loggers import *
from math_calc import MathCalc


if __name__ == '__main__':
    GCODEParser = GCODEParser('GCODEs/trace_0.txt')

    GCODEParser.set_move_flag(True)     # Will be important when multitask will run

    for ln in range(GCODEParser.get_gcode_lines_amount()):

        values = GCODEParser.get_gcode_line_values()
        logger['P_INF'].info(f'----------------------------- BGN -> GCODE LN: {ln} -----------------------------')

        if len(values):
            # Print out the values coming from GCODE line
            logger['GCODE'].info(f'{values}')
            # Move carriage
            Carriage.move_to_point(**values)
            # Print out the LEFT and RIGHT HYPEN
            logger['HYPEN'].info(f'{Carriage["HYP_L"]}[mm]|{int(round(MathCalc.steps_amt(Carriage["HYP_L"])))}[stp] && '
                                 f'{Carriage["HYP_R"]}[mm]|{int(round(MathCalc.steps_amt(Carriage["HYP_R"])))}[stp]')

        if not len(values):
            logger['P_INF'].info(f'** GCODE line was skipped **')

        GCODEParser.inc_gcode_line()

        logger['P_INF'].info(f'----------------------------- END -> GCODE LN: {ln} -----------------------------\n\n\n')
        # time.sleep(Carriage['STP_TIM'] / 50000)
    Carriage.dis_mtrs()


