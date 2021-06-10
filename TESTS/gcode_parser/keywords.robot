*** Settings ***
Library    lib/gcode_reader.py
Library    test_lib.py

*** Variables ***


*** Keywords ***
Get GCODE line values from file ${TEST}
    ${result}=  get gcode line values r    ${TEST}
    [Return]    ${result}


Get GCODE lines amount from file ${TEST}
    ${result}=  get gcode lines amount    ${TEST}
    [Return]    ${result}