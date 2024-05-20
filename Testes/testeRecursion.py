def teste(x):
  if x>6:
    return "Acabou"
  else:
    print(x)
    teste(x+1)

teste(0)