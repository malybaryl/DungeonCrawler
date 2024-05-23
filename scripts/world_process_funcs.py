import csv

def process_1_ground_csv(type, cols, rows, level):  
    world_data = [[-1] * cols for _ in range(rows)]
    with open(f"assets/levels/{level}/{type}_ground.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)        
    return world_data

def process_2_decoration_dows_csv(type, cols, rows, level):
    world_decoration_down_data = [[-1] * cols for _ in range(rows)]
    with open(f"assets/levels/{level}/{type}_decorations_down.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_decoration_down_data[x][y] = int(tile)
    return world_decoration_down_data

def process_3_decorations_up_csv(type, cols, rows, level):  
    world_decoration_up_data = [[-1] * cols for _ in range(rows)]
    with open(f"assets/levels/{level}/{type}_decorations_up.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_decoration_up_data[x][y] = int(tile)
    return world_decoration_up_data

def process_4_walls_csv(type, cols, rows, level):  
    walls = [[-1] * cols for _ in range(rows)]
    with open(f"assets/levels/{level}/{type}_walls.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                walls[x][y] = int(tile)
    return walls

def process_5_mobs_and_objects_csv(type, cols, rows, level): 
    world_mobs_data = [[-1] * cols for _ in range(rows)]   
    with open(f"assets/levels/{level}/{type}_mobs_and_objects.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_mobs_data[x][y] = int(tile)
    return world_mobs_data

def process_6_ground2_csv(type, cols, rows, level):  
    world_data2 = [[-1] * cols for _ in range(rows)]
    with open(f"assets/levels/{level}/{type}_ground2.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data2[x][y] = int(tile)
    return world_data2    