from labyrinthe import *


def individu_aleatoire(laby):
    chemin = []
    vivant = True
    (x, y) = (0, 0)
    while vivant:
        dir = random.choice(['N', 'S', 'E', 'W'])
        if laby.cells[y][x][dir]:
            if dir == 'N':
                if (chemin == []) or (chemin[-1] != 'S'):
                    chemin.append(dir)
                    y -= 1
            if dir == 'S':
                if (chemin == []) or (chemin[-1] != 'N'):
                    chemin.append(dir)
                    y += 1
            if dir == 'E':
                if (chemin == []) or (chemin[-1] != 'W'):
                    chemin.append(dir)
                    x += 1
            if dir == 'W':
                if (chemin == []) or (chemin[-1] != 'E'):
                    chemin.append(dir)
                    x -= 1
        else:
            vivant = False
    return chemin

def first_gen(laby, taille_pop):
    return [individu_aleatoire(laby) for _ in range(taille_pop)]

def fitness(laby, individu):
    score = 0
    x_end = laby.width-1
    y_end = laby.height-1
    x, y = 0, 0
    for dir in individu:
        if dir == 'N':
            y -= 1
        if dir == 'S':
            y += 1
        if dir == 'E':
            x += 1
        if dir == 'W':
            x -= 1
    dist_to_end = math.sqrt((x_end-x)**2+(y_end-y)**2)
    dist_max = math.sqrt((x_end)**2+(y_end)**2)
    dist_done = dist_max - dist_to_end
    score += dist_done
    return score

def selection(laby, pop):
    return sorted(pop, key=(lambda x: fitness(laby, x)), reverse=True)[:len(pop)//2]



labyrinthe = Labyrinthe(5,6)
labyrinthe.generate()
pop = first_gen(labyrinthe, 16)
[fitness(labyrinthe, e) for e in pop]
labyrinthe.plot(pop)
