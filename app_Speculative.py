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
outfile_name = '500cargoes.txt'


## Script ( No need to edit below this) ########################################
##

# Internal import
import lib_Speculative as libS

# External imports
import os.path

fout = open(os.path.join('outputs', '500cargoes.txt'), 'w')
for i in range(500):
    stock = libS.GetOneCargo()
    fout.write('Cargo %d -------------------------\n'%(i+1)  + libS.PrettyPrint(stock) + '\n\n')
fout.close()