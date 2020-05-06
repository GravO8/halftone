#pip3 install opencv-python
#python3 -m pydoc halftone
#python3 halftone.py -h
import argparse
import re
import cv2
import numpy as np
from math import ceil
import os
import sys
            

def halftone(img_name, side = 20, jump = None, bg_color = (255,255,255), fg_color = (0,0,0), alpha = 1.4):
    '''
    Generates an halftone image from the image specified in img_name
    Arguments:
        img_name (required)- String with the image name (must include the image
        extension)
        side (optional)- Length (in pixels) of the side of each square that 
        composes the output image (default is 20)
        jump (optional)- Length (in pixels) of the side of each square the 
        program will scan from original image (default is 0.7% of the minimum 
        between the width and height)
        bg_color (optional)- Background color of the output image (default is 
        white)
        fg_color (optional)- Color of the circles of the output image (default 
        is black)
        alpha (optional)- Float (greater than 0) that determines how big the 
        circles can be. When alpha is 1, the maximum radius is side/2 (default
        is 1.4)
    '''
    assert os.path.exists(img_name), "can't find image {}".format(img_name)
    assert side > 0, "side must be greater than 0"
    assert alpha > 0, "alpha must be greater than 0"
    print("Halftone for image", img_name)
    bg_color      = bg_color[::-1] 
    fg_color      = fg_color[::-1] 
    img 		  = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    if(jump == None):
        jump = ceil(min(height,height)*0.007)
    assert jump > 0, "jump must be greater than 0"
    print("height: {}, width: {}, side: {}, jump: {}, bg_color: {}, fg_color: {}, alpha: {}".format(height, width, side, jump, bg_color, fg_color, alpha))
    
    height_output, width_output = side*ceil(height/jump), side*ceil(width/jump)
    canvas 	      = np.zeros((height_output,width_output,3), np.uint8)
    canvas[:]     = bg_color
    output_square = np.zeros((side, side, 3), np.uint8)
    
    x_output, y_output = 0, 0
    for y in range(0, height, jump):
        for x in range(0, width, jump):
            output_square[:] = bg_color
            intensity        = 1 - square_avg_value(img[y:y+jump, x:x+jump])/255
            radius           = int(alpha*intensity*side/2)
            cv2.circle(output_square, (side//2,side//2), radius, fg_color, -1)
            canvas[y_output:y_output+side, x_output:x_output+side] = output_square
            x_output += side
        y_output += side
        x_output = 0
    cv2.imwrite("out-"+img_name, canvas)
    print("done!")
    
    
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
    parser.add_argument("file", help = "(required)- String with the image name"+
    " (must include the image extension")
    parser.add_argument("-s", "--side", help = "(optional)- Length (in pixels)"+
    " of the side of each square that composes the output image (default is 20)"
    , type = int, default = 20)
    parser.add_argument("-j", "--jump", help = "(optional)- Length (in pixels)"+
    " of the side of each square the program will scan from original image (de"+
    "fault is 0.7%% of the minimum between the width and height)", type = int)
    parser.add_argument("-bg", "--bg_color", help = "(optional)- Background co"+
    "lor of the output image (default is white)", default = "(255,255,255)", 
    type = rgb_color)
    parser.add_argument("-fg", "--fg_color", help = "(optional)- Color of the "+
    "circles of the output image (default is black)", default = "(0,0,0)", type 
    = rgb_color)
    parser.add_argument("-a", "--alpha", help = "(optional)- Float (greater th"+
    "an 0) that determines how big the circles can be. When alpha is 1, the ma"+
    "ximum radius is side/2 (default is 1.4)", type = float, default = 1.4)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    halftone(args.file, 
            side = args.side, 
            jump = args.jump,
            bg_color = str_to_rgb(args.bg_color),
            fg_color = str_to_rgb(args.fg_color),
            alpha = args.alpha)
    
