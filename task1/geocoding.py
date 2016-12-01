import geocoder
import requests
import csv
import sys

from tqdm import tqdm
import util

total = util.get_number_of_lines(sys.argv[1]) - 1
fake = bool(len(sys.argv) > 3 and sys.argv[3] == '--fake')

print('geocoding...')
with open(sys.argv[1]) as reader, open(sys.argv[2], 'w') as out:
    writer = csv.writer(out, delimiter=',')
    next(reader)
    if not fake:
        for row in tqdm(reader, total=total):
            if len(row) != 2:
                while True:
                    try:
                        ll = geocoder.yandex(row).latlng
                        break
                    except requests.exceptions.ReadTimeout:
                        print('ReadTimeOut')
                        continue
                    except requests.exceptions.ConnectionError:
                        print('ConnectionError')
                        continue
                    except Exception as e:
                        writer.writerow(row)
                        for row in reader:
                            writer.writerow(row)
                        raise e
                writer.writerow(ll)
            else:
                writer.writerow(row)
    else:
        with open('fake_geocoding_results.csv') as f:
            reader = csv.reader(f, delimiter=',')
            for row in tqdm(reader, total=total):
                writer.writerow(row)

