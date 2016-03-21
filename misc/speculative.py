''' Speculative cargo generator
    cblouin@dal.ca
'''

import gentable
from random import choice


def RandomTonnage( s ):
    # dice
    n = int(s[: s.find('d') ])
    out = gentable.Nd6(n)
    
    # Multiplier (optional)
    if 'X' in s:
        mult = float( s[ s.find('X')+1 : ] )
        out *= mult
    
    return out

def Mass( dT, density ):
    return dT * float(density)

def Legality( s ):
    x = int(choice(s))
    temp = ['WMD', 'Restricted', 'Military', 'Controlled', 'Hazardous', 'safe', 'unrestricted']    
    out = 'LC%d - (%s)'%(x, temp[x])
    return out
    
    
def CargoType( s ):
    out = gentable.Random3d6('CargoType', gentable.Nd6(3))[0]
    
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
    price = qunt * price
    
    kilo = price / 1000.    
    if kilo < 1000.:
        return '%.1f KCr'%(kilo)
    
    kilo /= 1000.
    return '%.1f MCr'%(kilo)
    
    
    
def SpecialHandling( legal ):
    out = gentable.Random3d6('SpeculativeHandling', gentable.Nd6())
    
    temp = set(legal).intersection(set(out[1]))
    if temp:
        return out[0], Legality(choice(list(temp)))
    else:
        return 'none', Legality(choice(legal))

def GetOneCargo():
    # Roll on the main table once
    x = gentable.Randomd66('speculative', gentable.d66())
    
    out = {}
    out['Type'] = x[0]
    out['dT'] = RandomTonnage( x[3] )
    out['Mass'] = Mass(out['dT'], x[4])
    out['Cost'] = Cost(out['dT'] , int( x[1] ))
    out['Reaction modifiers'] = x[2].split(',')
    out['Cargo type'] = CargoType( x[5] )
    out['special'], out['Legality'] = SpecialHandling( x[6] )
    
    # VOlatility
    out['Volatility'] = gentable.Random3d6('volatility', gentable.Nd6(3))
    
    return out

def PrettyPrint( x ):
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