# This is the Random Sample algorithm used to compare to Bayesian Optimization
import random
import math
import csv
import subprocess
import os
import re

# Objective function: mass of the pressure vessel (M = ρ * V)
def objective_function(L, R, t_s, t_h, t_n):
    # Material density (rho)
    rho = 7.75e-9 # tonne/mm^3
    
    # Nozzle is a cylindrical shape with thickness t_nozzle
    R_n = 150.0 # Fixed radius of the nozzle (mm)
    H_n = 150.0 # Fixed length of the nozzle (mm)

    max_stress_val = None # Calling Abaqus to calculate
    epsilon = 1e-3 # Small value to prevent equality issues
    p = 10.0 # MPa
    sigma_allow = 260.0 # MPa

    min_t_s = (p * R) / (2.0 * sigma_allow)

    min_t_h = (p * R) / (2.0 * sigma_allow)

    min_t_n = (p * R_n) / (2.0 * sigma_allow)

    # Ensure thickness is less than radius
    t_s_violation = max(0, t_s - (R - epsilon))  # If t_s >= R, penalize
    t_h_violation = max(0, t_h - (R - epsilon))  # If t_h >= R, penalize

    # Setup volumetric constraint
    volume = math.pi * (R - (t_s / 2.0))**2 * L + (4.0/3.0)*math.pi * (R - (t_h / 2.0))**3
    
    # Compute vessel mass
    shell_area   = 2.0 * math.pi * R * L # A = 2*pi*R*L for cylindrical part (two halves of full vessel)
    head_area    = 4.0 * math.pi * R**2 # A = 4*pi*R^2 for endcap (sphere)
    nozzle_area  = 2.0 * math.pi * R_n * H_n # A = 2*pi*R*H for cylindrical nozzle (two nozzles)
    hole_area    = math.pi * (R_n**2)

    volume_shell  = shell_area * t_s # V = A*t for shell thickness
    volume_heads  = head_area * t_h # V = A*t for head thickness
    volume_nozzle = nozzle_area * t_n # V = A*t for nozzle thickness
    volume_hole   = hole_area * t_s # V = A*t for hole thickness

    total_volume = volume_shell + volume_heads + volume_nozzle - volume_hole # combine all volumes
    mass = rho * total_volume # mass = density * volume, rho = density = 7.75e-9 
    
    # Clean up old results file if it exists
    if os.path.exists("results.txt"):
        os.remove("results.txt")

    # Call Abaqus to compute
    cmd = [r"C:\SIMULIA\Commands\abaqus.bat", # full path to abaqus.bat
    "cae","noGUI=runAbaqus.py","--",
    str(R),
    str(L),
    str(t_s),
    str(t_h),
    str(t_n)]   

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        stress_history = max_stress_val
        return 0

    return mass # Mass in tonnes, 1 tonne = 1000 kg

