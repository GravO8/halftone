#pip3 install opencv-python
import cv2
import numpy as np
import os

def average_pixel_color(square):
	# sum = 0
	# for i in range(len(square)):
	# 	sum += square[i]
	# return sum/len(square)
    return sum(square)/len(square)
    

def halftone(img_name, side = 40, jump = 2, bg_color = (255,255,255), circle_color = (0,0,0)):
    '''
    Arguments:
        img_name: String with the imagem name (must include the image extension)
        side: Length (in pixels) of the side of each square that composes the 
        output image
        jump: Length (in pixels) of the side of each square the program will 
        scan from original image
        bg_color: Background color of the output image (default is white)
        circle_color: Color of the circles of the output (default is black)
    '''
    if( not os.path.exists(img_name) ):
        print("can't find image ", img_name)
        return
    print("doing halftone for image: ", img_name)
    img 		  = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    print("height: {}\nwidth: {}".format(height, width))
    
    scale = side // jump
    
    remove_tmp()
    
# h = height*scale 
# while (h % side != 0):
# 	h += 1
# l = width*scale
# while(l % side != 0):
# 	l += 1
# bg 		= np.zeros( (h,l,3), np.uint8 )
# bg[:] 	= bg_color											
# 
# for y in range(0, height, jump):
# 	for x in range(0, width, jump):
# 		sel = img[y:y+jump, x:x+jump]
# 		sq 	= []
# 		for i in range(len(sel)):
# 			for l in range(len(sel[i])):
# 				sq.append( int(sel[i][l]) )
# 			intensity = average_pixel_color(sq)
# 
# 		square = np.zeros( (side, side, 3), np.uint8 )
# 		square[:] = bg_color												#BACKGROUND COLOR
# 		r = int((-0.1411764*intensity) + 25*(2**0.5))
# 		cv2.circle(square, (side//2, side//2), r, circle_color, -1)			#CIRCLE COLOR
# 		h = y*scale
# 		l = x*scale
# 		print(h,h+side, "            ", l,l+side, "\n")
# 		bg[h:h+side, l:l+side] = square
# # 
# # cv2.imwrite(img_name + " - Halftone Gradient .jpg", bg)

def remove_tmp():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(current_dir):
    	if( file.endswith(".tmp") ):
    		os.remove(file)
    
        
if __name__ == "__main__":
    #"IMG-20170712-WA0010"
    halftone("girl.jpg", jump = 5)
