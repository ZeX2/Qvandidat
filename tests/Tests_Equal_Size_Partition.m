close all


plot_brutforce_q4_to_q20()
function plot_brutforce_q4_to_q20()
    views = [0 0; 90 0; 90 90; 45 45];
    
    for v=views'
        figure('Name', 'equal_size_partition' + strjoin(string(v), ''))
        files= dir(fullfile('data','equal_size_partition', '*.mat'));
        
        for i=1:length(files)
            data_bruteforce = load(fullfile(files(i).folder, files(i).name));

            gammas = data_bruteforce.gammas;
            betas = data_bruteforce.betas;
            results = data_bruteforce.results;

            subplot(3, 4, i)
            surf(gammas, betas, results)
            xlabel('gammas')
            ylabel('betas')
            title('q = ' + string(i + 3))
            view(v')
        end
    end
end