import pathfinder as pf

ref_img = "maze_1"        
pf.display_map(pf.img_to_map(f"{ref_img}.png"), pf.path_creator(pf.img_to_map(f"{ref_img}.png")))
