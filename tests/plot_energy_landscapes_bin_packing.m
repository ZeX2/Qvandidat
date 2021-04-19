clear;clc;close all


Folders= dir(fullfile('data','bin_packing','nonoise_sv'));
dirFlags = [Folders.isdir];
Folders = Folders(dirFlags);

for k = 3 : length(Folders)
    fprintf('Sub folder #%d = %s\n', k, Folders(k).name);
    folder = Folders(k);
    
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
    pause
    close all
    
end

