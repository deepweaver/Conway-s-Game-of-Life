#!/usr/bin/python
import numpy as np

import argparse 
import os, sys 

parser = argparse.ArgumentParser(description="Conway's Game of Life")
parser.add_argument('--animation', action='store_true', default=False, \
    help="by default we have a graphical display, if you don't like it, you can disable it" )
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

# print(board) 


m = n = 100 # random board size 
ON = 1
OFF = 0
vals = [ON, OFF]
grid = None 
generations = 1000
output = [] 
# populate grid with random on/off - more off than on





if args.random_init:
    grid = np.random.choice(vals, m*n, p=[0.2, 0.8]).reshape(m, n)
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
                    # print("{},{} is on".format(i,j))
    if x > generations:
        return None
    output.append(newGrid)
    grid = newGrid 
    if args.animation:
        # print(newGrid) 
        mat.set_data(newGrid)

        return [mat]




if args.animation:
    import matplotlib.pyplot as plt 
    import matplotlib.animation as animation
    fig, ax = plt.subplots()
    mat = ax.matshow(grid)
    ani = animation.FuncAnimation(fig, update, interval=250, save_count=5, repeat=False )
    plt.show()

else:
    for i in range(generations):
        update(i) 

# print(output)
with open(args.outputfile, 'w') as file:
    for i, v in enumerate(output):
        file.write("Generation {}\n".format(i))
        for j in range(output[i].shape[0]):
            for k in range(output[i].shape[1]):
                file.write("{}".format(output[i][j,k])) 
            file.write("\n") 











