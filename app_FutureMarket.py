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
##

# Campaign salt (Unique word, phrase for a campaign)
campaign_salt = 'geronimo'

# System to simulate
origin_system = 'Terra'

# Campaign anchor timestamp (By default Jan 1 2170)
anchor_year =  2170
anchor_month = 1
anchor_day   = 1

# Time of assessment
current_year  = 2170
current_month = 6
current_day   = 1

# Duration to project ahead
delta_week = 4

# Net Market Analysis Level of the Trader
MA_skill = 18


## Script ( No need to edit below this) ########################################
##

# External imports
from datetime import datetime

# Internal imports
import lib_FuturePrice as libFP

# Compute time
anchor_timestamp  = datetime(anchor_year, anchor_month, anchor_day)
current_timestamp = datetime(current_year, current_month, current_day)

# Week identifier (since the model work on a day to day basis)
current_week = (current_timestamp - anchor_timestamp).days / 7

# Build model
G = libFP.FuturePrice(campaign_salt, origin_system, current_week, delta_week)

print('wk: week ID\nPrice: Percent of base price\nVolume: Percent of base volume\nC&MA: Min, average and Max consensus forecast, and market Analysis.\n')
print('wk\tPrice\tVol\tCmin\tC\tCmax\tMAmin\tMA\tMAmax\n' + '-'*75 )
for week  in range(current_week, current_week + delta_week + 1):
    x = [G.GetPrice(week), G.GetVolume(week),
            G.GetConsensusPrice(week, bound='min'), G.GetConsensusPrice(week), G.GetConsensusPrice(week,bound='max'),
            G.GetMarketAnalysis(week, MA_skill, 0, bound='min'), G.GetMarketAnalysis(week, MA_skill, 0), G.GetMarketAnalysis(week, MA_skill, 0, bound='max')
            ]

    for i in range(len(x)):
        x[i] = str(int(x[i]))
    
    x = '%d\t'%(week) + '\t'.join(x)
    print  x
        
    