import random

# Calculate average waiting time for a given schedule
def avg_waiting_time(schedule, burst_times):
    waiting_time = 0
    total_waiting = 0
    for p in schedule[:-1]:
        total_waiting += waiting_time
        waiting_time += burst_times[p]
    return total_waiting / len(schedule)

# Fitness function (we want to minimize avg waiting time)
def fitness(schedule, burst_times):
    return 1 / (1 + avg_waiting_time(schedule, burst_times))

# Generate random schedule
def random_schedule(n):
    schedule = list(range(n))
    random.shuffle(schedule)
    return schedule

# Tournament selection
def selection(population, burst_times):
    contenders = random.sample(population, 3)
    return max(contenders, key=lambda s: fitness(s, burst_times))

# Crossover (ordered crossover for schedules)
def crossover(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    child = [None] * len(p1)
    child[a:b] = p1[a:b]
    fill = [p for p in p2 if p not in child]
    idx = 0
    for i in range(len(p1)):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child

# Mutation: swap two processes
def mutate(schedule, rate=0.2):
    for _ in range(len(schedule)):
        if random.random() < rate:
            i, j = random.sample(range(len(schedule)), 2)
            schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule

# Main GEA for CPU Scheduling
def gene_expression_scheduler(burst_times, pop_size=30, generations=200):
    n = len(burst_times)
    population = [random_schedule(n) for _ in range(pop_size)]
    best = None

    for g in range(generations + 1):  # include final generation
        population.sort(key=lambda s: fitness(s, burst_times), reverse=True)
        if best is None or fitness(population[0], burst_times) > fitness(best, burst_times):
            best = population[0]

        new_pop = []
        while len(new_pop) < pop_size:
            p1 = selection(population, burst_times)
            p2 = selection(population, burst_times)
            child = crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)

        population = new_pop

        # Print only selected generations
        if g == 0 or g == 10 or g % 50 == 0:
            print(f"Gen {g}: Best Avg Waiting Time = {avg_waiting_time(best, burst_times):.2f}")

    return best

# Example with 5 processes
burst_times = [5, 2, 8, 3, 6]   # CPU burst times for processes P1...P5
best_schedule = gene_expression_scheduler(burst_times)

print("\n✅ Best Schedule Found:", best_schedule)
print("✅ Avg Waiting Time:", avg_waiting_time(best_schedule, burst_times))
