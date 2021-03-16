RPi Python App to control the wall painter

Content of a program:

main.py: main runner of the app
-

class *GCODEParser*:
* reading the GCODE 
* getting all GCODE line values


class *Carriage*:
* moving whole carriage into needed point according GCODE readed before
---

carriage.py: carriage runner
-
class *Carriage*
* contains two motors (MOT_L and MOR_R) - *Motor* classes
* first running point of the class is method 'move_to_point'
---
CONSTANTS.py: all necessary settings for the app
-

TODO LIST:
-
* continue with README.md
* fix the start point - now it is 'begin' but it is not possible to achieve this in real word

