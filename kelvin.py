# Title: Project #1		Name: David Cackette			Date: 2/11/2015

# Abstract: Takes a .jpg image, makes a copy of and renames it, then applies Instagram-style filters to it.

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
			outfile = "me-kelvin.jpg"
			Image.open(self.filename).save(outfile)
			self.im = Image.open(outfile)
		return self.im
	
	def execute(self, command, **kwargs): # Cuts the filename down to before the ".jpg" (4 characters)
		filename2 = self.filename[:len(self.filename)-4] + "-kelvin.jpg"
		default = dict(	
			filename = filename2,
			width = self.image().size[0],
			height = self.image().size[1]
		)
		format = dict(default.items() + kwargs.items())
		command = command.format(**format)
		error = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
		return error
		
	def colortone(self, color, level, type = 0):origin # Defines how to change the colors of the image
		
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

class Frame(Filter): # Applies the frame to the image
				
	def frame(self, frame):
		path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.execute("convert {filename} \( '{frame}' -resize {width}x{width}! -unsharp 1.5x1.0+1.5+0.02 \) -flatten {filename}",
			frame = os.path.join(path, "frames", frame)
		)

class Kelvin(Filter, Frame): # Modifies the image's colors
	
	def apply(self):
		self.execute("convert \( {filename} -auto-gamma -modulate 120,50,100 \) \( -size {width}x{height} -fill 'rgba(255,153,0,0.5)' -draw 'rectangle 0,0 {width},{height}' \) -compose multiply {filename}");
		self.frame("Kelvin.jpg");

f = Kelvin("me.jpg") # Tells what file (me.jpg) and what filter (Kelvin) to apply
f.apply() # Applies the filter