import random
import numpy as np

NBR_ARRONDISSEMENTS = 12
COUT_MAGASIN = 6
REVENUS_ARRONDISSEMENTS = np.array([1, 8, 6, 3, 2, 4, 2, 2, 1, 1, 1, 3])
ADJACENCE = np.array([
    [1,1,0,0,1,1,0,0,0,0,0,0],
    [1,1,1,0,0,1,1,0,0,0,0,0],
    [0,1,1,1,0,1,1,0,0,0,0,0],
    [0,0,1,1,0,0,1,0,1,0,0,0],
    [1,0,0,0,1,1,0,1,0,1,1,1],
    [1,1,1,0,1,1,1,1,1,0,0,0],
    [0,1,1,1,0,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,1,1],
    [0,0,0,1,0,1,1,1,1,0,0,1],
    [0,0,0,0,1,0,0,0,0,1,1,0],
    [0,0,0,0,1,0,0,1,1,1,1,1],
    [0,0,0,0,1,0,0,1,1,0,1,1]])


# génération d'un individu aléatoirement
def individu_aleatoire():
    return np.array([random.randint(0,1) for i in range(NBR_ARRONDISSEMENTS)])

# calcul de la fitness de l'individu (correspondant au chiffre d'affaires ici)
def fitness(individu):
    s = 0
    couverture = np.dot(individu,ADJACENCE)
    for i in range(NBR_ARRONDISSEMENTS):
        # si l'arrondissement est couvert par un magasin dans un arrondissement adjacent
        # on ajoute les revenus correspondants
        if couverture[i] != 0:
            s += REVENUS_ARRONDISSEMENTS[i]
        # si l'arrondissement contient un magasin
        # on retire le coût d'un magasin
        if individu[i] != 0:
            s -= COUT_MAGASIN
    return s

# génération de deux nouveaux individus 
# à partir de deux individus séléctionnés dans la génération précédente
# à partir de [A,B] et [C,D] on crée [A,D] et [C,B]
def croisement(i1, i2):
    i3 = [0]*NBR_ARRONDISSEMENTS
    i4 = [0]*NBR_ARRONDISSEMENTS
    for i in range(NBR_ARRONDISSEMENTS//2):
        i3[i] = i1[i]
        i4[i] = i2[i]
        i3[-i-1] = i2[-i-1]
        i4[-i-1] = i1[-i-1]
    if NBR_ARRONDISSEMENTS%2==1:
        i3[NBR_ARRONDISSEMENTS//2+1] = i1[NBR_ARRONDISSEMENTS//2+1]
        i4[NBR_ARRONDISSEMENTS//2+1] = i2[NBR_ARRONDISSEMENTS//2+1]
    return (np.array(i3), np.array(i4))

# séléction de la moitié la plus fit des individus de la génération précédente
def selection(gen):
    gen.sort(key=fitness, reverse=True)
    return gen[:len(gen)//2]

# création aléatoire de la première génération
def first_gen(taille_pop):
    return [individu_aleatoire() for i in range(taille_pop)]

# reproduction deux à deux des individus de la génération précédente
def next_gen(prev_gen):
    next_gen = list.copy(prev_gen)
    for i in range(len(prev_gen)//2):
        new1, new2 = croisement(prev_gen[i], prev_gen [-i-1])
        next_gen.append(new1)
        next_gen.append(new2)
    return next_gen

# modification d'un des caractères de certains individus de la génération
def mutation(proba, gen):
    for e in gen:
        if random.random() <= proba:
            i = random.randint(0, NBR_ARRONDISSEMENTS-1)
            e[i] = 1 - e[i]
    return gen

##################################################################################

TAILLE_POP = 100
PROBA_MUTATION = 0.8
NBR_GEN = 100

# générations successives
gen = first_gen(TAILLE_POP)
for i in range(NBR_GEN):
    gen = selection(gen)
    print(f"Géneration {i} : meilleure fitness {max([fitness(e) for e in gen])}")
    gen = next_gen(gen)
    gen = mutation(PROBA_MUTATION, gen)
final_fit = [fitness(e) for e in gen]
final_fit.sort()
print(final_fit)
