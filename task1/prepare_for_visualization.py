import sys
import os

path = sys.argv[1]
in_result = os.path.join(path, 'result')
out_coordinates = os.path.join(path, 'data.js')
out_counts = os.path.join(path, 'ddd.js')

# coordinates
with open(in_result) as res, open(out_coordinates, 'w') as out:
    l = [[float(x) for x in line.split('\u0001')[:2]] for line in res]
    out.write('var coords = {};'.format(l))

# numbers of addresses
with open(in_result) as res, open(out_counts, 'w') as out:
    l = [int(line.split('\u0001')[2]) for line in res]
    out.write('var count = {};'.format(l))
