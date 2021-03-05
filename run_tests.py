import os
import argparse

parser = argparse.ArgumentParser(description='A helper to run tests.')

parser.add_argument('problem', metavar='PROBLEM',
                    help='Run tests for specified PROBLEM. Valid options are ex for Pontus exact cover and eq for equal size partition')

args = parser.parse_args()

if args.problem == 'ec' or args.problem == 'exact' or \
        args.problem == 'exact_cover' or args.problem == 'ex':

    os.system('python -m unittest tests' +
              os.path.sep + 'exact_cover_tests.py')

elif args.problem == 'eq' or args.problem == 'equal' or \
        args.problem == 'equal_sise_partition' or args.problem == 'esp':

    os.system('python -m unittest tests' +

              os.path.sep + 'equal_size_partition_tests.py')
else:
    parser.print_help()
    exit(0)
