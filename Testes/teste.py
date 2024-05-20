import cv2 as cv
import re
from py_openshowvar import openshowvar
client = openshowvar('192.168.50.205', 7000)
print(client.can_connect)

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

client.write('$OV_PRO', '10', debug=False)  # sets the speed

x_robo = 300
y_default = 170  # the robot moves in the plane xz, so the y variable is a constant
z = 100

A = 180
B = 20
C = -180

client.write('COM_ACTION', '3', debug=True)
client.write("COM_POS", str("{X " + str(x_robo) + ", Y " + str(y_default) + ", Z " + str(z) + ", A " +
             str(A) + ", B " + str(B) + ", C " + str(C) + "}"), debug=False)  # Defines join angles
client.write('COM_ACTION', '3', debug=True)
client.write("COM_POS", str("{X " + str(x_robo) + ", Y " + str(y_default) + ", Z " + str(z) + ", A " +
             str(A) + ", B " + str(B) + ", C " + str(C) + "}"), debug=False)  # Defines join angles

client.close()
