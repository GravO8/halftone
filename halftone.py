#pip3 install opencv-python
#python3 -m pydoc halftone
#python3 halftone.py -h
import argparse
import re
import cv2
import numpy as np
import os
import sys
            

def halftone(img_name, side = 40, jump = 5, bg_color = (255,255,255), fg_color = (0,0,0), alpha = 1):
    '''
    Generates an halftone image from the image specified in img_name
    Arguments:
        img_name: String with the imagem name (must include the image extension)
        side: Length (in pixels) of the side of each square that composes the 
        output image
        jump: Length (in pixels) of the side of each square the program will 
        scan from original image
        bg_color: Background color of the output image (default is white)
        fg_color: Color of the circles of the output image (default is black)
        alpha: Float in the range ]0,2[ that determines how big the circles can
        be. When alpha has the default value of 1, the maximum radius is side/2
    '''
    if( not os.path.exists(img_name) ):
        print("can't find image", img_name)
        return
    print("Halftone for image:", img_name)
    bg_color      = bg_color[::-1] 
    fg_color      = fg_color[::-1] 
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
            cv2.circle(output_square, (side//2, side//2), radius, fg_color, -1)
            canvas[y_output:y_output+side, x_output:x_output+side] = output_square
            x_output += side
        y_output += side
        x_output = 0
    cv2.imwrite("out-"+img_name, canvas)
    print("done!")
    
    
def output_img_dimensions(height, width, scale, side):
    '''
    Computes the dimensions of the output image and makes sure they are a 
    multiple of side
    Returns the output image width and height 
    '''
    height_output = height * scale
    if(height_output % side != 0):
        height_output += side - height_output % side
    width_output = width*scale 
    if(width_output % side != 0):
        width_output += side - width_output % side
    return height_output, width_output
    
    
def square_avg_value(square):
    '''
    Calculates the average grayscale value of the pixels in a square of the 
    original image 
    Argument:
        square: List of N lists, each with N integers whose value is between 0 
        and 255
    '''
    sum = 0
    n = 0
    for row in square:
        for pixel in row:
            sum += pixel
            n += 1
    return sum/n
    
    
def str_to_rgb(str):
    '''
    Receives a string with a rgb value and returns a tuple with the 
    corresponding rgb value
    '''
    split = str[1:-1].split(",")
    return (int(split[0]), int(split[1]), int(split[2]))
    
    
def get_args():
    '''
    Reads and parses the arguments from the command line
    '''
    def rgb_color(arg, pat = re.compile("\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3}\)")):
        if( pat.match(arg) and
            int(arg[1:-1].split(",")[0]) < 256 and
            int(arg[1:-1].split(",")[1]) < 256 and
            int(arg[1:-1].split(",")[2]) < 256 ):
            return arg
        raise argparse.ArgumentTypeError("invalid rgb value")
    parser = argparse.ArgumentParser(description = "Generate halftone images")
    parser.add_argument("file", help = "Image file name (with image extension)")
    parser.add_argument("-s", "--side", help = "Length (in pixels) of the side"+
    " of each square that composes the output image", type = int, default = 40)
    parser.add_argument("-j", "--jump", help = "Length (in pixels) of the side"+
    " of each square the program will scan from original image", type = int, default = 5)
    parser.add_argument("-bg", "--bg_color", help = "Background color of the " +
    "output image (default is white)", default = "(255,255,255)", type = rgb_color)
    parser.add_argument("-fg", "--fg_color", help = "Color of the circles of " +
    "the output image (default is black)", default = "(0,0,0)", type = rgb_color)
    parser.add_argument("-a", "--alpha", help = "Float in the range ]0,2[ that"+
    " determines how big the circles can be. When alpha has the default value "+
    "of 1, the maximum radius is side/2", type = float, default = 1)
    args = parser.parse_args()
    return args
        
if __name__ == "__main__":
    args = get_args()
    print(args)
    halftone(args.file, 
            side = args.side, 
            jump = args.jump,
            bg_color = str_to_rgb(args.bg_color),
            fg_color = str_to_rgb(args.fg_color),
            alpha = args.alpha)
    
