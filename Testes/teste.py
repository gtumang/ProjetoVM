import cv2 as cv
import re
from py_openshowvar import openshowvar
import numpy as np
from math import sin, cos, pi


def calculaPosKukaB(pos, mHom) -> tuple:
    print(pos)
    posC = np.array(pos)
    print(posC)
    posB = np.matmul(mHom, posC)
    return posB


client = openshowvar('192.168.50.205', 7000)
# print(client.can_connect)

bla = client.read("$POS_ACT", debug=False)
# # Extrair o conteúdo entre aspas simples
# # Converter os bytes para string

data_string = bla.decode()

# Extrair os valores de X, Y e Z usando expressões regulares
x_value = float(re.findall(r'X ([\d.-]+)', data_string)[0])
y_value = float(re.findall(r'Y ([\d.-]+)', data_string)[0])
z_value = float(re.findall(r'Z ([\d.-]+)', data_string)[0])

# print("Valor de X do robo:", x_value)
# print("Valor de Y do robo:", y_value)
# print("Valor de Z do robo:", z_value)

client.write('$OV_PRO', '5', debug=False)  # sets the speed

# x_robo = 300
# y_default = 0 # the robot moves in the plane xz, so the y variable is a constant
# z = 200

# A = 0
# B = 0
# C = -175

# pontos meio:
# 8: [  16.82926871,
# -138.884677,
# 1317.17096396]
# erro: y=4mm, x=40mm

# 5:
# [57.96082591,
#  -54.20936614,
#  1266.78254289]
# erro: y=2mm,x=25mm

# 2:
# [-1.57934635,
#  -53.68170028,
#  1275.23845624]
# erro: y=2mm, x=25mm

# pontos esquerda:
# 7:
# [-68.41826589,
#  -150.90859058,
#  1311.17035087]
# erro: x=15mm,y=3mm
# 4:
# [-64.57410669,
#  -101.96532622,
#  1298.63383601]
# erro:x=15mm, y=3mm
# 1:
# [-57.89615511,
#  -52.4823431,
#  1288.56890307]
# erro: x=20mm,y=1mm

# Pontos direita:
# 3:
# [57.96082591,
#  -54.20936614,
#  1266.78254289]

# 6:
# [57.7614113,
#  -101.10507864,
#  1278.05144644]

# 9:
[56.97577122,
 -146.52463578,
 1291.68422494]

posC = np.array((50,
                 -150,
                 1300,
                 1))


def ajuste_x(pos_x):
    return -0.17262662831294961*pos_x-25


offset_x = ajuste_x(posC[0])


print(offset_x)

# posC[0] = posC[0]+offset_x

posCt = posC.T

alpha = -pi/2

bH_c = np.array([[1,     0,         0,        250],
                 [0, cos(alpha), -sin(alpha), 150],
                 [0, sin(alpha), cos(alpha),   80],
                 [0,     0,         0,        1]])

posB = np.matmul(bH_c, posCt)

offset_z = 95

x_robo = posB[0]
y_default = -20
z_robo = posB[2]+offset_z

A = 0
B = 0
C = -175

print(posB)

client.write('COM_ACTION', '3', debug=True)
client.write("COM_POS", str("{X " + str(x_robo) + ", Y " + str(y_default) + ", Z " + str(z_robo) + ", A " +
             str(A) + ", B " + str(B) + ", C " + str(C) + "}"), debug=False)  # Defines join angles
client.write('COM_ACTION', '3', debug=True)
client.write("COM_POS", str("{X " + str(x_robo) + ", Y " + str(y_default) + ", Z " + str(z_robo) + ", A " +
             str(A) + ", B " + str(B) + ", C " + str(C) + "}"), debug=False)  # Defines join angles

client.close()
