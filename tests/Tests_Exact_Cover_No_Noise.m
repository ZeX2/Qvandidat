close all

plot_exact_cover_depo()
plot_exact_cover_bitflip()
plot_exact_cover_phaseflip()
plot_exact_cover_ampdamp()
plot_exact_cover_phasedamp()

function plot_exact_cover_depo()
	files= dir(fullfile('data','exact_cover','depo', 'depo_f*.mat'));

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

function plot_exact_cover_bitflip()
	files= dir(fullfile('data','exact_cover','bitflip', 'bitflip_f*.mat'));

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

function plot_exact_cover_phaseflip()
	files= dir(fullfile('data','exact_cover','phaseflip', 'phaseflip_f*.mat'));

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

function plot_exact_cover_ampdamp()
	files= dir(fullfile('data','exact_cover','ampdamp', 'ampdamp_f*.mat'));

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

function plot_exact_cover_phasedamp()
	files= dir(fullfile('data','exact_cover','phasedamp', 'phasedamp_f*.mat'));

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
