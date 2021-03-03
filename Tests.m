close all

data = load("hej.mat")


gammas = data.gammas;
betas = data.betas;
results = data.results;

surf(gammas,betas,results)