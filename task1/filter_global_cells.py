import sys
from tqdm import tqdm
import csv
from subprocess import check_output


lat_min = 51.612900
lat_max = 51.741699

lon_min = 39.135361
lon_max = 39.316978

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

delimiter = ','
total = int(check_output(['wc', '-l', input_file_name]).decode().split(' ')[0])

print('filtering cells...')
with open(input_file_name, 'r') as fin, open(output_file_name, 'w') as out:
    writer = csv.writer(out, delimiter=delimiter)
    reader = csv.reader(fin, delimiter=delimiter)
    next(reader)
    for row in tqdm(reader, total=total):
        if lon_min <= float(row[6]) <= lon_max and lat_min <= float(row[7]) <= lat_max:
            writer.writerow(row[6:8])

