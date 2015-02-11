# Title: Project #1		Name: David Cackette			Date: 2/11/2015

# Abstract: Takes an image, makes a copy of and renames it, then applies Instagram-style filters to it.

import math
import os, inspect
import subprocess
from PIL import Image

class Filter:
	
	def __init__(self, filename): # Constructor
		self.filename = filename
		self.im = False
		
	def image(self): # Sets the new filename, opens the file and saves it as the new file, then opens the new file
		if not self.im:
			outfile = "me-toaster.jpg"
			Image.open(self.filename).save(outfile)
			self.im = Image.open(outfile)
		return self.im
	
	def execute(self, command, **kwargs): # Cuts the filename down to before the ".jpg" (4 characters)
		filename2 = self.filename[:len(self.filename)-4] + "-toaster.jpg"
		default = dict(	
			filename = filename2,
			width = self.image().size[0],
			height = self.image().size[1]
		)
		format = dict(default.items() + kwargs.items())
		command = command.format(**format)
		error = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
		return error
		
	def colortone(self, color, level, type = 0): # Defines how to change the colors of the image
		
		arg0 = level
		arg1 = 100 - level
		if type == 0:
			negate = '-negate'
		else:
			negate = ''

		# Sets up the modifications of the image's colors
		self.execute("convert {filename} \( -clone 0 -fill '{color}' -colorize 100% \) \( -clone 0 -colorspace gray {negate} \) -compose blend -define compose:args={arg0},{arg1} -composite {filename}",
			color = color,
			negate = negate,
			arg0 = arg0,
			arg1 = arg1
		)

class Vignette(Filter): # Applies the vignette to the image

	def vignette(self, color_1 = 'none', color_2 = 'black', crop_factor = 1.5):
		crop_x = math.floor(self.image().size[0] * crop_factor)
		crop_y = math.floor(self.image().size[1] * crop_factor)
		 
		self.execute("convert \( {filename} \) \( -size {crop_x}x{crop_y} radial-gradient:{color_1}-{color_2} -gravity center -crop {width}x{height}+0+0 +repage \) -compose multiply -flatten {filename}",
			crop_x = crop_x,
			crop_y = crop_y,
			color_1 = color_1,
			color_2 = color_2,
		)

class Border(Filter): # Applies the border to the image
	
	def border(self, color = 'black', width = 20):
		self.execute("convert {filename} -bordercolor {color} -border {bwidth}x{bwidth} {filename}",
			color = color,
			bwidth = width
		)

class Toaster(Filter, Vignette, Border): # Modifies the image's colors
	
	def apply(self):
		self.colortone('#330000', 50, 0)
		self.execute("convert {filename} -modulate 150,80,100 -gamma 1.2 -contrast -contrast {filename}");
		self.vignette('none', 'LavenderBlush3');
		self.vignette('#ff9966', 'none');
		self.border('white')

f = Toaster("me.jpg") # Tells what file (me.jpg) and what filter (Toaster) to apply
f.apply() # Applies the filter