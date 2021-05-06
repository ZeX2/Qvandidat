

def get_problem_list():
    problem_list = [

            # statevector
                    {'W_max': 6, 'W': [4, 2], 'p': 1, 'noise': False},
                    {'W_max': 6, 'W': [4, 2], 'p': 2, 'noise': False},
                    {'W_max': 6, 'W': [4, 2], 'p': 3, 'noise': False},
                    {'W_max': 6, 'W': [4, 2], 'p': 4, 'noise': False},
                    {'W_max': 6, 'W': [4, 2], 'p': 5, 'noise': False},
                    {'W_max': 6, 'W': [4, 2], 'p': 6, 'noise': False},
                    {'W_max': 6, 'W': [4, 2], 'p': 7, 'noise': False},

                    {'W_max': 6, 'W': [4, 5], 'p': 1, 'noise': False},
                    {'W_max': 6, 'W': [4, 5], 'p': 2, 'noise': False},
                    {'W_max': 6, 'W': [4, 5], 'p': 3, 'noise': False},
                    {'W_max': 6, 'W': [4, 5], 'p': 4, 'noise': False},
                    {'W_max': 6, 'W': [4, 5], 'p': 5, 'noise': False},
                    {'W_max': 6, 'W': [4, 5], 'p': 6, 'noise': False},
                    {'W_max': 6, 'W': [4, 5], 'p': 7, 'noise': False},

                    {'W_max': 3, 'W': [1], 'p': 1, 'noise': False},
                    {'W_max': 3, 'W': [1], 'p': 2, 'noise': False},
                    {'W_max': 3, 'W': [1], 'p': 3, 'noise': False},
                    {'W_max': 3, 'W': [1], 'p': 4, 'noise': False},
                    {'W_max': 3, 'W': [1], 'p': 5, 'noise': False},
                    {'W_max': 3, 'W': [1], 'p': 6, 'noise': False},
                    {'W_max': 3, 'W': [1], 'p': 7, 'noise': False},

                    {'W_max': 3, 'W': [3], 'p': 1, 'noise': False},
                    {'W_max': 3, 'W': [3], 'p': 2, 'noise': False},
                    {'W_max': 3, 'W': [3], 'p': 3, 'noise': False},
                    {'W_max': 3, 'W': [3], 'p': 4, 'noise': False},
                    {'W_max': 3, 'W': [3], 'p': 5, 'noise': False},
                    {'W_max': 3, 'W': [3], 'p': 6, 'noise': False},
                    {'W_max': 3, 'W': [3], 'p': 7, 'noise': False},

                    # Diamond swap
                    {'W_max': 3, 'W': [1], 'p': 1, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [1], 'p': 2, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [1], 'p': 3, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [1], 'p': 4, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [1], 'p': 5, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [1], 'p': 6, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [1], 'p': 7, 'noise': True, 'routing': 'diamond'},

                    {'W_max': 3, 'W': [3], 'p': 1, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [3], 'p': 2, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [3], 'p': 3, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [3], 'p': 4, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [3], 'p': 5, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [3], 'p': 6, 'noise': True, 'routing': 'diamond'},
                    {'W_max': 3, 'W': [3], 'p': 7, 'noise': True, 'routing': 'diamond'},

                    # Linear swap
                    {'W_max': 6, 'W': [4, 2], 'p': 1, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 2], 'p': 2, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 2], 'p': 3, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 2], 'p': 4, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 2], 'p': 5, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 2], 'p': 6, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 2], 'p': 7, 'noise': True, 'routing': 'linear'},

                    {'W_max': 6, 'W': [4, 5], 'p': 1, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 5], 'p': 2, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 5], 'p': 3, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 5], 'p': 4, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 5], 'p': 5, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 5], 'p': 6, 'noise': True, 'routing': 'linear'},
                    {'W_max': 6, 'W': [4, 5], 'p': 7, 'noise': True, 'routing': 'linear'},

                    {'W_max': 3, 'W': [1], 'p': 1, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [1], 'p': 2, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [1], 'p': 3, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [1], 'p': 4, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [1], 'p': 5, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [1], 'p': 6, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [1], 'p': 7, 'noise': True, 'routing': 'linear'},

                    {'W_max': 3, 'W': [3], 'p': 1, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [3], 'p': 2, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [3], 'p': 3, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [3], 'p': 4, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [3], 'p': 5, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [3], 'p': 6, 'noise': True, 'routing': 'linear'},
                    {'W_max': 3, 'W': [3], 'p': 7, 'noise': True, 'routing': 'linear'}

                    ]

    return problem_list
