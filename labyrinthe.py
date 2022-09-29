import math
import random
import matplotlib.pyplot as plt

class Labyrinthe:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[{'zone': i*width+j, 'N': False, 'S': False, 'E': False, 'W': False} for j in range(width)] for i in range(height)]
    
    def merge(self, i, j, direction):
        cell1 = self.cells[i][j]
        if cell1[direction] == True:
            return False
        if direction == 'N':
            if i == 0:
                return False
            cell2 = self.cells[i-1][j]
            if cell1['zone'] == cell2['zone']:
                return False
            cell1['N'] = True
            cell2['S'] = True
        if direction == 'S':
            if i == self.height-1:
                return False
            cell2 = self.cells[i+1][j]
            if cell1['zone'] == cell2['zone']:
                return False
            cell1['S'] = True
            cell2['N'] = True
        if direction == 'E':
            if j == self.width-1:
                return False
            cell2 = self.cells[i][j+1]
            if cell1['zone'] == cell2['zone']:
                return False
            cell1['E'] = True
            cell2['W'] = True
        if direction == 'W':
            if j == 0:
                return False
            cell2 = self.cells[i][j-1]
            if cell1['zone'] == cell2['zone']:
                return False
            cell1['W'] = True
            cell2['E'] = True
        new_zone = cell1['zone']
        old_zone = cell2['zone']
        for i1 in range(self.height):
            for j1 in range(self.width):
                if self.cells[i1][j1]['zone'] == old_zone:
                    self.cells[i1][j1]['zone'] = new_zone
        return True

    def is_ready(self):
        one_zone = self.cells[0][0]["zone"]
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j]["zone"] != one_zone:
                    return False
        return True

    def generate(self):
        walls = []
        for i in range(self.height):
            for j in range(self.width):
                for d in ['N', 'S', 'E', 'W']:
                    walls.append((i, j, d))
        random.shuffle(walls)
        while not(self.is_ready()):
            curr_wall = walls.pop(0)
            self.merge(curr_wall[0], curr_wall[1], curr_wall[2])

    def plot(self, path_list):
        n = len(path_list)
        c = math.ceil(math.sqrt(n))
        for k in range(n):
            ax = plt.subplot(c, c, k+1)
            ax.fill([0,1,1,0,0], [0,0,1,1,0], 'lightcoral')
            ax.fill([self.width-1,self.width,self.width,self.width-1,self.width-1], [self.height-1,self.height-1,self.height,self.height,self.height-1], 'greenyellow')
            ax.invert_yaxis()
            ax.axis("off")
            ax.plot([0, self.width, self.width, 0, 0], [0, 0, self.height,self.height, 0], 'purple')
            for i in range(self.height):
                for j in range(self.width):
                    if self.cells[i][j]['N'] == False:
                        ax.plot([j, j+1], [i ,i], 'blueviolet')
                    if self.cells[i][j]['E'] == False:
                        ax.plot([j+1, j+1], [i ,i+1], 'blueviolet')
            curr_path = path_list[k]
            i = 0.5
            j = 0.5
            i_list = [0.5]
            j_list = [0.5]
            for dir in curr_path:
                if dir == 'N':
                    j-=1
                if dir == 'S':
                    j+=1
                if dir == 'E':
                    i+=1
                if dir == 'W':
                    i-=1
                i_list.append(i)
                j_list.append(j)
            ax.plot(i_list, j_list, 'darkorange')
        plt.show()

if __name__ == '__main__':
    a = Labyrinthe(20,15)
    a.generate()
    a.plot([['S', 'E', 'E', 'N', 'E'], ['S', 'E', 'S', 'W', 'S'], ['E', 'E', 'E', 'S', 'E'], ['S', 'E', 'S', 'W', 'S'], ['E', 'E', 'E', 'S', 'E'], ['S', 'E', 'S', 'W', 'S'], ['E', 'E', 'E', 'S', 'E'], ['S', 'E', 'S', 'W', 'S'], ['E', 'E', 'E', 'S', 'E']])