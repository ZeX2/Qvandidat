import json
import scipy.io
import numpy as np
from datetime import timedelta, datetime


def save_results(results, problem, dt=-1, file_name=None, extra_data={}, save_mat=True, save_json=True):
    x = results[0]
    fun = results[1]
    p = len(x) // 2
    
    dt_str = str(timedelta(seconds=dt))
    data = {'expected_value':fun, 'optimal_gammas':x[0:p], \
            'optimal_betas':x[p:p*2], 'problem_identifier':problem, \
            'now':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
            'deltatime':dt_str}

    data.update(extra_data)

    if file_name is None: file_name = problem

    if save_mat:
        scipy.io.savemat(file_name + '.mat', data)

    if save_json:
        with open(file_name + '.json', 'w') as fp:
            json.dump(data, fp, indent=4, cls=NumpyEncoder)
    
    return data


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
