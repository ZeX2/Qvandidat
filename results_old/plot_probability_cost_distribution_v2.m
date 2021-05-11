clear;clc;close all

p1 = get_results_data('angles-p1*.mat', @pred_problem_instance2);
p2 = get_results_data('angles-p2*.mat', @pred_problem_instance2);
p3 = get_results_data('angles-p3*.mat', @pred_problem_instance2);
p4 = get_results_data('angles-p4*.mat', @pred_problem_instance2);
p5 = get_results_data('angles-p5*.mat', @pred_problem_instance2);
p6 = get_results_data('angles-p6*.mat', @pred_problem_instance2);
p7 = get_results_data('angles-p7*.mat', @pred_problem_instance2);

landscapes = get_results_data('landscape*.mat', @pred_problem_instance2);

[p1m, p1n] = get_avg_prob_per_category(p1, 1);
[p2m, p2n] = get_avg_prob_per_category(p2, 1);
[p3m, p3n] = get_avg_prob_per_category(p3, 1);
[p4m, p4n] = get_avg_prob_per_category(p4, 1);
[p5m, p5n] = get_avg_prob_per_category(p5, 1);
[p6m, p6n] = get_avg_prob_per_category(p6, 1);
[p7m, p7n] = get_avg_prob_per_category(p7, 1);


i = -1;
for landscape = landscapes
    i = i + 2;
    key = get_key(landscape);
    data = p1n(key);
    
    subplot(5, 8, i)
    
    
	prob_dist = data.probability_distribution_items;
    appr_ratio = data.approximation_ratio;
    
    s = sum(prob_dist(:,2));
    
    bar(prob_dist(:,1), prob_dist(:,2))
    axis tight
    ylim([0, 1])
    xlabel('Cost')
    ylabel('Probability')
    title(string(p1m(key)) + " " + string(s))
    
    subplot(5, 8, i + 1)
    
    data = landscape;
    gammas = data.gammas;
    betas = data.betas;
    results = data.landscape;

    %figure('Name', data.file_name)

    surf(gammas, betas, -results)
    shading interp
    axis tight
    
    xlabel('gamma')
    ylabel('beta')
    zlabel('Expected value')
    title(key)
end


for data = get_results_data('angles*.mat', @pred1)
    
    prob_dist = data.probability_distribution_items;
    appr_ratio = data.approximation_ratio;
    
    figure('Name', data.file_name)

    bar(prob_dist(:,1), prob_dist(:,2))
    axis tight
    ylim([0, 1])
    xlabel('Cost')
    ylabel('Probability')
    title(file.name)
end

function [M,N]=get_avg_prob_per_category(p, cost_for_optimal_solution)
    M = containers.Map;
    N = containers.Map;
    for pp = p
        key = get_key(pp);
        if ~isKey(M,key); M(key) = []; end
        costs = pp.probability_distribution_items(:, 1);
        probs = pp.probability_distribution_items(:, 2);
        M(key) = [M(key) probs(costs == cost_for_optimal_solution)];
        N(key) = pp;
    end
    
    for m = keys(M)
       M(m{1}) = mean(M(m{1}));
    end
end

function key=get_key(data)
    key = "" + string(data.problem.A) + " " + string(data.problem.B) + " " + string(data.problem.C);
end



function ret=pred_problem_instance2(data)
    W = data.problem.W;
    I = length(W);
    W_max = data.problem.W_max;
    noise = data.noise;
    p = data.p;
            
    % ret = ~noise && p == 1 && I == 2 && W_max == 2;
    %if W_max == 2 && all(size(W) == size([1, 1])); ret = 1; end
    
    ret = 0;
    if all(size(W) == size([1, 1])) && all(W == [1, 1]) && W_max == 2 && noise && A == 32 && B == 4 && C == 576
        ret = 1;
    end
    
    if all(size(W) == size([1])) && all(W == [1]) && W_max == 1 && noise && A == 8 && B == 4 && C == 12
        %ret = 1;
    end
    
    if all(size(W) == size([1, 1, 1])) && all(W == [1, 1, 1]) && W_max == 1 && noise && A == 12 && B == 4 && C == 324
        %ret = 1;
    end

    %if I > 1; ret = 1; end
    %if I > 1 && all(W == W(1)); ret = 1; end
    
    %if W_max == 1; ret = 1; end
    
    
    %if sum(W) == W_max; ret = 1; end
    
    %if mod(sum(W), W_max) == 0; ret = 1; end
    
end
