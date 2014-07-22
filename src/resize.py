#!/usr/bin/python

import PIL
from PIL import Image
import sys
import os
from PIL import ImageOps

""" 
Resizes images to a given size, retaining the target aspect ratio, with no stretching. WARNING: Will crop images

Resizing on the SimpleImage PHP class by Simon Jarvis
http://www.white-hat-web-design.co.uk/articles/php-image-resizing.php
"""

#Divides two numbers
def divide(x,y):
	return float(x)/float(y)

#Gets the filenames from the command-line arguments
def get_files_from_args():
	files = []
	if(len(sys.argv) > 3):
		for args in sys.argv[1:len(sys.argv) -2]:
			files.append(args)
	return files

#Gets the target size from the command-line arguments
def get_size_from_args():
	sys_len = len(sys.argv)
	return (int(sys.argv[sys_len - 1]), int(sys.argv[sys_len - 2]))

def resize(image, size):
        return image.resize(size,Image.ANTIALIAS)

#Regular resizing - not very good
def resize_images(files,size):
	for file in files:
	        try :
	                image = Image.open(file)

	                filename, ext = os.path.splitext(file)
	                image.thumbnail(size, PIL.Image.ANTIALIAS)
	                image.save(filename + "-resized" + ext)
	        except IOError:
	                print "File " + file + " not found"

#Crops an image to a height
def crop_to_height(image,theight,twidth):
	width,height = image.size
	diff = height - theight
	y = diff/2
		
	left = 0
	right = width
	bottom = height - y
	top = y

	return image.crop((left,top,right,bottom))

#Crops an image to a width
def crop_to_width(image,theight,twidth):
	width,height = image.size
	diff = width - twidth
	x = diff/2	
	left = x
	right = width - x
	bottom = height
 	top = 0

	return image.crop((left,top,right,bottom))

#Resizes an image to a width
def resize_to_width(image,twidth):
	width,height = image.size
	ratio = divide(twidth,width)
	height = height * ratio
	return resize(image, (int(twidth), int(height)))

#Resies an image to a height
def resize_to_height(image,theight):
	width,height = image.size
	ratio = divide(theight,height)
	width = width * ratio
	return resize(image,(int(width),int(theight)))

#Clean resizing, with no stretching
def resize_super_intelligent(files,size):
	for file in files:
		try:
			image = Image.open(file)
			
			filename, ext = os.path.splitext(file)
			
			width, height = image.size
			twidth, theight = size
			w_ratio = divide(twidth, width)
			h_ratio = divide(theight,height)
			if((height * w_ratio) >= theight):
				image = resize_to_width(image,twidth)
				image = crop_to_height(image,theight,twidth)
			elif((width * h_ratio) >= twidth):
				image = resize_to_height(image,theight)
				image = crop_to_width(image, theight, twidth)
			
			image = resize(image,size)
			image.save(filename + "-resized" + ext)
		except IOError:
			print "File " + file + " not found"

resize_super_intelligent(get_files_from_args(), get_size_from_args())

