close all

plot_exact_cover_depo()

function plot_exact_cover_depo()
	files= dir(fullfile('data','exact_cover','nonoise', 'depo_f*.mat'));

    %for i=1:length(files)
    for i=[1 10 18]
        data_depo = load(fullfile(files(i).folder, files(i).name))
        bar(data_depo.dist_keys, data_depo.dist_values)
        alpha 0.7
        hold on
        % Well, it looked beautiful in mu mind!
        xline(data_depo.mean)
    end
	legend(string(1:length(files)))

end

