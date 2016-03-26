'''
InterstellarTrader: Automating interstellar economics for the Traveller Universe.
Copyright (C) 2016  Christian Blouin (bongotastic@gmail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
    Instructions: Modify the parameters in the section below and execute this script using python
'''

## Parameters for your to specify #############################################

# Bilateral trade number (usually between 9 and about 5 from high to low traffic)
BTN = 8

# System name
origin_world = 'Terra'

# Current time
current_year  = 2170
current_month = 3
current_day   = 12

## Script ( No need to edit below this) ########################################
##

# Internal Imports
from lib_Passenger import *

# External Imports
from datetime import datetime

x = GeneratePassengers(10)

# Time
current_timestamp = datetime(current_year, current_month, current_day)

# Write out
outfile = '%s.%s.passengers.csv'%(origin_world, current_timestamp.strftime('%b%d.%Y'))
fout = open(outfile, 'w')
fout.write(PrettyPrint(x))
fout.close()

print PrettyPrint(x)