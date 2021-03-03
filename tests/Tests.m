close all

data_bruteforce = load("data/bruteforce_0.mat")

data_diff_p1 = load("data/differential_evolution_p1_0.mat")
data_shgo_p1 = load("data/shgo_p1_0.mat")
data_shgo_p2 = load("data/shgo_p2_0.mat")
data_shgo_p3 = load("data/shgo_p3_0.mat")
data_shgo_p4 = load("data/shgo_p4_0.mat")


gammas = data_bruteforce.gammas;
betas = data_bruteforce.betas;
results = data_bruteforce.results;

surf(gammas, betas,results)
hold on

plot3(data_diff_p1.x(1), data_diff_p1.x(2), data_diff_p1.fun, 'or')
plot3(data_shgo_p1.x(1), data_shgo_p1.x(2), data_shgo_p1.fun, 'or')

xlim([4,5])
ylim([2,3])

figure 

plot(data_shgo_p4.x(4:8))
