clear;clc;close all


Folders= dir(fullfile('data','bin_packing','nonoise_sv'));
dirFlags = [Folders.isdir];
Folders = Folders(dirFlags);

for k = 3 : length(Folders)
    fprintf('Sub folder #%d = %s\n', k, Folders(k).name);
    folder = Folders(k);
    
    listan = vfunc(Folders.name);
    
    listan_numbers = cellfun(@(x)dir_name2num(x), listan);
    [~,order] = sort(listan_numbers);
    sorted_listan = listan(order);
    
    
    files = dir(fullfile(folder.folder,folder.name,'*_bruteforce.mat'));
    
    for i = 1 : length(files)
        file = files(i);
        data = load(fullfile(file.folder, file.name));
        
        
        gammas = data.gammas;
        betas = data.betas;
        results = data.results;
        
        
        figure('Name', file.name)
        
        surf(gammas, betas,results)
        
        xlabel('gamma')
        ylabel('beta')
        zlabel('Expected value')
        title(file.name)
        
        
    end
    input('Press enter to continue')
    close all
    
end

function n = dir_name2num(dir)
    a = strsplit(dir, '_n')
    if length(a) > 1
        n = str2num(a{2})
    else
        n = -1
    end
    n = n + sum(a{1})*1000
end



function not_a_cell=vfunc(varargin)
    not_a_cell = varargin;
end
