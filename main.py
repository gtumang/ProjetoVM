from kukaMov import Kuka
import funcKukacador
import time
import numpy as np
from math import cos, sin, pi
import sys

OFFSET_CORTE_U = 70
OFFSET_CORTE_V = 10

# cam_mtx = [[1.25713212e+03, 0.00000000e+00, 3.03629665e+02],
#            [0.00000000e+00, 1.24920455e+03, 1.78493973e+02],
#            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

# # Homogenea C para B
# # Rx(90 graus)
# # T(250,150,80)

# alpha = -pi/2

# bH_c = np.array([[1,     0,         0,        250],
#                  [0, cos(alpha), -sin(alpha), 150],
#                  [0, sin(alpha), cos(alpha),   80],
#                  [0,     0,         0,        1]])

# # f = 3.67
# # f = 3.67
# # ro_w = 7.6679e-04
# # ro_h = 7.6679e-04
# ro_w = 3.98e-3
# ro_h = 3.98e-3


# def correcao(pos) -> tuple:
#     return 1.7*pos+10


# # alterar esses valores em pixel para mover o robo
# # cuidado ao mexer nas outras coisas
# p_x = 235
# p_y = 50


# posTela_C = funcKukacador.calculaPosTelaC(
#     u=p_x, u0=320, v0=480, v=p_y, mtx=cam_mtx, Z=1270, ro_h=ro_h, ro_w=ro_w)
# posTela_C.append(1)
# posHKuka_B = funcKukacador.calculaPosKukaB(posTela_C, bH_c)

# print(posHKuka_B)
# posHKuka_B[1] = -200

# posKuka_B = posHKuka_B[:3]

# # if posKuka_B[0] < 50 or posKuka_B[2] < 50:
# #     sys.exit()

# posKuka = list(posKuka_B)
# posKuka.append(0)
# posKuka.append(0)
# posKuka.append(-175)

# print(posKuka)

rob = Kuka('192.168.50.205', 7000)

if rob.connect():
    rob.init()
    rob.setVel(2)
    # time.sleep(1)
    rob.setPos([rob.x_robo_min, rob.y_default, rob.z_robo_max, 0, 0, -175])
    time.sleep(5)
    print(rob.getPos())
    rob.close()
