import os
import numpy as np
rnd = np.random.RandomState(2021)
# Initiating a random state with a seed to make sure everybody
# has the same data locally after they've run the script.


# NOTE
# This was a quick and dirty solution, if there are possible
# solution missing that are relevant please modify this
# script to generate them too.

# possible things to sort by
#  W_max, len(W)

def one_exactly_full_truck(num_of_qubits=10, max_tries=10000):
    hash_set = set()

    tries = 0
    while tries < max_tries:
        tries += 1

        # This could probably be improved 
        I = random_integer(1, max(num_of_qubits//2, 4))
        W = random_integer(1, max(num_of_qubits//2, 4), I)
        W_max = sum(W)

        if not valid_instance(W, W_max, I, num_of_qubits): continue

        
        data = {'W': W, 'W_max': W_max}
        if str(data) in hash_set: continue
        hash_set.add(str(data))

        # Who dosen't want to yell sometimes?
        yield data


def only_one_item_per_truck(num_of_qubits=10, max_tries=10000):
    hash_set = set()

    tries = 0
    while tries < max_tries:
        tries += 1

        I = random_integer(1, max(num_of_qubits//2, 4))
        W = random_integer(1, max(num_of_qubits//2, 4), I)

        smallest = min(W)

        if I != 1:
            second_smallest = np.sort(W)[1]
            W_max = random_integer(smallest, second_smallest + smallest - 1)
        else:
            W_max = random_integer(smallest, smallest * 2 - 1)

        if not valid_instance(W, W_max, I, num_of_qubits): continue
        
        data = {'W': W, 'W_max': W_max}
        if str(data) in hash_set: continue
        hash_set.add(str(data))

        yield data


def more_or_less_random(num_of_qubits=10,max_tries=10000):
    hash_set = set()

    tries = 0
    while tries < max_tries:
        tries += 1

        I = random_integer(1, max(num_of_qubits//2, 4))
        W = random_integer(1, max(num_of_qubits//2, 4), I)

        W_max = (num_of_qubits - I*I) // I

        if not valid_instance(W, W_max, I, num_of_qubits): continue
        
        data = {'W': W, 'W_max': W_max}
        if str(data) in hash_set: continue
        hash_set.add(str(data))

        yield data


def items_with_equal_weights(num_of_qubits=10,max_tries=10000):
    hash_set = set()

    tries = 0
    while tries < max_tries:
        tries += 1

        I = random_integer(1, max(num_of_qubits//2, 4))
        W = np.zeros(I, int) + random_integer(1, max(num_of_qubits, 4))

        W_max = (num_of_qubits - I*I) // I

        if not valid_instance(W, W_max, I, num_of_qubits): continue
        
        data = {'W': W, 'W_max': W_max}
        if str(data) in hash_set: continue
        hash_set.add(str(data))

        yield data


def valid_instance(W, W_max, I, num_of_qubits):
    num_qubits = I*I + I*W_max

    if num_qubits != num_of_qubits: return False
    if max(W) > W_max: return False

    return True


def random_integer(low, high, size=None):
    if low == high: return low
    return rnd.randint(low, high + 1, size)



def encode_data(W, W_max):
    rep_arr = ','.join(map(str, np.sort(W)))
    return rep_arr + ':' + str(W_max)


def decode_data(s):
    parts = s.split(':')
    W = list(map(int, parts[0].split(',')))
    W_max = int(parts[1])
    
    return {'W': W, 'W_max': W_max}


def save_data(dataset, file_name):
    data_dir = os.path.join(os.path.dirname(__file__), 'data') 
    data_file = os.path.join(data_dir, file_name)
    os.makedirs(data_dir, exist_ok=True)

    string_data = ''
    for data in dataset: string_data += encode_data(**data) + os.linesep
    string_data = string_data.strip()

    # make sure it is ok if file is missing
    try: os.remove(data_file) 
    except FileNotFoundError: pass

    f = open(data_file, 'w')
    f.write(string_data)
    f.close()

        
def decode_file(file_name):
    data_dir = os.path.join(os.path.dirname(__file__), 'data') 
    data_file = os.path.join(data_dir, file_name)

    f = open(data_file, 'r')
    file_lines = f.readlines()
    f.close()

    for line in file_lines: 
        yield decode_data(line)


# Method signature says it all
def generate_and_save_a_lot_of_data():
    n_max = 30
    for n in range(1, n_max+1):
        print(n, '/', n_max)

        save_data(one_exactly_full_truck(n, 100000),\
                'one_exactly_full_truck_n'+str(n))
        save_data(only_one_item_per_truck(n, 100000),\
                'only_one_item_per_truck_n'+str(n))
        save_data(more_or_less_random(n, 100000),\
                'more_or_less_random_n'+str(n))
        save_data(items_with_equal_weights(n, 100000),\
                'items_with_equal_weights_n'+str(n))


def dev_funcs():
    for n in range(1, 30):
        #dataset = list(one_exactly_full_truck(n, 100000))
        #dataset = list(only_one_item_per_truck(n, 100000))
        #dataset = list(more_or_less_random(n, 100000))
        dataset = list(items_with_equal_weights(n))
        print(dataset)
        print('n:', n, 'number of instances:', len(dataset))
        input()


if __name__ == '__main__':
    generate_and_save_a_lot_of_data()
    #dev_funcs()
