import random
import numpy as np

# Step 1: Define the Knapsack Problem
# Sample data: values and weights of items
values = [60, 100, 120, 80, 30]
weights = [10, 20, 30, 15, 5]
max_weight = 50
num_items = len(values)

# Fitness function: maximize value while staying under weight limit
def fitness(nest):
    total_value = 0
    total_weight = 0
    for i in range(num_items):
        if nest[i] == 1:
            total_value += values[i]
            total_weight += weights[i]
    if total_weight > max_weight:
        return 0  # Penalty for exceeding capacity
    return total_value

# Step 2: Initialize Parameters
num_nests = 25
max_iterations = 100
discovery_rate = 0.25  # Probability of discovering a nest
alpha = 1.0  # Step size for Lévy flights

# Step 3: Initialize Population
def initialize_population():
    return [[random.randint(0, 1) for _ in range(num_items)] for _ in range(num_nests)]

population = initialize_population()

# Step 4: Evaluate Fitness
fitness_values = [fitness(nest) for nest in population]

# Step 5: Generate New Solutions using Lévy flights (simple binary flipping)
def levy_flight(nest):
    new_nest = nest.copy()
    for i in range(num_items):
        if random.random() < 0.3:  # 30% chance to flip each bit
            new_nest[i] = 1 - new_nest[i]
    return new_nest

# Step 6: Replace worst nests
def abandon_worst_nests(population, fitness_values):
    num_abandon = int(discovery_rate * num_nests)
    worst_indices = np.argsort(fitness_values)[:num_abandon]

    for idx in worst_indices:
        population[idx] = [random.randint(0, 1) for _ in range(num_items)]
    return population

# Step 7: Main Loop
best_nest = None
best_fitness = -1

for iteration in range(max_iterations):
    for i in range(num_nests):
        # Generate a new solution by Lévy flight
        new_nest = levy_flight(population[i])
        new_fitness = fitness(new_nest)

        # Greedy selection
        if new_fitness > fitness_values[i]:
            population[i] = new_nest
            fitness_values[i] = new_fitness

        # Track the global best
        if new_fitness > best_fitness:
            best_fitness = new_fitness
            best_nest = new_nest.copy()

    # Abandon a fraction of the worst nests
    population = abandon_worst_nests(population, fitness_values)
    fitness_values = [fitness(nest) for nest in population]

# Step 8: Output the Best Solution
print("Best Solution (Item Inclusion):", best_nest)
print("Best Total Value:", best_fitness)
print("Total Weight:",
      sum(weights[i] for i in range(num_items) if best_nest[i] == 1))
