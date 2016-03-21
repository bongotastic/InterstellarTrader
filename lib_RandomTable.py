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

# Import Section
from random import randint
import os.path

# Constants
table_prefix = 'tables'
systems_prefix = 'systems'
outputs_prefix = 'outputs'


## Basic dice rolling ##################################################
##
def d66(d1mod = 0, d2mod = 0):
    ''' Generate a 1d6 1d6 concatenation
        INPUT: d1mod (int) a modifier to the first dice
               d2mod (int) a modifier to the second dice
        OUTPUT: d66 as a string
    '''
    #dice
    d1 = randint(1,6) + d1mod
    d2 = randint(1,6) + d2mod
    
    # Gather
    return str(d1) + str(d2)    

def Nd6(N=3, mod=0):
    ''' Generate Nd6 summation
        INPUT: N (int) number of dice (3 by default)
               mod (int) a modifier to the summation
        OUTPUT: An integer.
    '''    
    out = mod
    for i in range(N):
        out += randint(1,6)
    return out    

def ThreeD6(mod = 0):
    return Nd6(mod=mod)

## Table generation from text-encoded tables ###############################
##
def Randomd66(table, outcome):
    ''' Fetch an outcome from a d66 table
        INPUT: table (string) Name of the table (prefix without .txt)
               outcome (string) a valid dice roll
        OUTPUT: A dictionary data structure organizing the outcome.
    '''
    # Open Table
    data = open(os.path.join(table_prefix, table + '.txt'))
    for line in data:
        line = line.strip().split('\t')
        if outcome == line[0]:
            return line[1:]

    return []    

def Random3d6(table, outcome):
    ''' Fetch an outcome from a 3d6 table
        INPUT: table (string) Name of the table (prefix without .txt)
               outcome (int) A valid dice roll
        OUTPUT: A dictionary data structure organizing the outcome.
    '''
    # parse the table
    data = open(os.path.join(table_prefix, table + '.txt'))
    for line in data:
        line = line.strip().split('\t')
        
        # Solve range
        if not '-' in line[0]:
            if not '+' in line[0]:
                minv = maxv = int(line[0])
            else:
                t = line[0].replace('+','').strip()
                minv = int(t)
                maxv = 1000
        else:
            line[0] = line[0].split('-')
            minv = int(line[0][0])
            maxv = int(line[0][1])
            
        if outcome >= minv and outcome <= maxv:
            return line[1:]
        
    return line[1:]


## Testing code ########################################################
if __name__ == '__main__':
    pass