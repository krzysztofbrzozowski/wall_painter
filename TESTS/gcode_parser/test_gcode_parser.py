import unittest

from gcode_parser import GCODEParser


class TestGcodeParser(unittest.TestCase):

    def setUp(self):
        print(self._testMethodName)

    def test_gcode_desired_lines_amount(self):
        """test if the values are equal"""
        self.GCODEParser = GCODEParser('test_gcode_trace_lines_amount.txt')

        self.expected_result = 69
        self.result = None

        self.result = self.GCODEParser.get_gcode_lines_amount()
        self.assertEqual(self.result, self.expected_result)

    def test_gcode_not_desired_lines_amount(self):
        """test if the values are not equal"""
        self.GCODEParser = GCODEParser('test_gcode_trace_lines_amount.txt')

        self.expected_result = 68
        self.result = None

        self.result = self.GCODEParser.get_gcode_lines_amount()
        self.assertNotEqual(self.result, self.expected_result)

    def test_output_equal_desired_values(self):
        """test if the values are equal"""
        self.GCODEParser = GCODEParser('test_gcode_trace_values.txt')

        self.expected_result = {'ID': 1, 'G': 1, 'X': 563, 'Y': 964, 'E': 63}
        self.result = dict()

        for ln in range(self.GCODEParser.get_gcode_lines_amount()):
            self.result = self.GCODEParser.get_gcode_line_values()

        self.assertEqual(self.result, self.expected_result)

    def test_output_not_equal_desired_values(self):
        """test if the values are not equal"""
        self.GCODEParser = GCODEParser('test_gcode_trace_values.txt')

        self.expected_result = {'ID': 0, 'G': 1, 'X': 563, 'Y': 944, 'E': 63}
        self.result = dict()

        for ln in range(self.GCODEParser.get_gcode_lines_amount()):
            self.result = self.GCODEParser.get_gcode_line_values()

        self.assertNotEqual(self.result, self.expected_result)

    def tearDown(self):
        self.GCODEParser = None


if __name__ == '__main__':
    # suite = unittest.TestSuite((
    #     unittest.makeSuite(TestGcodeParser),
    # ))
    # result = unittest.TextTestRunner().run(suite)
    # TestGcodeParser.disconnect()

    unittest.main()