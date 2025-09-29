import numpy as np

# Example Data:
num_cars = 5
num_slots = 5
slot_distances = np.array([10, 20, 15, 30, 25])  # Distances of parking slots to entrance
num_wolves = 10
max_iter = 50

# Initialize wolves: each wolf is a permutation of slot indices representing car assignments
def initialize_population(num_wolves, num_slots):
    population = []
    for _ in range(num_wolves):
        wolf = np.random.permutation(num_slots)
        population.append(wolf)
    return population

# Fitness function: total walking distance for assigned slots
def fitness(wolf):
    total_distance = 0
    for car_index, slot_index in enumerate(wolf):
        total_distance += slot_distances[slot_index]  # Distance of car's assigned slot
    return total_distance

# Update position of wolf based on alpha, beta, delta (GWO update mechanism)
def update_position(wolf, alpha, beta, delta, a):
    # Generate a new wolf position by exploring around alpha, beta, delta wolves
    new_wolf = wolf.copy()
    
    for i in range(len(wolf)):
        r1 = np.random.rand()
        r2 = np.random.rand()
        
        # Move the wolf toward the alpha, beta, or delta
        if r1 < 0.33:
            new_wolf[i] = alpha[i]  # Move toward alpha wolf
        elif r1 < 0.66:
            new_wolf[i] = beta[i]   # Move toward beta wolf
        else:
            new_wolf[i] = delta[i]  # Move toward delta wolf
            
    # Ensure new_wolf is a valid permutation (no duplicates)
    new_wolf = np.unique(new_wolf)
    if len(new_wolf) < len(wolf):
        # if duplicates occur, randomly swap elements to maintain uniqueness
        missing_values = list(set(range(len(wolf))) - set(new_wolf))
        np.random.shuffle(missing_values)
        new_wolf = np.append(new_wolf, missing_values)

    # Now we randomly swap some elements to increase diversity and exploration
    swap_indices = np.random.choice(len(wolf), 2, replace=False)
    new_wolf[swap_indices[0]], new_wolf[swap_indices[1]] = new_wolf[swap_indices[1]], new_wolf[swap_indices[0]]
    
    return new_wolf

# Main GWO loop for parking slot allocation
def gwo_parking_allocation():
    # Initialize wolves (population)
    population = initialize_population(num_wolves, num_slots)
    
    # Variables to keep track of the best solutions
    alpha = None
    beta = None
    delta = None
    
    alpha_score = float('inf')
    beta_score = float('inf')
    delta_score = float('inf')
    
    # GWO main loop (iterations)
    for iteration in range(max_iter):
        # Evaluate the fitness of each wolf in the population
        fitness_scores = []
        for wolf in population:
            score = fitness(wolf)
            fitness_scores.append(score)
            
            # Update alpha, beta, delta based on fitness
            if score < alpha_score:
                delta_score, delta = beta_score, beta
                beta_score, beta = alpha_score, alpha
                alpha_score, alpha = score, wolf
            elif score < beta_score:
                delta_score, delta = beta_score, beta
                beta_score, beta = score, wolf
            elif score < delta_score:
                delta_score, delta = score, wolf
        
        # Update positions of wolves based on best wolves (alpha, beta, delta)
        new_population = []
        for wolf in population:
            # Adjust the exploration factor "a" to control the step size over iterations
            a = 2 - iteration * (2 / max_iter)
            new_wolf = update_position(wolf, alpha, beta, delta, a)
            new_population.append(new_wolf)
        population = new_population
        
        # Print progress
        print(f"Iteration {iteration+1}: Best total walking distance = {alpha_score}")
    
    # Final best result
    print("\nBest Assignment of Cars to Slots (car i -> slot number):")
    print(alpha)
    print("Slot distances:", slot_distances[alpha])
    print("Total walking distance:", alpha_score)

# Run the optimizer
gwo_parking_allocation()
