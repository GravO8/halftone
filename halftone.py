#pip3 install opencv-python
import cv2
import numpy as np
import os, sys

def output_img_dimensions(height, width, scale, side):
    height_output  = height * scale
    if(height_output % side != 0):
        height_output += side - height_output % side

    width_output   = width*scale 
    if(width_output % side != 0):
        width_output  += side - width_output % side
    
    return height_output, width_output
    
    
def square_avg_value(square):
    sum = 0
    n = 0
    for row in square:
        for pixel in row:
            sum += pixel
            n += 1
    return sum/n
    
    
def remove_tmp():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(current_dir):
    	if( file.endswith(".tmp") ):
    		os.remove(file)
            

def halftone(img_name, side = 40, jump = 2, bg_color = (255,255,255), circle_color = (0,0,0), alpha = 1):
    '''
    Arguments:
        img_name: String with the imagem name (must include the image extension)
        side: Length (in pixels) of the side of each square that composes the 
        output image
        jump: Length (in pixels) of the side of each square the program will 
        scan from original image
        bg_color: Background color of the output image (default is white)
        circle_color: Color of the circles of the output (default is black)
        alpha: Float in the range ]0,2[ that determines how big the circles can
        be. When alpha has the default value of 1, the maximum radius is side/2
    '''
    if( not os.path.exists(img_name) ):
        print("can't find image", img_name)
        return
    print("Halftone for image:", img_name)
    bg_color      = bg_color[::-1]
    circle_color  = circle_color[::-1]
    img 		  = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    
    scale = side // jump
    height_output, width_output = output_img_dimensions(height, width, scale, side)
        
    canvas 	      = np.zeros((height_output,width_output,3), np.uint8)
    canvas[:]     = bg_color
    output_square = np.zeros((side, side, 3), np.uint8)
    
    x_output, y_output = 0, 0
    for y in range(0, height, jump):
        for x in range(0, width, jump):
            output_square[:] = bg_color
            intensity        = 1 - square_avg_value(img[y:y+jump, x:x+jump])/255
            radius           = int(alpha*intensity*side/2)
            cv2.circle(output_square, (side//2, side//2), radius, circle_color, -1)
            canvas[y_output:y_output+side, x_output:x_output+side] = output_square
            x_output += side
        y_output += side
        x_output = 0
    cv2.imwrite("out-"+img_name, canvas)
    print("done!")
    remove_tmp()
    
        
if __name__ == "__main__":
    halftone("girl.jpg", jump=5)
