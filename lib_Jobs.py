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

# Import gentable
from lib_RandomTable import *
from random import randint, random, seed

## Functions ###########################################################
##
def GetNdays(n):
    ''' Returns a list of day offset to map to the job list.
        INPUT: BTN (float) The Bilateral Trade Number
        OUTPUT: A sorted list of n integers between 0 and 6
    '''
    out = []
    for i in range(n):
        out.append(randint(0,7))
    out.sort()
    return out

def FreightVolume(BTN):
    ''' Encodes the volume of an individual job in dT for tramp freighters.
        INPUT: BTN (float) The Bilateral Trade Number
        OUTPUT: A float of a volume in dT
    '''
    if BTN <= 6.0:
        return max(1., Nd6(2,-10))
    elif BTN == 6.5:
        return max(1., Nd6(2,-7))
    elif BTN == 7.0:
        return max(1., Nd6(2,-2))
    elif BTN == 7.5:
        return max(1., Nd6(2,-2) * 5)   
    elif BTN == 8.0:
        return max(1., Nd6(2,-2) * 5) 
    else:
        return max(1., Nd6(2,-2) * 10)
    
def FreightBrackets(BTN):
    ''' Encodes the table of with daily and weekly volume in dT for tramp freighters.
        INPUT: BTN (float) The Bilateral Trade Number
        OUTPUT: A tuple with [min_day, max_day], [min_week, max_week]
    ''' 
    if BTN <= 5.0:
        return [0,0], [0,5]
    elif BTN == 5.5:
        return [0,0], [0,5]
    elif BTN == 6.0:
        return [0,0], [5,10]  
    elif BTN == 6.5:
        return [0,5], [10,50]
    elif BTN == 7.0:
        return [5,10], [50,100]
    elif BTN == 7.5:
        return [10,50], [100,500]   
    elif BTN == 8.0:
        return [10,50], [500,1000]
    elif BTN == 8.5:
        return [50,100], [1000,5000]
    else:
        return [100,500], [10000,50000]   
    
def FreightBasePrice(week):
    ''' Encodes the table of base prices for tramp freight jobs, per parsecs, with respect to lead time.
        INPUT: week (int) The number of week ahead to the job
        OUTPUT: A list with [ 1 parsec, 2+ parsec ].
    ''' 
    if week < 2:
        return [700, 650]
    elif week < 4:
        return [670, 605]
    elif week < 4:
        return [640, 570]
    elif week < 8:
        return [570, 505]
    elif week < 12:
        return [505, 450]
    else:
        return [450, 400]
    
def FinalePrice( MoS ):
    ''' Encodes the table of negiciation outcomes for bids on tramp freight jobs.
        INPUT: MoS (int) The margin of success of the bid
        OUTPUT: A factor to modify the payoff of a job.
    '''    
    if MoS <= -10:
        return 0.5
    elif MoS <= -7:
        return 0.8
    elif MoS <= -5:
        return 0.85
    elif MoS <= -3:
        return 0.9
    elif MoS <= -1:
        return 0.95
    elif MoS <= 1:
        return 1.0
    elif MoS <= 3:
        return 1.05 
    elif MoS <= 5:
        return 1.1
    elif MoS <= 7:
        return 1.15 
    elif MoS <= 9:
        return 1.20    
    else:
        return 1.5
    
## Job Logics and generators ###########################################
##  
def PriceMods( x ):
    ''' Compute the modifier for the bid of a job based on route traffic, handling and shiping terms.
        INPUT: MoS (int) The margin of success of the bid
        OUTPUT: 3d6 modifer as an integer
    '''  
    out = 0
    
    # Modifier for the least busy jump
    route = set(x[8])
    rmod = {'M':-4, 'm':-2, '-':4}
    if route == set('M'):
        out -= 4
    if 'M' in route:
        route.remove('M')
    if route == set('m'):
        out -= 2
    elif route == set('-'):
        out += 4
        
    # Handling
    if x[2] != 'none':
        temp = randint(1,4)
        out += temp
        x[2] = x[2] + '+' * (temp-1)
        
    # Terms
    temp = {'FOB':-1, 'FAS':-2, 'EXW':-3, 'DES':1, 'DEQ':2, 'DFD':3}
    if x[3] in temp:
        out += temp[x[3]]    
    
    return out
        
def FreightJob(BTN):
    ''' Generate a single tramp freight job.
        INPUT: BTN (float) The Bilateral Trade Number for a run
        OUTPUT: The data defining a job as a list
    ''' 
    # Volume
    dTon = FreightVolume(BTN)
    
    # Cargo Type
    cargo_type = Random3d6('CargoType', ThreeD6())[0]
    
    # Handling
    handling = []
    n = 1
    while n > 0:
        temp = Random3d6('SpecialHandling', ThreeD6())[0]
        if temp == '2X':
            n += 1
        if not temp in handling and temp != '2X':
            handling.append(temp)
            n -= 1
    if len(handling) > 1 and 'none' in handling:
        handling.remove('none')
    handling = ', '.join(handling)
    
    #terms
    terms = Random3d6('ShippingTerms', ThreeD6())[0]
    
    
    return [dTon, cargo_type, handling, terms]

def FreightJobs(BTN, minpk=10, maxpk=50):
    ''' Create a random list of jobs fitting within the boundaries of a minimum and a maximum.
        INPUT: BTN (float) The Bilateral Trade Number for a run
               minpk (int) The minimum dT of the combined jobs
               maxpk (int) The maximum dT of the combined jobs
               
        OUTPUT: A list of job entities.
    ''' 
    total = 0
    
    jobs = []
    
    maxpk = randint(minpk, maxpk)
    
    while total < maxpk:
        j = FreightJob(BTN)
        if j[0] > 1.0:
            jobs.append(j)
            total += jobs[-1][0]
        
    return jobs
    
def FreightMarketOneWorld(BTN, dest_name='Nusku', volumes=[], dayofweek = 0, myseed=None):
    ''' Generates 4 weeks of jobs as a list for a particular run.
        INPUT: BTN (float) The BTN of a particular run
               dest_name (string) Name of destination world
               volumes (list of floats) A list of freight volume modifiers as computed by market fluctuations.
               dayofweek (int) The index of the current day of week, used to deleted jobs taking place in the past.
               myseed (int) A seed to use for a particular run, at a particular time.
        OUTPUT: A list of jobs spanning up to 4 weeks.
    '''  
    # Seeding
    if seed:
        seed(myseed)
        
    # Get brackets
    bkts = FreightBrackets(BTN)
    
    total_load = []
    
    if not volumes:
        volumes = [1.0]*4
    
    for week in range(4):
        # Get jobs
        load = FreightJobs(BTN, int(bkts[1][0] * volumes[week]), int(bkts[1][1] * volumes[week]) )
        
        # Geberate times
        days = GetNdays(len(load))
        
        # Marry them
        for i in range(len(load)):
            load[i].append(days[i]+(week*7))
            load[i].append(dest_name)
            load[i].append(FreightBasePrice(week))
        
        total_load.extend(load)
    
    # Remove past days
    out = []
    for job in total_load:
        if job[4] >= dayofweek:
            job[4] -= dayofweek
            out.append(job)
        
    return out
        
    
    
if __name__ == '__main__':
    FreightMarketOneWorld(10.0)        
