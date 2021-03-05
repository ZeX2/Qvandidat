close all


plot_brutforce_q4_to_q20()
function plot_brutforce_q4_to_q20()
    for i=4:20
        data_bruteforce = load("data/equal_size_partition/bruteforce_q"+string(i)+".mat");

        gammas = data_bruteforce.gammas;
        betas = data_bruteforce.betas;
        results = data_bruteforce.results;
        
        subplot(2, 4, i - 3)
        surf(gammas, betas,results)
        xlabel('gammas')
        ylabel('betas')
        title('q = ' + string(i))
        %view(45,45)
    end
end