clear;clc;close all


files = dir(fullfile('data','bin_packing','nonoise_sv','*_bruteforce.mat'));
files = dir(fullfile('data','bin_packing','nonoise_sv_old','*_bruteforce.mat'));

for k = 1:length(files)
    file = files(k);
	fprintf('File #%d = %s\n', k, file.name);
    
    data = load(fullfile(file.folder, file.name));
    
    if ~pred(data); continue; end
    
    gammas = data.gammas;
    betas = data.betas;
    results = data.results;

    figure('Name', file.name)

    surf(gammas, betas, -results)

    xlabel('gamma')
    ylabel('beta')
    zlabel('Expected value')
    title(file.name)
    
end

function ret=pred(data)
    W = data.problem_identifier.W;
    I = length(W);
    W_max = data.problem_identifier.W_max;
	ret = 0;
        
    %if W_max == 3; ret = 1; end
    
    if W_max == 1; ret = 1; end
    if W_max == 2 && all(size(W) == size([1, 1])); ret = 1; end
    
    %if I > 1; ret = 1; end
    %if I > 1 && all(W == W(1)); ret = 1; end
    
    %if W_max == 1; ret = 1; end
    
    %if all(size(W) == size([1, 1])) && all(W == [1, 1]); ret = 1; end
    
    %if sum(W) == W_max; ret = 1; end
    
    %if mod(sum(W), W_max) == 0; ret = 1; end
    
end
