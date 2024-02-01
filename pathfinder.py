import random
import PIL.Image

def add_obstacle(area, l, h, x_anch, y_anch):
    grid_access = area.copy()
    for x in range(l):
        for y in range(h):
            if [x_anch+x, y_anch+y] in grid_access:
                grid_access.remove([x_anch+x, y_anch+y])
    return grid_access

def path_creator(map):
    path_possible = True
    step = 0
    current_pos = [map[1]] # 2 dim list
    path_pool = [current_pos] # 3 dim list (Inner: Point, Mid: Step, Outer: List)

    while map[2] not in current_pos:
        if step > map[3]*map[4]:
            path_possible = False
            break
        step += 1
        new_points = []
        for point in current_pos:
            # up
            next_point = [point[0], point[1]+1]
            if next_point in map[0]:
                point_exists = False
                for points in path_pool:
                    if next_point in points or next_point in new_points:
                        point_exists = True
                if point_exists == False:
                    new_points.append(next_point)
                    
            # right
            next_point = [point[0]+1, point[1]]
            if next_point in map[0]:
                point_exists = False
                for points in path_pool:
                    if next_point in points or next_point in new_points:
                        point_exists = True
                if point_exists == False:
                    new_points.append(next_point)
            
            # down
            next_point = [point[0], point[1]-1]
            if next_point in map[0]:
                point_exists = False
                for points in path_pool:
                    if next_point in points or next_point in new_points:
                        point_exists = True
                if point_exists == False:
                    new_points.append(next_point)

            # left
            next_point = [point[0]-1, point[1]]
            if next_point in map[0]:
                point_exists = False
                for points in path_pool:
                    if next_point in points or next_point in new_points:
                        point_exists = True
                if point_exists == False:
                    new_points.append(next_point)
        path_pool.append(new_points)
        current_pos = new_points
    if path_possible:
        path = [map[2]]

        for set in range(len(path_pool)-2, -1, -1):
            path_head = path[-1]
            poss_points = []
            for i in path_pool[set]:
                if [path_head[0], path_head[1]+1] == i or [path_head[0]+1, path_head[1]] == i or [path_head[0], path_head[1]-1] == i or [path_head[0]-1, path_head[1]] == i:
                    poss_points.append(i)
            path.append(random.choice(poss_points))

        return list(reversed(path))
    else:
        return []

def create_grid(width, height):
    grid = []
    for x in range(width):
        for y in range(height):
            grid.append([x, y])
    return grid

def add_obstacles(area):
    while True:
        if input("Exit? (y/n) ") == 'y':
            break
        else:
            length = input("Length: ")
            height = input("Height: ")
            x_coord = input("Bottom left x: ")
            y_coord = input("Bottom left y: ")
            area = add_obstacle(area, length, height, x_coord, y_coord)
            print("=====Added=====\n")
    return area

def img_to_map(img_path):
    img = PIL.Image.open(f"{img_path}")
    start = [0, 0]
    fin = [0, 0]
    grid = create_grid(img.width, img.height)

    for x in range(img.width):
        for y in range(img.height):
            if img.getpixel((x, y)) == (0, 0, 0, 255):
                grid.remove([x, img.height-y-1])
            elif img.getpixel((x, y)) == (0, 255, 0, 255):
                start = [x, img.height-y-1]
            elif img.getpixel((x, y)) == (255, 0, 0, 255):
                fin = [x, img.height-y-1]
    
    return [grid, start, fin, img.width, img.height]

def display_map(map, path):
    if path == []:
        print("No path possible")
    else:
        img_scale = round(1000 / max(map[3], map[4]))
        im = PIL.Image.new(mode = "RGB", size = (map[3], map[4]))

        pixel_map = im.load()

        for point in map[0]:
            pixel_map[point[0], point[1]] = (255, 255, 255)

        for point in path:
            pixel_map[point[0], point[1]] = (0, 0, 255)

        pixel_map[map[1][0], map[1][1]] = (0, 255, 0)
        pixel_map[map[2][0], map[2][1]] = (255, 0, 0)

        im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        im = im.resize((map[3]*img_scale, map[4]*img_scale), resample=PIL.Image.NEAREST)
        im.show()