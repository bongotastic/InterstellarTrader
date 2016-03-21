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

# External imports
from math import ceil
from operator import itemgetter
from random import random, seed
from datetime import datetime
import os.path

# Internal imports
from lib_Jobs import FreightMarketOneWorld, FinalePrice, PriceMods
from lib_FuturePrice import FuturePrice


def AdjacentHexes(i):
    return [i+1, i-1, i+100, i+101, i-100, i-99]



class TravellerSystem:
    def __init__(self, instring=''):
        self.name = ''
        self.trade_codes = []
        self.WTN = 0.0
        self.CR = 0
        self.TL = 9
        self.ID = 1974
        self.code = ''
        
        # 
        self.jumps = {}
        
        if instring:
            self.ParseInString(instring)
            
    def ParseInString(self, s):
        '''Instancitate from the string'''
        s = s.split('\t')
        
        self.ID = int(s[0])
        self.name = s[1]
        self.WTN = float(s[2])
        self.trade_codes = s[3].replace('"','').split(',')
        self.CR = int(s[4])
        self.TL = int(s[5])
        
    def RangeRings(self):
        out = {0:[], 1:[],2:{}}
        i = self.ID
        
        out[1].extend( AdjacentHexes(i) )
        
        temp = []
        for item in out[1]:
            temp.extend(AdjacentHexes(item))
            
        temp = set(temp)
        temp = temp.difference(out[1])
        temp = list(temp)
        temp.remove(self.ID)
        
        out[2] = temp
        
        return out
        
