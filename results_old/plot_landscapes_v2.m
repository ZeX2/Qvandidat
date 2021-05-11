clear;clc;close all

global M;
M = containers.Map;
d = get_results_data('angles*.mat', @pred);

for m = keys(M)
    k = m{1};
    a = unique(M(k));
    if length(a) == 7
       disp(k)
       disp(a) 
    end
    
end

p = 0;
for dd = d
    p = max(p, dd.p);
end

for data = get_results_data('landscape*.mat', @pred)
    
    gammas = data.gammas;
    betas = data.betas;
    results = data.landscape;

    figure('Name', data.file_name)

    surf(gammas, betas, -results)
    axis tight
    
    xlabel('gamma')
    ylabel('beta')
    zlabel('Expected value')
    title(data.file_name)
    
end


function ret=pred(data)
    W = data.problem.W;
    I = length(W);
    W_max = data.problem.W_max;
    noise = data.noise;
    p = data.p;
	ret = 0;
        
    %if W_max == 3; ret = 1; end
    
    %if I == 1 && W_max == 1; ret = 1; end
    %ret = ~noise;
    if noise && W_max == 2 && all(size(W) == size([1, 1])) && all(W == [1, 1])
        ret = 1; 
        
        key = get_key(data);

        global M
        if ~isKey(M,key); M(key) = []; end

        M(key) = [M(key) p];
    end
    

    
    %if I > 1; ret = 1; end
    %if I > 1 && all(W == W(1)); ret = 1; end
    
    %if W_max == 1; ret = 1; end
    
    %if all(size(W) == size([1, 1])) && all(W == [1, 1]); ret = 1; end
    
    %if sum(W) == W_max; ret = 1; end
    
    %if mod(sum(W), W_max) == 0; ret = 1; end
    
end

function key=get_key(data)
    key = "" + string(data.problem.A) + " " + string(data.problem.B) + " " + string(data.problem.C);
end




function ret=zeidan_pred(data)
    W = data.problem.W;
    I = length(W);
    W_max = data.problem.W_max;
    noise = data.noise;
	ret = 0;
    
    if ~noise && data.success; ret = 1; end
    
end