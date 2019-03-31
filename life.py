#!/usr/bin/python 
#encoding=utf-8
# just use python3 xxx to run the program
import numpy as np

import argparse 
import os, sys 

parser = argparse.ArgumentParser(description="Conway's Game of Life")
parser.add_argument('--animation', action='store_true', default=False, \
    help="we have a graphical display. If you don't like it or you don't \
    have matplotlib installed, you can disable it by ignoring this option" )
parser.add_argument('--inputfile', type=str, default='./inLife.txt', metavar='I', \
    help="specify input file path") 
parser.add_argument('--outputfile', type=str, default='./outLife.txt', metavar='O', \
    help="specify output file path. If not exist, the program will create one") 
parser.add_argument('--random_init', action='store_true', default=False, \
    help="If you don't have any input file, we can random generate initial state. In this case \
    the animation option will be automatically turned on") 

args = parser.parse_args() 
args.animation = True if args.random_init == True else args.animation 
if not os.path.exists(args.inputfile):
    print("can't find input file")
    sys.exit(1) 


np.random.seed(0) 



m = n = 100 # random board size, m is the height, n is the width 
ON = 1 # description of cell state, 1 for live, 0 for dead 
OFF = 0
grid = None 
generations = 1000 # maximum generation number
output = [] 





# populate grid with random on/off - more off than on
if args.random_init:
    grid = np.random.choice([ON, OFF], m*n, p=[0.2, 0.8]).reshape(m, n)
else: # else read from args.inputfile 
    board = [] 
    with open(args.inputfile, 'r') as file:
        for i, line in enumerate(file.readlines()):
            line = line.strip(' ').strip('\n') 

            if i == 0:
                generations = int(line.strip(' ')) 
                # print(generations)
            else: 
                board.append([ON if int(e) == 1 else OFF for i, e in enumerate(line)])
    grid = np.array(board) 
    m, n = grid.shape 
output.append(grid) 
x = 0







def update(data):
    global grid, x 
    x += 1
    newGrid = grid.copy()
    for i in range(m):
        for j in range(n):
            total = (grid[i, (j-1)%n] + grid[i, (j+1)%n] + 
                    grid[(i-1)%m, j] + grid[(i+1)%m, j] + 
                    grid[(i-1)%m, (j-1)%n] + grid[(i-1)%m, (j+1)%n] + 
                    grid[(i+1)%m, (j-1)%n] + grid[(i+1)%m, (j+1)%n])
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    '''
        Two for loops iterate over each cell. For each cell, 
        the ‘total’ stores the number of surrounding live 
        neighbor cells out of 8 neighbors, live or dead. 
        If the center cell, which has index [i,j], lives, 
        and if it has too few live neighbors(<2) or too many(>3), 
        the central cell dies of underpopulation or overpopulation 
        respectively. This also means the central cell with 
        2 or 3 neighbors lives on to the next generation. 
        However, if the central cell is dead and it has exactly 3 
        neighbors, it becomes a live cell as if by reproduction.
    '''
    if x > generations:
        return None
    output.append(newGrid)
    grid = newGrid 
    if args.animation:
        mat.set_data(newGrid)
        return [mat]




# use animation option
if args.animation:
    import matplotlib.pyplot as plt 
    import matplotlib.animation as animation
    fig, ax = plt.subplots()
    mat = ax.matshow(grid)
    ani = animation.FuncAnimation(fig, update, interval=250, save_count=5, repeat=False )
    plt.show()
else: # normal update
    for i in range(generations):
        update(i) 






# write output file

with open(args.outputfile, 'w') as file:
    for i, v in enumerate(output):
        file.write("Generation {}\n".format(i))
        for j in range(output[i].shape[0]):
            for k in range(output[i].shape[1]):
                file.write("{}".format(output[i][j,k])) 
            file.write("\n") 











