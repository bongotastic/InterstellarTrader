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

# Input file in system to use
system_input_file = 'systemsIW'

# Unique string used to generate a random seed
campaign_salt = 'geronimo'

# World on which the jobs are posted (and origin) -- Must match a world in systems file
origin_world = 'Terra'

# Current time
current_year  = 2170
current_month = 3
current_day   = 12

# Filter down all jobs that can't fit in a particular cargo hold
max_dT = 300

# Filter out all job more than this number of days in the future
max_ahead = 50


## Script ( No need to edit below this) ########################################
##

# Internal Imports
from lib_Universe import *

# Create a Universe
U = TravellerUniverse(system_input_file, campaign_salt)

# Generate a Freight Market
current_timestamp = datetime(current_year, current_month, current_day)
U.FreightMarket(origin_world, current_timestamp)

# Filter
U.FilterJobs(maxdt= max_dT, maxage= max_ahead)

# Write out
outfile = '%s.%s.csv'%(origin_world, current_timestamp.strftime('%b%d.%Y'))
U.CSVjobs(outfile)