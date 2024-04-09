import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img=mpimg.imread('test.png')
img = img[:, :, 0]
print(img)