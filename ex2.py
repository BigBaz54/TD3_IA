from labyrinthe import *

def get_pos(individu):
    x, y = 0, 0
    for curr_dir in individu:
        if curr_dir == 'N':
            y -= 1
        if curr_dir == 'S':
            y += 1
        if curr_dir == 'E':
            x += 1
        if curr_dir == 'W':
            x -= 1
    return x,y

def individu_aleatoire(laby):
    return continuer_chemin(laby, [])

def first_gen(laby, taille_pop):
    return [individu_aleatoire(laby) for _ in range(taille_pop)]

def fitness(laby, individu):
    x,y = get_pos(individu)
    cell = laby.cells[y][x]
    x_end = laby.width-1
    y_end = laby.height-1
    dist_end = math.sqrt((x_end-x)**2+(y_end-y)**2)+1
    if dist_end == 0:
        return 1
    if [cell['N'], cell['S'], cell['E'], cell['W']].count(True)<2:
        return 0
    score = 0
    score += 1/dist_end
    return score

def selection(laby, pop):
    return sorted(pop, key=(lambda x: fitness(laby, x)), reverse=True)[:len(pop)//2]

def continuer_chemin(laby, individu):
    chemin = individu
    vivant = True
    (x, y) = get_pos(individu)
    while vivant:
        curr_dir = random.choice(['N', 'S', 'E', 'W'])
        if laby.cells[y][x][curr_dir]:
            if curr_dir == 'N':
                if (chemin == []) or (chemin[-1] != 'S'):
                    chemin.append(curr_dir)
                    y -= 1
            if curr_dir == 'S':
                if (chemin == []) or (chemin[-1] != 'N'):
                    chemin.append(curr_dir)
                    y += 1
            if curr_dir == 'E':
                if (chemin == []) or (chemin[-1] != 'W'):
                    chemin.append(curr_dir)
                    x += 1
            if curr_dir == 'W':
                if (chemin == []) or (chemin[-1] != 'E'):
                    chemin.append(curr_dir)
                    x -= 1
        else:
            vivant = False
    return chemin

def croisement(individu):
    return individu[:len(individu)//2]

def mutation(proba, gen):
    for i in range(len(gen)):
        if random.random() <= proba:
            e = gen[i]
            m = random.randint(0, len(e))
            gen[i] = e[:m]
    return gen

def next_gen(laby, prev_gen):
    next_gen = []
    for e in prev_gen:
        next_gen.append(continuer_chemin(laby, e))
        next_gen.append(continuer_chemin(laby, croisement(e)))
    return next_gen


##################################################################################

TAILLE_POP = 1000
PROBA_MUTATION = 0.1
NBR_GEN = 1000

# générations successives
labyrinthe = Labyrinthe(10,10)
labyrinthe.generate()
gen = first_gen(labyrinthe, TAILLE_POP)
for i in range(NBR_GEN):
    print(f"Géneration {i} : meilleure fitness {round(max([fitness(labyrinthe, e) for e in gen]), 2)}")
    if fitness(labyrinthe, gen[-1]) == 1:
        break
    gen = selection(labyrinthe, gen)
    gen = next_gen(labyrinthe, gen)
    gen = mutation(PROBA_MUTATION, gen)
    gen.sort(key=(lambda x: fitness(labyrinthe, x)))
labyrinthe.plot(gen[-9:])