# Random sample optimization algorithm
def random_sample_optimization(num_samples, lower_bound_L, upper_bound_L, lower_bound_R, upper_bound_R,
    lower_bound_t_shell, upper_bound_t_shell, lower_bound_t_endcap, upper_bound_t_endcap,
    lower_bound_t_nozzle, upper_bound_t_nozzle, v_req, output_file="random_results.csv"):
    best_solution = None
    Optimal_Mass = float('inf') # Start with a very high value (worst fitness)
    global stress_history 

    # If initial values are provided, use them as the first solution
    if initial_values is not None:
        L, R, t_s, t_h, t_n = initial_values
        fitness = objective_function(L, R, t_s, t_h, t_n)
        best_solution = (L, R, t_s, t_h, t_n)
        Optimal_Mass = fitness
        print(f"Starting Solution: {best_solution} with Fitness: {Optimal_Mass} tonnes")

        # Read MAX_STRESS from results.txt
        with open("results.txt", "r") as fout:
            for line in fout:
                if line.startswith("MAX_STRESS="):
                    max_stress = float(line.split('=')[1].strip()) # Strip any surrounding spaces or newlines
                if line.startswith("MASS="):
                    Mass = float(line.split('=')[1].strip()) # Strip any surrounding spaces or newlines

        # Write the initial result to the CSV
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['L', 'R', 't_s', 't_h', 't_n', 'MaxStress', 'Mass', 'Aba_Mass'])
            writer.writerow([round(L, 5), round(R, 5), round(t_s, 5), round(t_h, 5), round(t_n, 5), round(max_stress, 5), round(fitness, 5), round(Mass, 5)])

    for _ in range(num_samples):
        # Randomly generate values for L, r, t_shell, t_endcap, and t_nozzle within specified bounds
        L = random.uniform(lower_bound_L, upper_bound_L)
        R = random.uniform(lower_bound_R, upper_bound_R)
        t_s = random.uniform(lower_bound_t_shell, upper_bound_t_shell)
        t_h = random.uniform(lower_bound_t_endcap, upper_bound_t_endcap)
        t_n = random.uniform(lower_bound_t_nozzle, upper_bound_t_nozzle)

        R_n = 150.0 # Fixed radius of the nozzle (mm)
        H_n = 150.0 # Fixed length of the nozzle (mm)

        max_stress_val = None  
        epsilon = 1e-3 # Small value to prevent equality issues
        p = 10.0 # MPa
        sigma_allow = 260.0 # MPa

        min_t_s = (p * R) / (2.0 * sigma_allow)
        min_t_h = (p * R) / (2.0 * sigma_allow)
        min_t_n = (p * R_n) / (2.0 * sigma_allow)

        # Ensure thickness is less than radius
        t_s_violation = max(0, t_s - (R - epsilon)) # If t_s >= R, penalize
        t_h_violation = max(0, t_h - (R - epsilon)) # If t_h >= R, penalize

        # Setup volumetric constraint
        volume = math.pi * (R - (t_s / 2.0))**2 * L + (4.0/3.0)*math.pi * (R - (t_h / 2.0))**3
        
        # Check if the generated values meet the constraints (e.g., thickness must be positive)
        if volume > v_req and stress_history < 260 and t_s_violation >= 0 and t_h_violation >= 0 and t_s >= min_t_s and t_h >= min_t_h and t_n >= min_t_n:
            # Evaluate the objective function (mass of the pressure vessel)
            fitness = objective_function(L, R, t_s, t_h, t_n)
            
            # Update the best solution if the current fitness is better (lower mass)
            if fitness < Optimal_Mass:
                best_solution = (L, R, t_s, t_h, t_n)
                Optimal_Mass = fitness
            
            # Read MAX_STRESS from results.txt
            with open("results.txt", "r") as fout:
                for line in fout:
                    if line.startswith("MAX_STRESS="):
                        max_stress = float(line.split('=')[1].strip()) # Strip any surrounding spaces or newlines
                    if line.startswith("MASS="):
                        Mass = float(line.split('=')[1].strip()) # Strip any surrounding spaces or newlines
                        

            # Write the current iteration's result to the CSV
            with open(output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([round(L, 5), round(R, 5), round(t_s, 5), round(t_h, 5), round(t_n, 5), round(max_stress, 5), round(fitness, 5), round(Mass, 5)])

    # Ensure this return always returns a tuple (best_solution, Optimal_Mass)
    return best_solution, Optimal_Mass

# Parameters for the optimization
num_samples = 49 # Number of random samples
lower_bound_L = 1200.0  # Minimum shell length (mm)
upper_bound_L = 4000.0  # Maximum shell length (mm)
lower_bound_R = 300.0  # Minimum endcap radius (mm)
upper_bound_R = 1000.0  # Maximum endcap radius (mm)
lower_bound_t_shell = 40.0  # Minimum shell thickness (mm)
upper_bound_t_shell = 300.0  # Maximum shell thickness (mm)
lower_bound_t_endcap = 40.0  # Minimum endcap thickness (mm)
upper_bound_t_endcap = 300.0  # Maximum endcap thickness (mm)
lower_bound_t_nozzle = 30.0  # Minimum nozzle thickness (mm)
upper_bound_t_nozzle = 100.0  # Maximum nozzle thickness (mm)

v_req = 2.271e8 # Required minimum volume of vessel mm^3
stress_history = 0.0

# Starting values for L, R, t_shell, t_endcap, t_nozzle
initial_values = (1500.0, 500.0, 60.0, 60.0, 65.0)

# Run the random sample optimization
best_solution, Optimal_Mass = random_sample_optimization(num_samples, lower_bound_L, upper_bound_L, lower_bound_R, upper_bound_R,
    lower_bound_t_shell, upper_bound_t_shell, lower_bound_t_endcap, upper_bound_t_endcap,
    lower_bound_t_nozzle, upper_bound_t_nozzle, v_req, output_file="random_results.csv")

# Display the results
print(f"Best Solution (L, r, t_shell, t_endcap, t_nozzle): {best_solution}")
print(f"Optimal Mass: {Optimal_Mass} tonnes")
