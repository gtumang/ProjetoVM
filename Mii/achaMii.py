from tkinter import *
import cv2
import matplotlib.pyplot as plt
import numpy as np
from lib.kukaMov import Kuka
import lib.funcKukacador as funcKukacador
from math import cos, sin, pi, sqrt

DIST_Y_ROB = 865  # mm


def troca_saida(tempPath):
    global templatePath
    templatePath = tempPath


root = Tk()
root.geometry("500x500")
root.title('Escolher Alvo')
root.config(background='white')

quit_button = Button(root, text='Alvo escolhido', command=root.destroy)

quit_button.place(x=380, y=400)

img_pessoa1 = PhotoImage(file='img_proj/pessoa1.png')
pessoa1 = Button(root, image=img_pessoa1,
                 command=lambda *args: troca_saida('pessoa1.bmp'))

pessoa1.place(x=10, y=110)

img_pessoa2 = PhotoImage(file='img_proj/pessoa2.png')
pessoa2 = Button(root, image=img_pessoa2,
                 command=lambda *args: troca_saida('pessoa2.bmp'))

pessoa2.place(x=110, y=110)

img_pessoa3 = PhotoImage(file='img_proj/pessoa3.png')
pessoa3 = Button(root, image=img_pessoa3,
                 command=lambda *args: troca_saida("pessoa3.bmp"))

pessoa3.place(x=210, y=110)

root.mainloop()

# -----------------------------------------------------------------------------------------------------------------#
cap = cv2.VideoCapture(cv2.CAP_DSHOW)

_, img_pessoas_raw = cap.read(cv2.IMREAD_GRAYSCALE)

img_pessoas = cv2.cvtColor(img_pessoas_raw, cv2.COLOR_BGR2GRAY)[
    50:-170, 50:-50]

h, w = img_pessoas.shape

img = img_pessoas.copy()
assert img is not None, "file could not be read, check with os.path.exists()"
img2 = img.copy()
template = cv2.imread("img_proj/"+templatePath, cv2.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

img = img2.copy()
method = eval(methods[1])
# Apply template Matching
res = cv2.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    top_left = min_loc
else:
    top_left = max_loc

bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(img, top_left, bottom_right, 255, 2)

centro_imagem = (int((bottom_right[0]+top_left[0])/2),
                 int((bottom_right[1]+top_left[1])/2))


rob = Kuka('192.168.50.205', 7000)

alpha = -pi/2

H_tB = np.array([[1,     0,         0,        -60],
                 [0, cos(alpha), -sin(alpha), DIST_Y_ROB],
                 [0, sin(alpha), cos(alpha),   320],
                 [0,     0,         0,        1]])

#--------------------------------------------------------------------------------------------------------------#

RobPos = funcKukacador.image2kuka(centro_imagem, H_tB)

if rob.connect():
    print("Robô conectado")
    rob.init()
    rob.setVel(40)
    rob.setPos(RobPos)
    rob.close()

#--------------------------------------------------------------------------------------------------------------#

img = cv2.circle(img, centro_imagem, radius=4, color=(0, 0, 255), thickness=3)

plt.subplot(121), plt.imshow(res, cmap='gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img, cmap='gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle(method)

plt.show()
