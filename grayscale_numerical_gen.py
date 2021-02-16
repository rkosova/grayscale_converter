from PIL import Image, ImageDraw

class GrayscaleConvert():
	def __init__(self, img):
		"""Constructor for GrayscaleConvert. Sets up width and height variables. 

		:param img: PIL Image object of image to be grayscaled
		:type img: PIL Image object of any type
		"""
		self.pre_image = img
		self.width, self.height = self.pre_image.size

	def convert_num(self, algorithm="average"):
		"""Convert to a matrix of RGB values representing a gray RGB value based on the chosen algorithm.
		
		:param algorithm: determines the algorithm to generate the grayscale values, defaults to "average"
				"average" for averaging out the RGB values
				"highest" for the highest value out of the RGB values
				"upper_average" for the average of the two highest values of the RGB values
				"middle_average" for the average of the highest and lowest values of the RGB values
		:type algorithm: string

		:rtype: list
		:return: a height x width dimensional list with each nested list representing the RGB gray value for each row of pixels on the image (top to bottom)
		"""

		def compare_three(a, b, c):
			# to be optimized
			if (a>b) & (a>c): return a 
			elif (b>a) & (b>c): return b 
			elif (c>a) & (c>b): return c 
			else: return a

		def compare_three_upper(a, b, c):
			# to be optimized
			_l = [a, b, c]
			_l.sort(reverse=True)
			return _l


		entire = []
		for y in range(self.height):
			row = []
			for x in range(self.width):
				_r, _g, _b = self.pre_image.getpixel((x, y))
				if algorithm == "average":
					avg = (_r + _g +_b)//3
					row.append(avg)
				elif algorithm == "highest":
					highest = compare_three(_r, _g, _b)
					row.append(highest)
				elif algorithm == "upper_average":
					upper_avg = sum(compare_three_upper(_r, _g, _b)[:2])//2
					row.append(upper_avg)
				elif algorithm == "middle_average":
					_l = compare_three_upper(_r, _g, _b)
					middle_avg = (_l[0] + _l[2])//2
					row.append(middle_avg)

			entire.append(row)

		return entire


	def convert_image(self, numerical_matrix, fname):
		"""Takes the already grayscaled numerical image matrix and turns it into a png
		
		:param numerical_matrix: matrix of grayscaled image data (typically generated by GrayscaleConvert.convert_num())			
		:type numerical_matrix: list

		:param fname: image saved with this file name
		:type fname: string

		:return: saved image
		"""
		new_img = Image.new("RGB", (self.width, self.height), (0,0,0))
		drw = ImageDraw.Draw(new_img)
		
		for y in range(self.height):
			for x in range(self.width):
				rgb = numerical_matrix[y][x]
				new_img.putpixel((x, y), (rgb, rgb, rgb))

		new_img.save("%s.png" % fname)
