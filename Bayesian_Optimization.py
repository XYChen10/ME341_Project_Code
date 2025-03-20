import math
import csv
import subprocess
import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args

# Fixed parameters / constants 
p = 10.0  # MPa
sigma_allow = 260.0  # MPa
V_req = 2.271e8  # mm^3
rho = 7.75e-9  # tonne/mm^3
R_n = 150.0   # nozzle outer radius (mm)
H_n = 150.0   # nozzle height (mm)

# Design variable bounds
R_min, R_max = 300.0, 1000.0
L_min, L_max = 1200.0, 4000.0
t_s_min, t_s_max = 40.0, 300.0
t_h_min, t_h_max = 40.0, 300.0
t_n_min, t_n_max = 30.0, 100.0

# Define search space for (R, L, t_s, t_h, t_n)
space = [
    Real(R_min, R_max, name='R'),
    Real(L_min, L_max, name='L'),
    Real(t_s_min, t_s_max, name='t_s'),
    Real(t_h_min, t_h_max, name='t_h'),
    Real(t_n_min, t_n_max, name='t_n')
]

# A global list to store stress & constraint violations for penalty tuning
stress_history = []  
constraint_data = []
mass_history = []  # Stores mass without penalty
abaqus_mass_history = []  # Stores mass from Abaqus

# Penalty multipliers (updated after running penalty optimization script)
penalty_multipliers = {
    "volume_deficit": 5.0,
    "t_s_deficit": 0.1,
    "t_h_deficit": 0.1,
    "t_n_deficit": 0.1, 
    "stress_excess": 10.0}

# Continuous penalty function
def constraint_penalty(violations, multipliers):
    return sum(m * v**2 for m, v in zip(multipliers.values(), violations))

# Objective with volume & thickness constraints + stress check from Abaqus
@use_named_args(space)
def objective(R, L, t_s, t_h, t_n):
    global stress_history, constraint_data, mass_history, abaqus_mass_history
    max_stress_val = None
    epsilon = 1e-3  # Small value to prevent numerical issues

    # Compute estimated mass before applying penalties
    shell_area = 2.0 * math.pi * R * L
    head_area = 4.0 * math.pi * R**2
    nozzle_area = 2.0 * math.pi * R_n * H_n
    hole_area = math.pi * (R_n**2)

    volume_shell = shell_area * t_s
    volume_heads = head_area * t_h
    volume_nozzle = nozzle_area * t_n
    volume_hole = hole_area * t_s

    total_volume = volume_shell + volume_heads + volume_nozzle - volume_hole
    mass_without_penalty = rho * total_volume

    # Check geometric constraints
    volume = math.pi * (R - (t_s / 2.0))**2 * L + ((4.0/3.0) * math.pi * (R - (t_h / 2.0))**3)
    volume_deficit = max(0, V_req - volume)

    min_t_s = (p * R) / (2.0 * sigma_allow)
    t_s_deficit = max(0, min_t_s - t_s)

    min_t_h = (p * R) / (2.0 * sigma_allow)
    t_h_deficit = max(0, min_t_h - t_h)

    min_t_n = (p * R_n) / (2.0 * sigma_allow)
    t_n_deficit = max(0, min_t_n - t_n)

    # Compute penalty
    violations = [volume_deficit, t_s_deficit, t_h_deficit, t_n_deficit]
    penalty = constraint_penalty(violations, penalty_multipliers)

    # Run Abaqus
    if os.path.exists("results.txt"):
        os.remove("results.txt")

    cmd = [r"C:\SIMULIA\Commands\abaqus.bat",
        "cae", "noGUI=Run_Abaqus.py", "--",
        str(R), str(L), str(t_s), str(t_h), str(t_n)]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return 1e5 + penalty

    if not os.path.exists("results.txt"):
        return 1e5 + penalty

    # Parse results.txt
    with open("results.txt", "r") as f:
        content = f.read()

    match_mass = re.search(r"MASS=([0-9.+-eE]+)", content)
    match_stress = re.search(r"MAX_STRESS=([0-9.+-eE]+)", content)
    abaqus_mass = float(match_mass.group(1)) if match_mass else None
    max_stress_val = float(match_stress.group(1)) if match_stress else None
    stress_excess = max(0, max_stress_val - (sigma_allow / 3.0))
    penalty += penalty_multipliers["stress_excess"] * stress_excess**2
    stress_history.append(max_stress_val)
    mass_history.append(mass_without_penalty)
    abaqus_mass_history.append(abaqus_mass)  
    constraint_data.append([volume_deficit, t_s_deficit, t_h_deficit, t_n_deficit, stress_excess])

    return mass_without_penalty + penalty

# Run Bayesian optimization 
def main():
    print("Starting optimization with Abaqus stress check...")
    n_calls = 100  # Number of iterations
    # Note Try different starting points and numeber of calls, show plots

    # Define an initial design point
    initial_x = [500, 1500.0, 60.0, 60.0, 65.0] 
    # initial_x = [300, 1300.0, 100.0, 100.0, 60.0]  # Example: [R, L, t_s, t_h, t_n]
    # initial_x = [350, 1300.0, 70.0, 70.0, 75.0]  # Example: [R, L, t_s, t_h, t_n]

    # Evaluate the objective function at this initial point
    initial_y = [objective(initial_x)] # Must be a list
    
    # Run Bayesian Optimization
    result = gp_minimize(
        func=objective,  # Defines objective function to be minimized
        dimensions=space,  # Defines the search space of the optimization (bounds on inputs)
        n_calls=n_calls,  # Number of times to call this function (iterations)
        n_initial_points=50,  # Defines the number of starting points (initial sample, 5 variables)
        random_state=0,  # Ensures reproducibility of optimization (consistent results across runs)
        acq_func='EI',  # "Expected Improvement"(EI) method for acquisition
        x0=[initial_x],  # Provide initial design variable values
        y0=initial_y  # Provide the corresponding objective function value
    ) # Gaussian Process (gp) searches for where the acq_func can be improved with each step

    # Print best solution
    print("\nOptimization done.")
    print("Best parameters:")
    print(f"  R   = {result.x[0]:.4f} mm")
    print(f"  L   = {result.x[1]:.4f} mm")
    print(f"  t_s = {result.x[2]:.4f} mm")
    print(f"  t_h = {result.x[3]:.4f} mm")
    print(f"  t_n = {result.x[4]:.4f} mm")
    print(f"Minimum mass = {result.fun:.6f} tonne")

    with open("optimization_data.csv", "w", newline="") as fout:
        writer = csv.writer(fout)
        writer.writerow(["R", "L", "t_s", "t_h", "t_n", "MaxStress", "MassWithoutPenalty", "MassFromAbaqus", "Objective",
                         "VolumeDeficit", "t_s_Deficit", "t_h_Deficit", "t_n_Deficit","StressExcess"])
        for x, obj_val, mass_val, abaqus_mass, st_val, constraints in zip(result.x_iters, result.func_vals, mass_history, abaqus_mass_history, stress_history, constraint_data):
            writer.writerow(list(x) + [st_val if st_val is not None else "N/A", mass_val, abaqus_mass, obj_val] + constraints)

if __name__ == "__main__":
    main()
