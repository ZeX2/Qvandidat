def get_problem_list():
    problem_list = [{'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 1, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 2, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 3, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 4, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 5, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 6, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 7, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 1, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 2, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 3, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 4, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 5, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 6, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 7, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 1, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 2, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 3, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 4, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 5, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 6, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 7, 'noise': True},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 1, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 2, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 3, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 4, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 5, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 6, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 8, 'p': 7, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 1, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 2, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 3, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 4, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 5, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 6, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 16, 'p': 7, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 1, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 2, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 3, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 4, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 5, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 6, 'noise': False},
                    {'W_max': 1, 'W': [1], 'A': 8, 'B': 4, 'C': 32, 'p': 7, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 1, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 2, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 3, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 4, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 5, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 6, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 7, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 1, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 2, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 3, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 4, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 5, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 6, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 7, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 1, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 2, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 3, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 4, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 5, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 6, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 7, 'noise': True},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 1, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 2, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 3, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 4, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 5, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 6, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 32, 'p': 7, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 1, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 2, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 3, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 4, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 5, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 6, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 64, 'p': 7, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 1, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 2, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 3, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 4, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 5, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 6, 'noise': False},
                    {'W_max': 2, 'W': [1, 1], 'A': 32, 'B': 4, 'C': 128, 'p': 7, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 1, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 2, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 3, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 4, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 5, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 6, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 7, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 1, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 2, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 3, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 4, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 5, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 6, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 7, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 1, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 2, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 3, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 4, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 5, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 6, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 7, 'noise': True},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 1, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 2, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 3, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 4, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 5, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 6, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 12, 'p': 7, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 1, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 2, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 3, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 4, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 5, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 6, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 24, 'p': 7, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 1, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 2, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 3, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 4, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 5, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 6, 'noise': False},
                    {'W_max': 1, 'W': [1, 1, 1], 'A': 12, 'B': 4, 'C': 48, 'p': 7, 'noise': False}]
    return problem_list