class TravellerUniverse:
    # Reference time that should be the earliest valid campaign date
    reftime = datetime(2170, 01, 01)
    
    def __init__(self, filename, salt):
        # Manage whole universe
        self.fname = os.path.join('systems', filename + '.txt')
        
        self.salt = salt
        
        # Systems
        self.systems = {}
        self.routes = []
        
        for line in open(self.fname):
            if line[0] == '#':
                continue
            
            if line[0] in ['M', 'm', 'f', '-']:
                self.routes.append(line.split('\t'))

            elif line != '\n':
                x = TravellerSystem(line)    
                self.systems[x.name] = x
                
        self.ConnectWorlds()
        
    def GetWorld(self, key):
        # Case 1: by name
        if key in self.systems:
            return self.systems[key]
        
        # Case 2: by coordinate
        for w in self.systems:
            if key == self.systems[w].ID:
                return self.systems[w]
        
        return None
        
    def ConnectWorlds(self):
        '''Create list of jumps.'''
        # Expand routes into pairs
        Major = []
        minor = []
        
        for route in self.routes:
            for i in range(1, len(route)-1):
                temp = route[i:i+2]
                if route[0] == 'M':
                    Major.append(temp)
                else:
                    minor.append(temp)
        
        # Process on world at the time
        for w in self.systems:
            W = self.systems[w]
            rings = self.RangeRings(w)
            
    def RangeRings(self, name):
        temp = self.systems[name].RangeRings()
        
        out = {0:[], 1:[], 2:[]}
        
        for i in range(3):
            for j in range(len(temp[i])):
                x = self.GetWorld(temp[i][j])
                if x:
                    out[i].append(x.name)
        return out
    
    def DistanceMap(self, origin, maxdist = 16):
        # A map of distances
        distmap = {origin:(0,'M')}
        
        nodes = {}
        nodes[origin] = {'route':'' , 'distance':0}
        probes = [origin]
        while probes:
            for r in self.routes:
                if probes[0] in r:
                    other = r[1:3]
                    other.remove(probes[0])
                    other = other[0]
                    if not other in nodes:
                        t = nodes[probes[0]]
                        nodes[other] = {'route':t['route']+r[0] , 'distance':t['distance']+int(r[3])}
                        probes.append(other)
                    else:
                        # replace path if shorter
                        t = nodes[probes[0]]
                        if t['distance']+int(r[3]) < nodes[other]['distance']:
                            nodes[other]['route'] = t['route']+r[0]
                            nodes[other]['distance'] = t['distance']+int(r[3])
                            
            probes = probes[1:]
                    
        
        return nodes
    
    def BTNdistance(self, d):
        if d < 2:
            return 0.0
        elif d < 3:
            return 0.5
        elif d < 6:
            return 1.0
        elif d < 10:
            return 1.5
        elif d < 20:
            return 2.0
        else:
            return 2.5
        
    def FreightMarket(self, system_name, timestamp):
        
        # Week
        self.start_week = self.WeekID(timestamp)
        self.start_date = timestamp
        
        # Firs day of week
        dow = self.DayOfWeek(timestamp)
        
        # Map
        nodes = self.DistanceMap(system_name, 10)
        
        # Price
        self.futures = FuturePrice(self.salt, system_name, self.start_week)
        
        # Predict volumes
        volumes = []
        for i in range(self.start_week, self.start_week+4):
            temp = max( 0.0, self.futures.GetVolume(i) / 100.0)
            volumes.append(temp)


        
        # Generate all freight streams
        jobs = []
        for w in nodes:
            if w == system_name:
                continue
            
            a = self.systems[w].WTN
            b = self.systems[system_name].WTN
            if abs(a-b) >= 2.0:
                BTN = (min(a,b) * 2) + 2.0
            else:
                BTN = a + b
            BTN -= self.BTNdistance( nodes[w]['distance'] )
        
            seed = self.salt + system_name + w + str(self.WeekID)
            
            temp = FreightMarketOneWorld( BTN , w, volumes, dow, seed)
            
            for i in range(len(temp)):
                # Add distance in parsec
                temp[i].append(nodes[w]['distance'])
                temp[i].append(nodes[w]['route'])
                
                # Compute a modification for the job
                mod = PriceMods( temp[i] )
                
                # Compute price estimate
                if temp[i][7] < 2:
                    price = temp[i][6][0]
                else:
                    price = temp[i][6][1] * temp[i][7]
                    
                restricted = 1.0
                # Restricted
                if 'restricted' in temp[i][2]:
                    price *= 2**(1+temp[i][2].count('+'))                
                    
                price = FinalePrice(mod) * price * temp[i][0]
                
                # Adjust the price to consensus market
                temp[i][6] = ceil(price * (self.futures.GetConsensusPrice(temp[i][0]/7)/100.0))
            
            
            jobs.extend(temp)
            
        jobs.sort(key=itemgetter(4))
        
        self.jobs = jobs
            
    def FilterJobs(self, maxdt = 300, maxage = 50 ):
        out = []
        
        for j in self.jobs:
            # Not all jobs in the future are already posted
            if (j[7] == 0 or random() <= 0.7**(j[7])) and j[0] <= maxdt:
                out.append(j)
                
        self.jobs = out
        
    def CSVjobs(self, fname):
        fout = open(os.path.join('outputs', fname), 'w')
        
        fout.write('Day,dT,Type,Destination,Handling,Terms,Expected bid,Distance,route\n')
        
        for s in self.jobs:
            fout.write('%d,%d,%s,%s,%s,%s,%d,%d,%s\n'%(s[4],s[0],s[1],s[5],s[2],s[3],s[6],s[7],s[8]))
            
        fout.close()
        
    def RefTime(self):
        return TravellerUniverse.reftime
    
    def WeekID(self, newtime):
        temp = newtime - self.RefTime()
        return temp.days/7
            
    def DayOfWeek(self, newtime):
        temp = newtime - self.RefTime()
        return temp.days%7
        
if __name__ == '__main__':
    U = TravellerUniverse('systemsIW', 'geronimo')
    U.FreightMarket('Apishlun', datetime(2170,2,20))
    U.FilterJobs()
    U.CSVjobs('Apishlun.May20th.csv')
    
    print U.WeekID( datetime(2170, 03, 11) )