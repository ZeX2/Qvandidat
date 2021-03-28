import os
import numpy as np

# Note: [low,high) is a half-open interval,
# see np.random.randint for details.
def gen_data(low = 1, high = 10, num_qubits = 4, max_tries = 100):

    return_data = set()

    tries = 0
    while(tries < max_tries):
        tries += 1

        n = int(num_qubits / 2)
        x = np.random.randint(low, high, size=(n))
        y = np.random.randint(low, high, size=(n))

        sx = sum(x)
        sy = sum(y)

        # make sure the sum is equal in both arrays
        if sx > sy: y[0] += sx - sy
        else:       x[0] += sy - sx

        if x[0] >= high or x[0] < low or y[0] >= high or y[0] < low:
            continue

        arr = np.concatenate((x, y))

        return_data.add(encode_data(arr, max(sx, sy)))

    return_string = ''
    for data in return_data: return_string += data + os.linesep
    return return_string.strip()


# encodes a row of data
def encode_data(arr, sol):
    rep_arr = ','.join(map(str, np.sort(arr)))
    return rep_arr + ':' + str(sol)
    

# decodes a row of data
def decode_data(s):
    parts = s.split(':')
    arr = list(map(int, parts[0].split(',')))
    sol = int(parts[1])
    return (arr, sol)

def gen_q4_q20():

    data_one_of_each_q = []

    for i in range(4, 21):
        data = gen_data(1, 11, i, 10000)
        #print(data)
        print('Data generated for q = ' + str(i))

        save_data(data, 'example_data_q' + str(i))

        data_one_of_each_q.append(np.random.choice(data.split(os.linesep)))
    return_string = ''
    for data in data_one_of_each_q: return_string += data + os.linesep

    save_data(return_string.strip(), 'example_data_q4_q20')

def save_data(data, file_name):
    script_dir = os.path.dirname(__file__)
    example_file = os.path.join(script_dir,'data', file_name)

    f = open(example_file, 'w')
    f.write(data)
    f.close()
        
def decode_file(file_name):
    script_dir = os.path.dirname(__file__)
    example_file = os.path.join(script_dir,'data', file_name)

    f = open(example_file, 'r')
    file_lines = f.readlines()
    f.close()

    for line in file_lines: 
        yield decode_data(line)

def example():
    data = gen_data(1, 11, 4, 10000)
    #print(data)

    save_data(data, 'example_data')
    
    f = open(example_file, 'r')
    file_lines = f.readlines()
    f.close()

    string_data = ''
    for line in file_lines:
        (arr, sol) = decode_data(line)

        # do something useful here
        # we'll test encode_data and decode_data!

        string_data += encode_data(arr, sol) + os.linesep

    string_data = string_data.strip()

    # I've never used assert in python
    assert(data == string_data)
    print('Everything seem fine!')
    

#gen_q4_q20()
