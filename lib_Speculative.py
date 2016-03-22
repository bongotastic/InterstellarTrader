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
import lib_RandomTable

# External imports
from random import choice

## Functions #####################################################################
##

def RandomTonnage( s ):
    ''' Determine a random tonnage from a substring in the format Yd(XZ)
        INPUT: s (string) a substring from the speculative table
        OUTPUT: A dT (float)
    '''
    # dice
    n = int(s[: s.find('d') ])
    out = lib_RandomTable.Nd6(n)
    
    # Multiplier (optional)
    if 'X' in s:
        mult = float( s[ s.find('X')+1 : ] )
        out *= mult
    
    return out

def Mass( dT, density ):
    ''' Determine the mass from a cargo, given a dT and a density
        INPUT: dT (float) A size of a cargo in displacement ton
               density (float) The number of tons per dT
        OUTPUT: A mass in ton (float)
    '''
    return dT * float(density)


def Legality( s ):
    ''' Infer the legality class from a selection of classes as ASCII characters
        INPUT: s (string) a substring from the speculative table
        OUTPUT: A fully formed string with a qualitative descriptor.
    '''
    x = int(choice(s))
    temp = ['WMD', 'Restricted', 'Military', 'Controlled', 'Hazardous', 'safe', 'unrestricted']    
    out = 'LC%d - (%s)'%(x, temp[x])
    return out
    
    
def CargoType( s ):
    ''' Determine the type of cargo against a list of allowed typed
        INPUT: s (string) a substring from the speculative table
        OUTPUT: A cargo type (strong)
    '''
    out = lib_RandomTable.Random3d6('CargoType', lib_RandomTable.Nd6(3))[0]
    
    # RO/RO
    if out == 'RO/RO':
        if 'RO' in s:
            return 'RO/RO'
        else:
            out = 'break bulk'
            
    # Container
    if out == 'container':
        return out
    
    # Break bulk
    if out == 'break bulk':
        return 'break bulk'
    
    # shortcode
    t = out.split()
    scode = t[0][0] + t[1][0]
    if not scode in s:
        out = 'break bulk'
    return out
    
def Cost( qunt, price ):
    ''' Determine the base cost of a speculative cargo 
        INPUT: qnty (float) A cargo size in dT
               price (float) A base price per dT from the table
        OUTPUT: A cost as a string (string)
    '''
    price = qunt * price
    
    kilo = price / 1000.    
    if kilo < 1000.:
        return '%.1f KCr'%(kilo)
    
    kilo /= 1000.
    return '%.1f MCr'%(kilo)
    
    
def SpecialHandling( legal ):
    ''' Determine a cargo quirk from a custom table, also triggers the selection of a legality class
        INPUT: legal (string) a substring itemizing list a possible LC for this cargo from the speculative table
        OUTPUT: A tuple of ( handling , legality )
    '''
    out = lib_RandomTable.Random3d6('SpeculativeHandling', lib_RandomTable.Nd6())
    
    temp = set(legal).intersection(set(out[1]))
    if temp:
        return out[0], Legality(choice(list(temp)))
    else:
        return 'none', Legality(choice(legal))

def GetOneCargo():
    ''' Determine one speculative cargo with all of the possible metadata
        OUTPUT: A cargo as a dictionary. 
    '''
    # Roll on the main table once
    x = lib_RandomTable.Randomd66('speculative', lib_RandomTable.d66())
    
    out = {}
    out['Type'] = x[0]
    out['dT'] = RandomTonnage( x[3] )
    out['Mass'] = Mass(out['dT'], x[4])
    out['Cost'] = Cost(out['dT'] , int( x[1] ))
    out['Reaction modifiers'] = x[2].split(',')
    out['Cargo type'] = CargoType( x[5] )
    out['special'], out['Legality'] = SpecialHandling( x[6] )
    
    # VOlatility
    out['Volatility'] = lib_RandomTable.Random3d6('volatility', lib_RandomTable.Nd6(3))
    
    return out

def PrettyPrint( x ):
    ''' Determine an ASCII output representation for a cargo
        INPUT: x (dictionary) a cargo's metadata
        OUTPUT: A string representation (string)
    '''
    out = 'Type: %s [%d dT (%.1f T)]\nCost: %s\n'%(x['Type'], x['dT'], x['Mass'], x['Cost'])
    out += 'Handling: %s\nLegality: %s\nPrice Volatility: %s'%(x['Cargo type'], x['Legality'], x['Volatility'][0])
    if x['special'] != 'none':
        out += '\nQuirk: %s'%(x['special'])
    
    return out
    

if __name__ == '__main__':
    fout = open('500cargoes.txt', 'w')
    for i in range(500):
        stock = GetOneCargo()
        fout.write('Cargo %d -------------------------\n'%(i+1)  + PrettyPrint(stock) + '\n\n')
    fout.close()