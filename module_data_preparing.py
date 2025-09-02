"""Data Processing Module for Merchant Items

This module processes scraped merchant data to identify valuable items and
formats the data for API consumption.

Features:
    - Filters merchant data for specific valuable items
    - Processes raw CSV data into structured format
    - Prepares data for API endpoint usage
    - Pattern matching for item identification

Note: This code is deprecated and kept for reference only.
"""

import re


class RareItem:
    """
    A class used for filtering csv file and checking for valuable items

    ...

    Methods
    -------
    data_formatter()
        Function is loading csv file from specified direction, filtering provided
        data and returning ready data set.

    """
    def __init__(self):
        self.data_dictionary = {}

    def data_formatter(self) -> dict[int, dict[str, str]]:
        """Method for opening file prepared by scraper module to work with it, goal of function
        is to check if any of live merchants have for-sell any valuable item, at the same time
        this method is preparing data to be ready for later use of api.

        Returns
        -------
        dictionary
            With inside key of int type, which is representing order of merchants, than as a value
            of specified key we have another dict which is representing important data fields ->
            Name; Region; Zone; Link; Item

        """
        # Opening file to work with
        with open('work_files/csv_file.csv', 'r') as f:
            for line_number, line in enumerate(f):
                # Filtering every other line
                if line_number % 2 != 0:
                    line = line.split(',')
                    # Checking if line is filled with data
                    if line[3] != '?':
                        # Iterating over all items inside item_list which is inside item_list.txt file
                        with open('work_files/item_list.txt', 'r') as item_list:
                            for item in item_list:
                                item_re = re.search(item, line[5])
                                # If item is in 'wanted list'
                                if item_re:
                                    # Append zone
                                    zone_re = re.match('^[A-Z][a-z]+ [A-Z][a-z]+', line[3])
                                    # Append link for map
                                    link_re = re.search('images.*jpg', line[3])

                                    # make a dict of values with key sett as number corresponding
                                    # to concrete order number
                                    self.data_dictionary[int(line[0]) // 2] = {
                                        'Name': line[1],
                                        'Region': line[2],
                                        'Zone': zone_re.group(),
                                        'Link': 'https://lostmerchants.com/' + link_re.group(),
                                        'Item': f'{item_re.group()}'
                                    }
        return self.data_dictionary


"""
Basic usage:

1. Create instance of RareItem class
a = RareItem()

2. Create a variable for storing formatted dict from data_formatter() function return
b = a.data_formatter()
"""
