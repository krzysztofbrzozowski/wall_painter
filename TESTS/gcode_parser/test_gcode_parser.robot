*** Settings ***
Resource    keywords.robot
Documentation    This is some basic info about whole suite


*** Variables ***
${GCODE_TRACE_VAL}  /Users/krzysztofbrzozowski/Documents/PROJECTS/HARDWARE/wall_painter/software/app/TESTS/gcode_parser/test_gcode_trace_values.txt
${GCODE_TRACE_AMT}  /Users/krzysztofbrzozowski/Documents/PROJECTS/HARDWARE/wall_painter/software/app/TESTS/gcode_parser/test_gcode_trace_lines_amount.txt

*** Test Cases ***
Gcode lines amount equal desired value
    [Documentation]    Lines amount shall be the same as expected
    [Tags]    Unit Test

    ${expected}=    convert to integer    69
    ${result}=  Get GCODE lines amount from file ${GCODE_TRACE_AMT}
    should be equal    ${result}    ${expected}


Gcode lines amount NOT equal desired value
    [Documentation]    Lines amount shall NOT be the same as expected
    [Tags]    Unit Test

    ${expected}=    convert to integer    68
    ${result}=  Get GCODE lines amount from file ${GCODE_TRACE_AMT}
    should not be equal    ${result}    ${expected}

Output equal desired values
    [Documentation]    Values shall be the same as expected
    [Tags]    Unit Test

    ${expected}     create dictionary    ID=${1}   G=${1}   X=${563}   Y=${964}   E=${63}
    ${result}=  Get GCODE line values from file ${GCODE_TRACE_VAL}
    should be equal     ${result}   ${expected}


Output NOT equal desired values
    [Documentation]    Values shall NOT be the same as expected
    [Tags]    Unit Test

    ${expected}     create dictionary    ID=${2}   G=${4}   X=${563}   Y=${964}   E=${63}
    ${result}=  Get GCODE line values from file ${GCODE_TRACE_VAL}
    should not be equal    ${result}   ${expected}
