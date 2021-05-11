function ret=get_results_data(file_pattern, pred)
    ret = [];
    files = dir(fullfile(file_pattern));
    for k = 1:length(files)
        file = files(k);
        %fprintf('File #%d = %s\n', k, file.name);

        data = load(fullfile(file.folder, file.name));

        if ~pred(data); continue; end
        data.file_name = file.name;
        ret = [ret data];
    end
end
