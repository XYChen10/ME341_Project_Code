clear
clc

% Read the CSV file into a table
data = readtable('optimization_data_x1n30.csv');

Stress_vector = data.MaxStress;
Mass_W_P_vector = data.MassWithoutPenalty;
Mass_F_A_vector = data.MassFromAbaqus;
Objective_vector = data.Objective;

x = (1:31);

% Ploting Max Stress vs. Iteration
figure(1)
plot(x, Stress_vector)
xlim([1 31])
title('Max Stress vs. Iteration')
xlabel('Iterations')
ylabel('Max Stress (MPa)')
 
% Ploting Mass Without Penalty vs. Iteration
figure(2)
plot(x, Mass_W_P_vector)
xlim([1 31])
title('Mass Without Penalty vs. Iteration')
xlabel('Iterations')
ylabel('Mass Without Penalty (tonnes)')
 
% Ploting Mass (Abaqus) vs. Iteration
figure(3)
plot(x, Mass_F_A_vector)
xlim([1 31])
title('Mass (Abaqus) vs. Iteration')
xlabel('Iterations')
ylabel('Mass (Abaqus) (tonnes)')
 
% Ploting Objective Value vs. Iteration
figure(4)
plot(x, Objective_vector)
xlim([1 31])
title('Objective Value vs. Iteration')
xlabel('Iterations')
ylabel('Objective Value')

% Making the 3 way plot for B.O.
data2 = readtable('optimization_data_x2n30');
data3 = readtable('optimization_data_x3n30');

Objective_vector_2 = data2.Objective;
Objective_vector_3 = data3.Objective;

Mass_F_A_vector_2 = data2.MassFromAbaqus;
Mass_F_A_vector_3 = data3.MassFromAbaqus;

Mass_W_P_vector_2 = data2.MassWithoutPenalty;
Mass_W_P_vector_3 = data3.MassWithoutPenalty;

Stress_vector_2 = data2.MaxStress;
Stress_vector_3 = data3.MaxStress;

x_2 = (1:30);
x_3 = (1:30);

figure (5)
plot(x,Objective_vector)
hold on
plot(x_2,Objective_vector_2)
plot(x_3,Objective_vector_3)
xlim([1 32])
title('Objective Value For Three Separate Runs')
xlabel('Iterations')
ylabel('Objective Value')
hold off

figure (6)
plot(x,Mass_F_A_vector)
hold on
plot(x_2,Mass_F_A_vector_2)
plot(x_3,Mass_F_A_vector_3)
xlim([1 32])
title('Mass (Abaqus) For Three Separate Runs')
xlabel('Iterations')
ylabel('Mass (Abaqus) (tonnes)')
hold off

figure (7)
plot(x,Mass_W_P_vector)
hold on
plot(x_2,Mass_W_P_vector_2)
plot(x_3,Mass_W_P_vector_3,'MarkerFaceColor',[0.9290 0.6940 0.1250]);
xlim([0 30])
title('Mass Without Penalty For Three Separate Runs')
xlabel('Iterations')
ylabel('Mass Without Penalty (tonnes)')
plot(1,3.69,'o','MarkerEdgeColor',[0.4940 0.1840 0.5560], 'MarkerSize', 10)
plot(1,2.79,'o','MarkerEdgeColor',[0.4660 0.6740 0.1880], 'MarkerSize', 10)
plot(1,2.43,'o','MarkerEdgeColor',[0.3010 0.7450 0.9330], 'MarkerSize', 10)
plot(7,4.07,'*','MarkerEdgeColor',[0.4940 0.1840 0.5560], 'MarkerSize', 10)
plot(11,4.76,'*','MarkerEdgeColor',[0.4660 0.6740 0.1880], 'MarkerSize', 10)
plot(10,3.26,'*','MarkerEdgeColor',[0.3010 0.7450 0.9330], 'MarkerSize', 10)
L = legend('Run 1','Run 2','Run 3','(x0,y0)=(1,3.69)','(x0,y0)=(1,2.79)','(x0,y0)=(1,2.43)','(x*,y*)=(7,4.07)','(x*,y*)=(11,4.76)','(x*,y*)=(10,3.26)');
L.AutoUpdate = 'off';
scatter(x, Mass_W_P_vector, 10, 'k', 'filled');
scatter(x_2,Mass_W_P_vector_2, 10,'k', 'filled')
scatter(x_3,Mass_W_P_vector_3, 10,'k', 'filled')
hold off

figure (8)
plot(x,Stress_vector)
hold on
plot(x_2,Stress_vector_2)
plot(x_3,Stress_vector_3)
xlim([1 32])
title('Max Stress For Three Separate Runs')
xlabel('Iterations')
ylabel('Max Stress (MPa)')
hold off

data4 = readtable('random_results.csv');

Mass_F_A_vector_4 = data4.Aba_Mass;

Mass_W_P_vector_4 = data4.Mass;

Stress_vector_4 = data4.MaxStress;

x_4 = (1:32);

figure (9)
plot(x,Mass_W_P_vector)
hold on
plot(x_4,Mass_W_P_vector_4)
xlim([0 30])
plot(1,3.69,'ko', 'MarkerSize', 10)
plot(7,4.07,'*','MarkerEdgeColor',[0 0.4470 0.7410], 'MarkerSize', 10)
plot(23,4.40,'*','MarkerEdgeColor',[0.8500 0.3250 0.0980], 'MarkerSize', 10)
title('Bayesian Optimization (B.O.) vs. Random Sample (R.S.)')
xlabel('Iterations')
ylabel('Mass Without Penalty (tonnes)')
L = legend('Bayesian Optimization','Random Sample','(x0,y0)=(1,3.69)','B.O. (x*,y*)=(7,4.07)','R.S. (x*,y*)=(23,4.40)');
L.AutoUpdate = 'off';
scatter(x, Mass_W_P_vector, 10, 'k', 'filled');
scatter(x_4,Mass_W_P_vector_4, 10,'k', 'filled')
