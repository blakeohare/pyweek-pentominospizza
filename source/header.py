import math
import time
import random
import os

PI = 3.14159265358979323
TWO_PI = PI * 2
HALF_PI = PI / 2

# FPS and Seconds per frame
# ...at least canonically at 30 FPS which must of the calculations are done in due 
# to writing in PyGame initially. Divide the dt value by this.
FPS = 30.0
SPF = 1.0 / FPS
