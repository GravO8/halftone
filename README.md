# Halftone

This is a very simple python program that uses [open cv](https://docs.opencv.org/master/index.html) to generate images using the [halftone technique](https://en.wikipedia.org/wiki/Halftone).

## Command line usage

Put the source image in the same directory as halftone.py and call it like so:

`python3 halftone.py woman.jpg`

![command-line-usage](https://user-images.githubusercontent.com/25433159/81508242-f51cb500-92fa-11ea-9bf2-14ce45190288.jpg)

You can also learn about the optional arguments, doing so: `python3 halftone.py -h`



## Calling from another module

```python
import halftone

halftone.halftone("woman.jpg")
```

Learn more about the methods' signature and behaviour with `python3 -m pydoc halftone`



## Optional arguments

#### Side

The generated image is composed of squares with dots in them. This optional argument specifies how big each of these squares can be. 

Bellow is a series of images generated with different values of `side` which hopefully helps you visualize how this variable affects the image's size and smoothness. 

![side-variation](https://user-images.githubusercontent.com/25433159/81510498-f6a1a980-9309-11ea-8484-74d2c36a5986.jpg)

If you set `side = 1`, you won't get very good results (because each square will effectively be just one pixel). 

If you set `side = 2` each square will be 2 pixels wide and although you probably won't get a very clear image, you get a cool looking texture if you zoom in enough. 

Values of `side` that are too large create big images that may take a while to generate. 

The default `side` value is 20 pixels because from my experience playing with this variable, 20 gives you a nice equilibrium between image size and image smoothness. 