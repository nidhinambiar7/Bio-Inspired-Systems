import numpy as np
import random
import math

# Step 1: Define the problem (set of cities with coordinates)
cities = [
    (0, 0),
    (1, 5),
    (5, 2),
    (6, 6),
    (8, 3),
    (7, 9),
    (2, 7),
    (3, 3)
]
N = len(cities)

# Calculate Euclidean distance matrix
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

distance_matrix = [[euclidean_distance(cities[i], cities[j]) for j in range(N)] for i in range(N)]

# Step 2: Initialize Parameters
num_ants = N
max_iterations = 100
alpha = 1.0
beta = 5.0
rho = 0.5
Q = 100.0
tau_0 = 1.0

pheromone = [[tau_0 for _ in range(N)] for _ in range(N)]
heuristic = [[1 / distance_matrix[i][j] if i != j else 0 for j in range(N)] for i in range(N)]

best_tour = None
best_length = float('inf')

# Step 3, 4, 5: Iterate
for iteration in range(max_iterations):
    all_tours = []
    all_lengths = []

    for ant in range(num_ants):
        unvisited = list(range(N))
        current_city = random.choice(unvisited)
        tour = [current_city]
        unvisited.remove(current_city)

        while unvisited:
            probabilities = []
            for j in unvisited:
                tau = pheromone[current_city][j] ** alpha
                eta = heuristic[current_city][j] ** beta
                probabilities.append(tau * eta)
            total = sum(probabilities)
            probabilities = [p / total for p in probabilities]
            next_city = random.choices(unvisited, weights=probabilities, k=1)[0]
            tour.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city

        # Return to starting city
        tour.append(tour[0])
        tour_length = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(N))
        all_tours.append(tour)
        all_lengths.append(tour_length)

        if tour_length < best_length:
            best_length = tour_length
            best_tour = tour

    # Step 4: Update Pheromones
    # Evaporation
    for i in range(N):
        for j in range(N):
            pheromone[i][j] *= (1 - rho)

    # Deposit
    for tour, length in zip(all_tours, all_lengths):
        for i in range(N):
            a = tour[i]
            b = tour[i+1]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length  # because TSP is symmetric

# Step 6: Output the Best Solution
print("Best tour:", best_tour)
print("Best tour length:", round(best_length, 2))
