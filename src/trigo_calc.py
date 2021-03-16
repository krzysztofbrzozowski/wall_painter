import math


class TrigoCalc:
    def __init__(self):
        pass

    @staticmethod
    def get_hypotenuse(x, y):
        tangent_alpha = math.degrees(math.atan(y / x))
        sinus_alpha = math.sin(math.radians(tangent_alpha))
        hypotenuse = y / sinus_alpha
        return hypotenuse