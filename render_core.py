# Import modules
from PIL import Image, ImageTk
import numba as nb
import numpy as np
import math

# =========================================
# Def functions
# - HSV to RGB (HSV: 0 to 1; RGB: 0 to 255)
@nb.njit(fastmath=True)
def HSVtoRGB(h: float, s: float, v: float):
  """HSV to RGB (HSV: 0 to 1; RGB: 0 to 255)"""
  if s == 0.0:
    return v, v, v
  i = int(h*6.0)
  f = (h*6.0) - i
  p = ( v*(1.0 - s) ) * 255
  q = ( v*(1.0 - s*f) ) * 255
  t = ( v*(1.0 - s*(1.0-f)) ) *255
  i = i%6
  if i == 0:
      return v, t, p
  if i == 1:
      return q, v, p
  if i == 2:
      return p, v, t
  if i == 3:
      return p, q, v
  if i == 4:
      return t, p, v
  if i == 5:
      return v, p, q

# - Calculates Mandelbrot pixel
@nb.njit(fastmath=True)
def pixelMandelbrot(position: tuple, maxIter: int):
  """Calculate Mandelbrot pixel"""
  cR = position[0]
  cI = position[1]
  zR = 0
  zI = 0
  i = 0

  while (zR * zR) + (zI * zI) < 4 and i < maxIter:
    tmp = zR
    zR = zR ** 2 - zI ** 2 + cR
    zI = 2 * zI * tmp + cI
    i += 1

  if i == maxIter:
    return (0, 0, 0)
  else:
    #return HSVtoRGB(i/maxIter, 1, 1)
    value = int(255*i/maxIter)
    return (value, 255, 255)
    #return (int(value), int(value*.75), int(value*.5))

# Calculates Julia Set pixel
@nb.njit(fastmath=True)
def pixelJuliaSet(position: tuple, C: tuple, maxIter: int):
  """Calculate Mandelbrot pixel"""
  cR = C[0]
  cI = C[1]
  zR = position[0]
  zI = position[1]
  i = 0

  while (zR * zR) + (zI * zI) < 4 and i < maxIter:
    tmp = zR
    zR = zR ** 2 - zI ** 2 + cR
    zI = 2 * zI * tmp + cI
    i += 1

  if i == maxIter:
    return (0, 0, 0)
  else:
    #return HSVtoRGB(i/maxIter, 1, 1)
    value = int(255*i/maxIter)
    return (value, 255, 255)
    #return (int(value), int(value*.75), int(value*.5))

# - Calculates Burning Ship pixel
@nb.njit(fastmath=True)
def pixelBurningShip(position: tuple, maxIter: int):
  """Calculate Burningship pixel"""
  cR = position[0]
  cI = position[1]
  zR = zI = 0
  i = 0

  while (zR * zR) + (zI * zI) < 4 and i < maxIter:
    tmp = zR
    zR = zR ** 2 - zI ** 2 + cR
    zI = abs(2 * zI * tmp) + cI
    i += 1

  if i == maxIter:
    return (0, 0, 0)
  else:
    value = i/maxIter*255
    return ( int(math.sqrt(value) * math.sqrt(255)), int(value), int(value) )

# fractalsInfos dict
fractalsInfos = {
  "mandelbrot": 
    {"func": pixelMandelbrot,
    "mode": "HSV",
    "pos": (-0.68, 0)},
  "burningship":
    {"func": pixelBurningShip,
    "mode": "RGB",
    "pos": (0, 0)},
    "julia set":
    {"func": pixelJuliaSet,
    "mode": "HSV",
    "pos": (0, 0)}
}
# - Render function without numba to be able to use non jittable functions
def render(params, fractal: str="mandelbrot"):
  """Render function without numba for non jittable functions
  Supported fractals: mandelbrot ; burningship"""

  renderImage = np.zeros((params["res"][0], params["res"][1], 3), dtype=np.uint8)
  if fractal == "julia set":
    renderImage = optimizedRenderArg(renderImage, params["pos"], params["scale"], params["res"], fractalsInfos[fractal]["func"],params["C"],
                                                                                                                              params["maxIter"])
  else:
    renderImage = optimizedRender(renderImage, params["pos"], params["scale"], params["res"], fractalsInfos[fractal]["func"], params["maxIter"])

  return arrayToImage(renderImage, fractalsInfos[fractal]["mode"])

# - Calculate fractal image with no arguments
@nb.njit(fastmath=True)
def optimizedRender(image, position: tuple, scale: float, res: tuple, fractalFunction, maxIter: int=20):
  """Renders image with no function argument"""
  
  for y in nb.prange(int(-res[1]/2), int(res[1]/2-1)):
    # Y loop
    yPos = ((y + res[1]/4)/res[1])*scale + position[1]

    for x in range(int(-res[0]/2), int(res[0]/2-1)):
      # X loop
      image[y][x] = fractalFunction(( ((x + res[0]/4)/res[0])*scale + position[0], yPos), maxIter)

  return image

@nb.njit(fastmath=True)
def optimizedRenderArg(image, position: tuple, scale: float, res: tuple, fractalFunction, arg, maxIter: int=20):
  """Renders image with one function agrument"""
  
  for y in nb.prange(int(-res[1]/2), int(res[1]/2-1)):
    # Y loop
    yPos = ((y + res[1]/4)/res[1])*scale + position[1]

    for x in range(int(-res[0]/2), int(res[0]/2-1)):
      # X loop
      image[y][x] = fractalFunction(( ((x + res[0]/4)/res[0])*scale + position[0], yPos), arg, maxIter)

  return image

# - Convert numpy array to TKImage
def arrayToImage(array, colorSpace: str="HSV"):
  """Convert numpy array to TKImage
  colorSpace: should be "HSV" or "RGB" """

  return ImageTk.PhotoImage(image=Image.fromarray(array, mode=colorSpace))

# - Convert Image to TkImage
def imageToTK(image):
  """Convert Image to TkImage"""

  return ImageTk.PhotoImage(image=image, size=(100, 100))


