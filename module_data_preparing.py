import re

dict = {}

with open('work_files/csv_file.csv') as f:
    for number, line in enumerate(f):
        # Filtering every other line
        if number % 2 != 0:
            line = line.split(',')

            # Checking if line is filled with data
            if line[3] != '?':

                # Iterating over all items inside item_list
                with open('work_files/item_list.txt', 'r') as item_list:
                    for item in item_list:
                        item_re = re.search(item, line[5])
                        # If item is in 'wanted list'
                        if item_re:
                            # append zone
                            zone_re = re.match("^[A-Z][a-z]+ [A-Z][a-z]+", line[3])
                            # append link for map
                            link_re = re.search("images.*jpg", line[3])
                            # make a dict of values with key setted as number corresponding to concrete order number
                            dict[int(line[0]) // 2] = {
                                'Name': line[1],
                                'Region': line[2],
                                'Zone': zone_re.group(),
                                'Link': 'https://lostmerchants.com/' + link_re.group(),
                                'Item': f'{item_re.group()}'
                            }

for k, v in dict.items():
    print(k, v)
