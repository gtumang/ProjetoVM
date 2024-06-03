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

print("Valor de X do robo:", x_value)
print("Valor de Y do robo:", y_value)
print("Valor de Z do robo:", z_value)

client.write('$OV_PRO', '5', debug=False)  # sets the speed

# x_robo = 300
# y_default = 0 # the robot moves in the plane xz, so the y variable is a constant
# z = 200

# A = 0
# B = 0
# C = -175

x_robo_max = 430
z_robo_max = 320
x_robo_min = -100
z_robo_min = 89

imagePoints = [[211.45245361328125, 173.94552612304688],
               [235.53671264648438, 174.5],
               [260.072509765625, 174.4642791748047],
               [211.5, 149.0],
               [236.5, 149.90695190429688],
               [261.42425537109375, 149.0357208251953],
               [211.4801788330078, 124.01821899414062],
               [236.53614807128906, 124.53313446044922],
               [261.5, 124.0]]

posImage_list = imagePoints[3]
posImage_list.append(1)

posImage = np.array([331.56097412109375, 137.4261474609375, 1300, 1])


def image2world(point):
    return np.array((1.98922818*point[0]-468.36345474, 1.93554415*point[1]-389.37186598, 1300, 1))


posC = image2world(posImage)


# print(offset_x)

# posC[0] = posC[0]+offset_x

posCt = posC.T

alpha = -pi/2

bH_c = np.array([[1,     0,         0,        250],
                 [0, cos(alpha), -sin(alpha), 150],
                 [0, sin(alpha), cos(alpha),   80],
                 [0,     0,         0,        1]])

posB = np.matmul(bH_c, posCt)

offset_x = -27
offset_z = 95

# x_robo = posB[0]+offset_x
# y_default = -200
# z_robo = posB[2]+offset_z
x_robo = x_robo_min
y_default = -200
z_robo = z_robo_max

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
