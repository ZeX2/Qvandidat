clear;clc;close all


instances=get_results_data('landscape*.mat', @pred);


for data = instances
    
    gammas = data.gammas;
    betas = data.betas;
    results = data.landscape;
    
    figure('Name', data.file_name)
    
    surf(betas, gammas, -results)
    axis tight
    shading interp
    xlabel('gamma')
    ylabel('beta')
    zlabel('Expected value')
    title(data.file_name)
end

landscapes_grouped_by_problem = group_by(instances, @group_pred);

for landscapes=landscapes_grouped_by_problem
    figure
    i = 0;
    for data = landscapes
        i = i + 1;
        subplot(1, 2, i);
        
        gammas = data.gammas;
        betas = data.betas;
        results = data.landscape;

        figure('Name', data.file_name)

        surf(betas, gammas, -results)
        axis tight
        shading interp
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        title(data.file_name)
    end
end

function b=group_by(instances, pred)
    M = containers.Map;
    for data = instances
        key = pred(data);
        if ~isKey(M,key); M(key) = []; end
        M(key) = [M(key) data];
    end
    
    b = {};
    i = 0;
    for m = keys(M)
        i = i + 1;
        b{i} = M(m{1});
    end
end

function ret=group_pred(data)
    p = data.problem;
    %p.noise = data.noise;
    fields = fieldnames(p);
    
    ret = "";
    for field = fields'
        ret = ret + field{1} + ": " + p.(field{1}) + ", ";
    end
end

function ret=pred(data)
    W = data.problem.W;
    I = length(W);
    W_max = data.problem.W_max;
    noise = data.noise;
	ret = 0;
        
    %if W_max == 3; ret = 1; end
    
    if I == 1 && W_max == 1; ret = 1; end
    ret = ~noise;
    ret = 1;
    %if W_max == 2 && all(size(W) == size([1, 1])); ret = 1; end
    
    %if I > 1; ret = 1; end
    %if I > 1 && all(W == W(1)); ret = 1; end
    
    %if W_max == 1; ret = 1; end
    
    %if all(size(W) == size([1, 1])) && all(W == [1, 1]); ret = 1; end
    
    %if sum(W) == W_max; ret = 1; end
    
    %if mod(sum(W), W_max) == 0; ret = 1; end
    
end
