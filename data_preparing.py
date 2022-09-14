import re

dict = {}

with open('work_files/csv_file.csv') as f:
    for number, line in enumerate(f):
        if number % 2 != 0:
            line = line.split(',')
            if line[3] != '?':
                zone_re = re.match("^[A-Z][a-z]+ [A-Z][a-z]+", line[3])
                link_re = re.search("images.*jpg", line[3])
                dict[line[0]] = {
                    'Name': line[1],
                    'Region': line[2],
                    'Zone': zone_re.group(),
                    'Link': 'https://lostmerchants.com/' + link_re.group(),
                }


for k, v in dict.items():
    print(k, v)
