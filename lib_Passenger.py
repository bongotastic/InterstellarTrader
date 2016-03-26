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

## Imports #######################################################################
##

# Internal imports
import lib_RandomTable as libRT

# External imports
from random import choice, randint

## Functions #####################################################################
##

def GetOnePassenger():
    '''
    '''
    
    # output
    out ={'kind':None}
    
    # Table 
    while not out['kind']:
        # Dice
        dice = libRT.d66() 
        
        # Table
        x = libRT.Randomd66('RandomPassenger', dice)
        
        # Identity
        out['kind'] = x[0]
            
        # Secret
        x = libRT.Randomd66('PassengerSecret', libRT.d66())
        if x[0] != '-':
            out['secret'] = x[0]
            
            if len(x) > 1:
                out['secret'] += '(%s)'%(choice( x[1].split(',') ))            
        
        
        # Gender
        out['gender'] = libRT.Random3d6('gender', libRT.Nd6())[0]
            
            
    
    # Returns
    return out

def GeneratePassengers(BTN):
    '''
    '''
    
    # Total number
    n_tot = libRT.Nd6(1,-1) * BTN
    n = {'high':0, 'medium':0, 'low':0}
    n['high'] = n_tot
    
    # Low passage
    n['low'] = randint( 0 , n['high'])
    n['high'] -= n['low']
    n['low'] = randint(0,n['low'])
    
    # Medium passage
    if n_tot:
        n['medium'] = randint( 0 , n['high'])
        n_tot -= n['medium']
        n['medium'] = randint(0, n['medium'])
    
    # High
    n['high'] = randint(0, n['high'])
    
    # output
    out = {'high':[], 'medium':[], 'low':[]}
    
    for k in out:
        for i in range(n[k]):
            out[k].append( GetOnePassenger() )
            
    return out
    
def PrettyPrint( x ):
    out = 'Passage\tGender\tType\tSecret\n'
    
    for k in ['high', 'medium', 'low']:
        for p in x[k]:
            out += '%s\t%s\t%s\t%s\n'%(k, p.get('gender','-'), p.get('kind','-'), p.get('secret','-') )
    
    return out


if __name__ == '__main__':
    
    x = GeneratePassengers(10)
    print PrettyPrint(x)