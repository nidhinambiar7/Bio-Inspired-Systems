import random
import string

TARGET = "HELLO WORLD"
POP_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 1000
CHARS = string.ascii_uppercase + " "

def fitness(ind):
    return sum(c1 == c2 for c1, c2 in zip(ind, TARGET))

def generate_individual():
    return ''.join(random.choice(CHARS) for _ in TARGET)

def mutate(ind):
    return ''.join(
        c if random.random() > MUTATION_RATE else random.choice(CHARS)
        for c in ind
    )

def crossover(p1, p2):
    point = random.randint(0, len(TARGET) - 1)
    return p1[:point] + p2[point:]

def selection(pop):
    return max(random.sample(pop, 5), key=fitness)

def genetic_algorithm():
    population = [generate_individual() for _ in range(POP_SIZE)]

    for gen in range(GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        best = population[0]
        print(f"Gen {gen}: {best} (Fitness = {fitness(best)})")
        if best == TARGET:
            break

        next_gen = population[:2]
        while len(next_gen) < POP_SIZE:
            p1 = selection(population)
            p2 = selection(population)
            child = crossover(p1, p2)
            child = mutate(child)
            next_gen.append(child)
        population = next_gen

    print("\nBest Match:", best)

if __name__ == "__main__":
    genetic_algorithm()
