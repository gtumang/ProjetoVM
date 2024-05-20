from kukaMov import Kuka
import funcKukacador
import time
import numpy as np
from math import cos, sin, pi
import sys

OFFSET_U = int(308.4772644042969)-272
OFFSET_V = int(162.7045440673828)-95

# Homogenea C para B
# Rx(90 graus)
# T(250,150,80)

alpha = -pi/2

bH_c = np.array([[1,     0,         0,        250],
                 [0, cos(alpha), -sin(alpha), 150],
                 [0, sin(alpha), cos(alpha),   80],
                 [0,     0,         0,        1]])

f = 3.67
# ro_w = 7.6679e-04
# ro_h = 7.6679e-04
ro_w = 3.98e-3
ro_h = 3.98e-3

p_x = 300
p_y = 300

posTela_C = funcKukacador.calculaPosTelaC(p_x, p_y, 1270, f, ro_h, ro_w)
posTela_C.append(1)
posHKuka_B = funcKukacador.calculaPosKukaB(posTela_C, bH_c)

print(posHKuka_B)
posHKuka_B[1] = posHKuka_B[1]-1420

posKuka_B = posHKuka_B[:3]

# if posKuka_B[0] < 50 or posKuka_B[2] < 50:
#     sys.exit()

posKuka = list(posKuka_B)
posKuka.append(0)
posKuka.append(0)
posKuka.append(-175)

print(posKuka)

rob = Kuka('192.168.50.205', 7000)

if rob.connect():
    rob.init()
    rob.setVel(2)
    # time.sleep(1)
    rob.setPos(posKuka)
    time.sleep(5)
    print(rob.getPos())
    rob.close()
