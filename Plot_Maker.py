# Set up Python 
import math
import csv
import subprocess
import re
import os
from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args
import matplotlib.pyplot as plt
import pandas as pd

# Load data from three CSV files
data1 = pd.read_csv("optimization_data_60_x1.csv")  # First dataset
data2 = pd.read_csv("optimization_data_60_x2.csv")  # Second dataset
data3 = pd.read_csv("optimization_data_60_x3.csv")  # Third dataset

# Extract iteration number (row index) and objective values
iterations1 = range(0, len(data1))  # Start from 0
iterations2 = range(0, len(data2))  # Start from 0
iterations3 = range(0, len(data3))  # Start from 0

objective_values1 = data1["Objective"].astype(float)
objective_values2 = data2["Objective"].astype(float)
objective_values3 = data3["Objective"].astype(float)

max_stress1 = data1["MaxStress"].astype(float)
max_stress2 = data2["MaxStress"].astype(float)
max_stress3 = data3["MaxStress"].astype(float)

mass_without_penalty1 = data1["MassWithoutPenalty"].astype(float)
mass_without_penalty2 = data2["MassWithoutPenalty"].astype(float)
mass_without_penalty3 = data3["MassWithoutPenalty"].astype(float)

# Identify the starting and optimal design for all datasets
initial_index1 = 0  # First iteration
optimal_index1 = objective_values1.idxmin()  # Index of minimum objective value

initial_index2 = 0  # First iteration
optimal_index2 = objective_values2.idxmin()  # Index of minimum objective value

initial_index3 = 0  # First iteration
optimal_index3 = objective_values3.idxmin()  # Index of minimum objective value

# Plot 1: Optimization Progression
plt.figure(figsize=(8, 5))
plt.plot(iterations1, objective_values1, marker='o', linestyle='-', markersize=5, label="Number of Calls 60")
plt.plot(iterations2, objective_values2, marker='s', linestyle='--', markersize=5, label="Number of Calls 60")
plt.plot(iterations3, objective_values3, marker='^', linestyle='-.', markersize=5, label="Number of Calls 50")

plt.scatter(iterations1[initial_index1], objective_values1[initial_index1], color='red', s=100, label="Initial Design 1", zorder=3)
plt.scatter(iterations2[initial_index2], objective_values2[initial_index2], color='purple', s=100, label="Initial Design 2", zorder=3)
plt.scatter(iterations3[initial_index3], objective_values3[initial_index3], color='orange', s=100, label="Initial Design 3", zorder=3)

plt.scatter(iterations1[optimal_index1], objective_values1[optimal_index1], color='green', s=100, label="Optimal Design 1", zorder=3)
plt.scatter(iterations2[optimal_index2], objective_values2[optimal_index2], color='blue', s=100, label="Optimal Design 2", zorder=3)
plt.scatter(iterations3[optimal_index3], objective_values3[optimal_index3], color='brown', s=100, label="Optimal Design 3", zorder=3)

plt.xlabel("Iteration")
plt.ylabel("Objective (Mass + Penalty)")
plt.title("Optimization Progress: Objective vs. Iteration")
plt.legend()
plt.grid(True)
plt.show()

# Plot 2: Max Stress vs Iteration
plt.figure(figsize=(8, 5))
plt.plot(iterations1, max_stress1, marker='o', linestyle='-', markersize=5, label="Number of Calls 60")
plt.plot(iterations2, max_stress2, marker='s', linestyle='--', markersize=5, label="Number of Calls 60")
plt.plot(iterations3, max_stress3, marker='^', linestyle='-.', markersize=5, label="Number of Calls 50")

plt.scatter(iterations1[initial_index1], max_stress1[initial_index1], color='red', s=100, label="Initial Design 1", zorder=3)
plt.scatter(iterations2[initial_index2], max_stress2[initial_index2], color='purple', s=100, label="Initial Design 2", zorder=3)
plt.scatter(iterations3[initial_index3], max_stress3[initial_index3], color='orange', s=100, label="Initial Design 3", zorder=3)

plt.scatter(iterations1[optimal_index1], max_stress1[optimal_index1], color='green', s=100, label="Optimal Design 1", zorder=3)
plt.scatter(iterations2[optimal_index2], max_stress2[optimal_index2], color='blue', s=100, label="Optimal Design 2", zorder=3)
plt.scatter(iterations3[optimal_index3], max_stress3[optimal_index3], color='brown', s=100, label="Optimal Design 3", zorder=3)

plt.xlabel("Iteration")
plt.ylabel("Max Abaqus Stress (MPa)")
plt.title("Max Stress vs. Iteration")
plt.legend()
plt.grid(True)
plt.show()

# Plot 3: Mass Without Penalty vs Iteration
plt.figure(figsize=(8, 5))
plt.plot(iterations1, mass_without_penalty1, marker='o', linestyle='-', markersize=5, label="Number of Calls 60")
plt.plot(iterations2, mass_without_penalty2, marker='s', linestyle='--', markersize=5, label="Number of Calls 60")
plt.plot(iterations3, mass_without_penalty3, marker='^', linestyle='-.', markersize=5, label="Number of Calls 50")

plt.scatter(iterations1[initial_index1], mass_without_penalty1[initial_index1], color='red', s=100, label="Initial Design 1", zorder=3)
plt.scatter(iterations2[initial_index2], mass_without_penalty2[initial_index2], color='purple', s=100, label="Initial Design 2", zorder=3)
plt.scatter(iterations3[initial_index3], mass_without_penalty3[initial_index3], color='orange', s=100, label="Initial Design 3", zorder=3)

plt.scatter(iterations1[optimal_index1], mass_without_penalty1[optimal_index1], color='green', s=100, label="Optimal Design 1", zorder=3)
plt.scatter(iterations2[optimal_index2], mass_without_penalty2[optimal_index2], color='blue', s=100, label="Optimal Design 2", zorder=3)
plt.scatter(iterations3[optimal_index3], mass_without_penalty3[optimal_index3], color='brown', s=100, label="Optimal Design 3", zorder=3)

plt.xlabel("Iteration")
plt.ylabel("Mass Without Penalty (tonnes)")
plt.title("Mass Without Penalty vs. Iteration")
plt.legend()
plt.grid(True)
plt.show()
