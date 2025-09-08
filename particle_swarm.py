import numpy as np

# Objective function
def f(x):
    return -x**2 + 20*x + 5

# Initial particle positions
positions = np.array([0.6, 2.3, 2.8, 8.3, 10, 9.6, 6, 2.6, 1.1])
velocities = np.zeros_like(positions)
pbest_positions = positions.copy()
pbest_scores = f(positions)
gbest_position = pbest_positions[np.argmax(pbest_scores)]
c1 = c2 = 1
w = 1

# Random values from the example for each iteration
r_values = [
    (0.213, 0.876),
    (0.113, 0.706),
    (0.178, 0.507)
]

print("Initial positions:\n", positions)
print("Initial function values:\n", f(positions))
print("Initial global best position:", gbest_position, "with value:", f(gbest_position))
print("-" * 50)

# Run 3 iterations as in the example
for t in range(3):
    r1, r2 = r_values[t]
   
    for i in range(len(positions)):
        velocities[i] = (
            w * velocities[i] +
            c1 * r1 * (pbest_positions[i] - positions[i]) +
            c2 * r2 * (gbest_position - positions[i])
        )

    positions += velocities
    scores = f(positions)

    # Update personal bests
    for i in range(len(positions)):
        if scores[i] > pbest_scores[i]:
            pbest_positions[i] = positions[i]
            pbest_scores[i] = scores[i]
   
    # Update global best
    gbest_position = pbest_positions[np.argmax(pbest_scores)]

    # Display results
    print(f"Iteration {t+1}")
    print("Positions:", positions.round(4))
    print("Velocities:", velocities.round(4))
    print("Function values:", scores.round(4))
    print("Global best position:", gbest_position, "with value:", f(gbest_position))
    print("-" * 50)
