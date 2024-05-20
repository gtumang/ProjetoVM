from py_openshowvar import openshowvar
import re


class Kuka:
    def __init__(self, ip, port) -> None:
        self._ip = ip
        self._port = port

        self.home = (300, 0, 200, 0, 0, -175)  # home coordinates
        self.offset_x = -40  # mm

    def connect(self) -> bool:
        self.client = openshowvar(self._ip, self._port)
        return self.client.can_connect

    def updatePos(self) -> None:
        self.client.write('COM_ACTION', '3', debug=True)
        self.client.write("COM_POS", str("{X " + str(self._x) + ", Y " + str(self._y) + ", Z " + str(self._z) + ", A " +
                                         str(self._A) + ", B " + str(self._B) + ", C " + str(self._C) + "}"), debug=False)  # Defines join angles
        self.client.write('COM_ACTION', '3', debug=True)
        self.client.write("COM_POS", str("{X " + str(self._x) + ", Y " + str(self._y) + ", Z " + str(self._z) + ", A " +
                                         str(self._A) + ", B " + str(self._B) + ", C " + str(self._C) + "}"), debug=False)  # Defines join angles

    def updateVel(self) -> None:
        # sets the speed
        self.client.write('$OV_PRO', f'{self._vel}', debug=False)

    def setVel(self, vel) -> None:
        self._vel = vel
        self.updateVel()

    # def getVel(self):
    #   return

    def setPos(self, pos) -> None:
        self._x, self._y, self._z, self._A, self._B, self._C = pos
        self._x += self.offset_x
        self.updatePos()

    def getPos(self) -> tuple:
        bla = self.client.read("$POS_ACT", debug=False)
        # # Extrair o conteúdo entre aspas simples
        # # Converter os bytes para string
        data_string = bla.decode()
        # Extrair os valores de X, Y e Z usando expressões regulares
        x_value = float(re.findall(r'X ([\d.-]+)', data_string)[0])
        y_value = float(re.findall(r'Y ([\d.-]+)', data_string)[0])
        z_value = float(re.findall(r'Z ([\d.-]+)', data_string)[0])

        return x_value, y_value, z_value

    def close(self) -> None:
        self.client.close()

    def init(self) -> None:
        self.setVel(10)
        # self.setPos(self.home)