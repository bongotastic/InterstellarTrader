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

# Name of the table
table_name = 'ShippingTerms'

# Kind of table 'd66' or '3d6'
table_type = '3d6'
dice1_mod_d66 = 0
dice2_mod_d66 = 0
dice_mod_3d6  = 0

# Pre-determined outcome? Set as a value, or to None for a random result
outcome = None


## Script ( No need to edit below this) ########################################
##

# Import
import lib_RandomTable as libRT

# d66 table
if table_type == 'd66':
    
    # Roll dice if not specified
    if outcome == None:
        outcome = libRT.d66(dice1_mod_d66, dice2_mod_d66)
        
    print libRT.Randomd66(table_name, outcome)

# 3d6 table
if table_type == '3d6':
    
    # Roll dice if not specified
    if outcome == None:
        outcome = libRT.Nd6(3, dice_mod_3d6)
        
    print libRT.Random3d6(table_name, outcome)