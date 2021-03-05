close all

%********* Exact cover *********%
bruteforce = logical(true);
diff = logical(true);
shgo = logical(true);

plot_exact_cover(bruteforce, diff, shgo)
%*******************************%


%********* Equal Size Partition *****%



%*******************************%





function plot_exact_cover(bruteforce, diff, shgo)

if bruteforce    
    data_bruteforce = load("data/exact_cover/bruteforce.mat")
    
    gammas = data_bruteforce.gammas;
    betas = data_bruteforce.betas;
    results = data_bruteforce.results;

    surf(gammas, betas,results)
end
if diff
    hold on
    data_diff_p1 = load("data/exact_cover/differential_evolution_p1.mat")
    plot3(data_diff_p1.x(2), data_diff_p1.x(1), data_diff_p1.fun, 'or')
    
end
if shgo
    hold on
    data_shgo_p1 = load("data/exact_cover/shgo_p1.mat")
    data_shgo_p2 = load("data/exact_cover/shgo_p2.mat")
    data_shgo_p3 = load("data/exact_cover/shgo_p3.mat")
    data_shgo_p4 = load("data/exact_cover/shgo_p4.mat")
    
    plot3(data_shgo_p1.x(2), data_shgo_p1.x(1), data_shgo_p1.fun, 'xb')
  
end
end



function plot_equal_size_partition(bruteforce, diff, shgo)

if bruteforce    
  
end
if diff

end
if shgo
    
end
end


