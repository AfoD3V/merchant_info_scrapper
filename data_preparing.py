import re

dict = {}

with open('work_files/csv_file.csv') as f:
    for number, line in enumerate(f):
        if number % 2 != 0:
            line = line.split(',')
            if line[3] != '?':
                dict[line[0]] = {
                    'Name': line[1],
                    'Region': line[2],
                    'Zone': line[3],
                }

for k, v in dict.items():
    print(v['Zone'])


for k, v in dict.items():
    print(k, v)