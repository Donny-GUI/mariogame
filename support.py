from PIL import Image
from csv import reader
from settings import tile_size
from os import walk, getcwd, sep, path, listdir
import pygame


def import_folder(path_: str) -> list:
	surface_list = []

	if not path.exists(path_):
		cwd = getcwd()
		_path = cwd + sep + path_.replace("/", sep)
	else:
		_path = path_ 

	for _,__,image_files in walk(_path):
		for image in image_files:
			full_path = _path + sep + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def import_csv_layout(path: str) -> list[list]:
	terrain_map = []
	realpath = getcwd() + sep + path
	with open(realpath) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_cut_graphics(path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / tile_size)
	tile_num_y = int(surface.get_size()[1] / tile_size)
	cut_tiles = []

	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_size
			y = row * tile_size
			new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
			cut_tiles.append(new_surf)

	return cut_tiles


def image_to_pixel_matrix(image_path: str) -> list[list[tuple[int, int, int, int]]]:
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixel_data = list(image.getdata())
    width, height = image.size
    pixel_matrix = [pixel_data[i:i+width] for i in range(0, len(pixel_data), width)]
    return pixel_matrix

def convert_background_to_alpha(input_path:str, output_path: str="") -> None:
	"""
	Convert a png file to a alpha-channel enabled png. it takes 
	"""

	output_path = input_path if output_path == "" else output_path
	image_object = Image.open(input_path)
	image_rgba = image_object.convert("RGBA")
	pixel_data = list(image_rgba.getdata())
	target_col = pixel_data[0]
	target_color = target_col[:-1]

	print("target color: ", target_color)

	def determine_alpha_color(input_image: str) -> tuple[int, int, int]:
		
		pixel_matrix = image_to_pixel_matrix(input_image)
		top_horizontal_line = pixel_matrix[0]
		left_vertical_line = [x[0] for x in pixel_matrix]
		bottom_horizontal_line = pixel_matrix[len(pixel_matrix)-1]
		last_index = len(top_horizontal_line) - 1
		last_horizontal_line = [x[last_index] for x in pixel_matrix]
		all_pixels = top_horizontal_line + left_vertical_line + bottom_horizontal_line + last_horizontal_line

		colors = {}
		px_pairs = {}

		for px in all_pixels:

			strpx = str(px)

			try:
				colors[strpx]+=1
			except KeyError:
				colors[strpx] = 1
				px_pairs[strpx] = px

		bestname = ""
		bestcolor = 0

		for name in px_pairs:

			val = colors[name]
			if val > bestcolor:
				bestname = name
				bestcolor = val
		
		retval = px_pairs[bestname]
		
		if len(retval) > 3:
			return retval[:-1]
		else:
			return retval

	def process_pixel(pixel, target_color=target_color) -> tuple[int, int, int, int]:
		r, g, b, a = pixel
		if (r, g, b) == target_color:
			return (r, g, b, 0)  # Set alpha to 0 for the target color
		else:
			return (r, g, b, a)  # Keep the original alpha for other colors

	# Process all pixels
	new_pixel_data = [process_pixel(pixel) for pixel in pixel_data]
	image_rgba.putdata(new_pixel_data)
	image_rgba.save(output_path)


def test():
	testpath = "C:\\Users\\donald\Desktop\\mariogame\\graphics\\character\\fall\\0.png"
	testoutputpath = "C:\\Users\\donald\Desktop\\mariogame\\graphics\\character\\fall\\test.png"
	convert_background_to_alpha(testpath, testoutputpath)

def fix_diddy_alpha():
	exit()
	path = "C:\\Users\\donald\Desktop\\mariogame\\graphics\\character\\"
	for subdir in ["fall", "idle", "jump", "run", "walk"]:
		fullpath = path + subdir + "\\"
		thefiles = [fullpath + x for x in listdir(fullpath)]
		for file in thefiles:
			print(file)
			convert_background_to_alpha(file)



	