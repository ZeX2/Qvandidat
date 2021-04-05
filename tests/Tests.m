close all

%********* Exact cover *********%
bruteforce = logical(true);
diff = logical(false);
shgo = logical(false);

plot_exact_cover(bruteforce, diff, shgo)
%*******************************%


%********* Equal Size Partition *****%



%*******************************%


%d = 2;
%p = 0.00351329440734538;
%F = (1-1/d)*(1-4*p/3)+1/d


function plot_exact_cover(bruteforce, diff, shgo)

    if bruteforce    
        
        title('No noise')
        data_bruteforce = load("data/exact_cover/nonoise/bruteforce_ny.mat")
        
        gammas = data_bruteforce.gammas;
        betas = data_bruteforce.betas;
        results = data_bruteforce.results;

        surf(gammas, betas,results)
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        
        figure('Name', 'phasedamp')
        
        data_bruteforce = load("data/exact_cover/phasedamp_probability/bruteforce_ny.mat")

        gammas = data_bruteforce.gammas;
        betas = data_bruteforce.betas;
        results = data_bruteforce.results;

        surf(gammas, betas,results)
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        
        figure('Name', 'ampdamp')
        
        data_bruteforce = load("data/exact_cover/ampdamp_probability/bruteforce_ny.mat")

        gammas = data_bruteforce.gammas;
        betas = data_bruteforce.betas;
        results = data_bruteforce.results;

        surf(gammas, betas,results)
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        
        figure('Name', 'phasedamp p=0.8')
        
        data_bruteforce = load("data/exact_cover/phasedamp_probability/bruteforce_ny_p_80.mat")

        gammas = data_bruteforce.gammas;
        betas = data_bruteforce.betas;
        results = data_bruteforce.results;

        surf(gammas, betas,results)
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        
        
        figure('Name', 'ampdamp p=0.8')
        
        data_bruteforce = load("data/exact_cover/ampdamp_probability/bruteforce_ny_p_80.mat")

        gammas = data_bruteforce.gammas;
        betas = data_bruteforce.betas;
        results = data_bruteforce.results;

        surf(gammas, betas,results)
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        
      
    end
    
    if diff
        hold on
        data_diff_p1 = load("data/exact_cover/nonoise/differential_evolution_p1.mat")
        plot3(data_diff_p1.x(2), data_diff_p1.x(1), data_diff_p1.fun, 'or')
    end

    if shgo
        hold on
        data_shgo_p1 = load("data/exact_cover/nonoise/shgo_p1.mat")    
        plot3(data_shgo_p1.x(2), data_shgo_p1.x(1), data_shgo_p1.fun, 'og')
    end
    axis tight
end



function plot_equal_size_partition(bruteforce, diff, shgo)

    if bruteforce    

    end
    if diff

    end
    if shgo

    end
end



