#pip3 install opencv-python
import cv2
import numpy as np
import os

def average(square):
	soma = 0
	for i in range(len(square)):
		soma += square[i]
	return (soma/len(square))

image = "IMG-20170712-WA0010"
img 			= cv2.imread(image + ".jpg", 0)
height, width 	= img.shape
print("altura: ", height)
print("largura: ", width)
side 			= 40				#tamanho dos 'pixels' que teem os circulos 
jump			= 2					#numero de pixels saltados na imagem original
factor 			= side//jump
#AS CORES ESTAO EM BGR EM VEZ DE RGB
#cor clara
bg_color 		= (255,195,255)
#cor escura
circle_color 	= (97,0,199)

h = height*factor 
while (h % side != 0):
	h += 1
l = width*factor
while(l % side != 0):
	l += 1
bg 		= np.zeros( (h,l,3), np.uint8 )
bg[:] 	= bg_color											

for y in range(0, height, jump):
	for x in range(0, width, jump):
		sel = img[y:y+jump, x:x+jump]
		sq 	= []
		for i in range(len(sel)):
			for l in range(len(sel[i])):
				sq.append( int(sel[i][l]) )
			intensity = average(sq)
		
		square = np.zeros( (side, side, 3), np.uint8 )
		square[:] = bg_color												#BACKGROUND COLOR
		r = int((-0.1411764*intensity) + 25*(2**0.5))
		cv2.circle(square, (side//2, side//2), r, circle_color, -1)			#CIRCLE COLOR
		h = y*factor
		l = x*factor
		print(h,h+side, "            ", l,l+side, "\n")
		bg[h:h+side, l:l+side] = square

cv2.imwrite(image + " - Halftone Gradient .jpg", bg)


current_dir = os.path.dirname(os.path.realpath(__file__))
for file in os.listdir(current_dir):
	if( file.endswith(".tmp") ):
		os.remove(file)
