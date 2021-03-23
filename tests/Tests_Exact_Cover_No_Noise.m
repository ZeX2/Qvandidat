close all

% plot_exact_cover_depo()
% plot_exact_cover_bitflip()
% plot_exact_cover_phaseflip()
% plot_exact_cover_ampdamp()
% plot_exact_cover_phasedamp()

%plot_exact_cover_all_noisemodels()
%plot_equal_size_partition_all_noisemodels()

function plot_exact_cover_all_noisemodels()
    folders = ["depo","phasedamp", "ampdamp", "phaseflip", "bitflip"];
    j = 0;
    for folder=folders
        j = j + 1;
        subplot(2, 3, j)
        files= dir(fullfile('data','exact_cover',folder,'*_f*.mat'));
        %is = 1:length(files);
        is = [1 10 18];
        
        fidelity = [];
        for i=is
            data = load(fullfile(files(i).folder, files(i).name));
            fidelity = [fidelity data.fidelity];
            b = bar(data.dist_keys, data.dist_values);
            alpha 0.7
            hold on
            % Well, it looked beautiful in my mind!
            x = xline(data.mean,'HandleVisibility','off');
            x.Color = b.FaceColor;
            x.LineWidth = 2;
        end
        title(folder)
        legend(num2str(fidelity', 'Fidelity: %.2f'))
    end
end


function plot_equal_size_partition_all_noisemodels()
    folders = ["depo","phasedamp", "ampdamp", "phaseflip", "bitflip"];
    subfolders = ["[ 3  6  7 10]","[ 4  6  8 10]","[ 1  1  3  5  8 10]","[ 3  4  8  8  9 10]","[ 2  6  6  8  8  8  8 10]","[ 1  1  3  6  7  9  9 10 10 10]","[ 1  3  5  6  6  8  9  9  9 10]","[ 2  2  3  3  4  5  5  6  7  8  9 10]","[ 2  3  4  4  6  8  9 10]","[1 1 1 2 3 3 4 5 6 6 9 9]"];
    
    for folder1=subfolders
        
        figure('Name', folder1)
        j = 0;
        for folder=folders
        
        j = j + 1;
        subplot(2, 3, j)
        files= dir(fullfile('data','equal_size_partition',folder, folder1,'*_f*.mat'));
        %is = 1:length(files);
        is = [1 10 18];
        
        fidelity = [];
        for i=is
            data = load(fullfile(files(i).folder, files(i).name));
            fidelity = [fidelity data.fidelity];
            b = bar(data.dist_keys, data.dist_values);
            alpha 0.7
            hold on
            % Well, it looked beautiful in my mind!
            x = xline(data.mean,'HandleVisibility','off');
            x.Color = b.FaceColor;
            x.LineWidth = 2;
        end
        title(folder)
        legend(num2str(fidelity', 'Fidelity: %.2f'))
        end
        
    end
end














function plot_exact_cover_depo()
	files= dir(fullfile('data','exact_cover','depo', 'depo_f*.mat'));

    %for i=1:length(files)
    for i=[1 10 18]
        data_depo = load(fullfile(files(i).folder, files(i).name))
        bar(data_depo.dist_keys, data_depo.dist_values)
        alpha 0.7
        hold on
        % Well, it looked beautiful in my mind!
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
