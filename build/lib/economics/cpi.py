# -*- coding: utf-8 -*-

# cpi.py - Consumer Price Index data manipulation, computation and Class
# Copyright (C) 2013 Tryggvi Björgvinsson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import collections
import json
import requests
import editdistance


class CPI(object):
    """
    Provides a Pythonic interface to Consumer Price Index data packages
    """

    def __init__(self):
        """
        Initialise a CPI instance. Default data package location is the cpi
        data on http://data.okfn.org
        """
        
        # Store datapackage and country as instance variables
        self.raw_data = json.loads(requests.get("http://data.okfn.org/data/core/cpi/r/cpi.json").text)
        self.data = {}
        # Load the data into the data structures
        self.load()

    def load(self):
        """
        Load data with the data from http://data.okfn.org/data/core/cpi/r/cpi.json
        """

        # Loop through the rows of the datapackage with the help of data
        for row in self.raw_data:
            # Get the code and the name and transform to uppercase
            # so that it'll match no matter the case
            code = row['Country Code'].upper()
            if not row['Country Name'] in self.data.keys():
                self.data[row['Country Name']] = {}
            # Get the date (which is in the field Year) and the CPI value
            self.data[row['Country Name']][int(row['Year'])] = float(row['CPI'])
            
    def get(self, date=datetime.date.today(), country=None):
        """
        Get the CPI value for a specific time. Defaults to today. This uses
        the closest method internally but sets limit to one day.
        """
        try:
            return self.data[country][date.year]
        except:
            raise KeyError('Key not found in data')

    def closest(self, date=datetime.date.today(), country=None,
                limit=datetime.timedelta(days=366)):
        """
        Get the closest CPI value for a specified date. The date defaults to
        today. A limit can be provided to exclude all values for dates further
        away than defined by the limit. This defaults to 366 days.
        """

        # Try to get the country
        try:
            possible_countries = [self.data[country]]          
        except:
            possible_countries = [elem for elem in self.data.keys() if editdistance.eval(country,elem) < 3]
            if len(possible_countries) == 0:
                return "No country found, typo unlikely for ",country
                    
        # Find the closest date
        country_cpi = {}
        for country in possible_countries:
            min_year_diff = 1000
            min_year = 0
            for year in self.data[country]:
                if min_year_diff > abs(date.year - int(year)):
                    min_year_diff = abs(date.year - int(year))
                    min_year = year
            country_cpi[country] = self.data[country][min_year]
        if len(country_cpi) == 1:
            return country_cpi[country_cpi.keys()[0]]
        else:
            return country_cpi
