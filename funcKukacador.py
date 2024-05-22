import numpy as np

def calculaPosTelaC(u,v,Z,f,ro_h,ro_w)->list:
  x = ro_w*(u-230)*Z/f #metade do comprimento da imagem cortada adquirida
  y = ro_h*(v-135)*Z/f  # metade da altura da imagem cortada adquirida
  return [x,y,Z]

def calculaPosKukaB(pos,mHom)->tuple:
  print(pos)
  posC = np.array(pos)
  print(posC)
  posB = np.matmul(mHom,posC)
  return posB
