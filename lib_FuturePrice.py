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

## Imports #############################################################
from random import randint, seed

## Function ############################################################
##
def FourD6():
    out = []
    for i in range(4):
        out.append(randint(1,6))
    return out

## Class declaration ###################################################
##

class FuturePrice:
    ''' This class creates a market fluctuation that is consistent over time for a given campaign. This prevents to 
        have to store any data as it can be generated on the fly when required. This genration is thus contingent to 
        a campaign salt (string), a system name, and a default present considered to be week 0.
    '''
    def __init__(self, salt, system, week_start = 0, time_span = 16):
        # Assumptions
        self.start_price = 100.0
        self.start_volume = 100.0
        
        self.price_volatility = 0.05
        self.price_regression = 0.2
        
        self.volume_volatility = 0.25
        self.volume_regression = 0.2
        
        # Seed 
        self.seed = hash(salt + system)
        
        # Storage
        self.price_dice = []
        self.volume_dice = []
        self.price = [self.start_price]
        self.volume = [self.start_volume]
        
        self.Generate(week_start, time_span)
        
    def Generate(self, week_start, time_span):
        # Set Seed
        seed(self.seed)
        
        # Proceed
        week = 0
        oldprice = self.start_price
        oldvolume = self.start_volume
        for week in range(week_start + time_span + 10):
            self.price_dice.append(FourD6())
            self.volume_dice.append(FourD6())
            
        # Generate true values
        for week in range(week_start + time_span + 1):
            oldp = self.price[-1]
            oldv = self.volume[-1]
            self.price.append(self.IterateParam(oldp,self.start_price,self.price_volatility,self.price_regression,self.price_dice[week]))
            self.volume.append(self.IterateParam(oldv,self.start_volume,self.volume_volatility,self.volume_regression,self.volume_dice[week]))
            
        
    def IterateParam(self, old, mean, volatility, regress, fourd):
        return old + (volatility * mean * (sum(fourd)-14)) + (regress * (mean - old))
    
    
    def GetPrice(self, week):
        if week < len(self.price):
            return self.price[week]
        
    def GetVolume(self, week):
        if week < len(self.volume):
            return self.volume[week]    
        
    def Analysis(self, dice, kind='consensus', critical=0, bound=None):
        # kind can be either consensus or market analysis, critical may be 1,0,-1
        # dice
        d = 1 + critical
        if kind == 'market analysis':
            d += 1
            
        dice = dice[:d]
        while len(dice) < 4:
            if bound == None:
                dd = randint(1,6)
            elif bound == 'min':
                dd = 1
            else:
                dd = 6
            dice.append( dd )
        
        return dice
    
    def GetConsensusPrice(self, week, bound=None):
        oldp = self.price[week-1]
        dice = self.Analysis(self.price_dice[week], bound=bound)
        return self.IterateParam(oldp, self.start_price, self.price_volatility, self.price_regression, dice)
    
    def GetMarketAnalysis(self, week, skill=10, mod=0, bound=None):
        oldp = self.price[week-1]
        crit = 0
        # Skills check 
        d = (skill+mod)
        MoS =  d -  (randint(1,6)+randint(1,6)+randint(1,6))
        if  d < 5 or MoS >= 10:
            crit = 1
        elif d > 16 or MoS <= -10:
            crit = -1
            
        newdice = self.Analysis(self.price_dice[week], 'market analysis', crit, bound)
        return self.IterateParam(oldp, self.start_price, self.price_volatility, self.price_regression, newdice)
  
  
        
## Testing code #############################################################
##
if __name__ == '__main__':
    G = FuturePrice('babble4', 'Terra')
    print G.GetPrice(2)
    print G.GetConsensusPrice(2, bound='min'), G.GetConsensusPrice(2), G.GetConsensusPrice(2,bound='max')
    print G.GetMarketAnalysis(2, 10, 0, bound='min'), G.GetMarketAnalysis(2, 10, 0), G.GetMarketAnalysis(2, 10, 0, bound='max')

    