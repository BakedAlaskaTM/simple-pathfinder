import pathfinder as pf
import linecache
import PIL.Image

ref_img = "maze_1"

width, height = pf.img_to_map(f'{ref_img}.png')[3:5]

