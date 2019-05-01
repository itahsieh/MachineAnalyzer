#!/usr/bin/env python3
import argparse
import sys

# usage
def usage():
        print ('''
            
    use the command "./viewer.py -h" to check out the usage
                    
''')


import sys
argv = sys.argv[1:]

if not argv:
    usage()
    sys.exit(2)


from viewer_opt import Opt, PlotKey

# parser
parser = argparse.ArgumentParser(prog='viewer', description = 'Vibrational data viewer')
parser.add_argument("-i", "--input", help="input data path", 
                    dest="data", default="default")

parser.add_argument('plot', 
                    default="default", help = "plot options: "+str(PlotKey))

parser.add_argument('--show', dest='show_gui', action='store_true',
                    default=False, help = "enable GUI window")

parser.add_argument('--raw', dest='raw_data', action='store_true',
                    default=False, help = "raw data tag")

parser.add_argument('--3ax-raw', dest='_3ax_raw_data', action='store_true',
                    default=False, help = "3-axes raw data tag")

parser.add_argument('--axis', dest='axis', default=None, 
                    help = "data of which axis, specify 'x', 'y', or 'z'")

parser.add_argument('--range', dest='record_range', default=None, 
                    help = "range of record number, e.g. range=1000,2000")

parser.add_argument('--fea', dest='fea_data', action='store_true',
                    default=False, help = "feature data tag")

parser.add_argument('--sampling', dest='sampling',
                    default="4e3", help = "set sampling rate (Hz)")

parser.add_argument('--bias', dest='bias',
                    default="0.0", help = "DC shift/ acceleration offset (mG), for 'velocity' use")

parser.add_argument('--IV', dest='IV',
                    default="0.0", help = "Initial velocity (m/s), for 'velocity' use")

parser.add_argument('--threshold', dest='threshold',
                    default="0.0", help = "acceleration threshold (mG), for 'velocity' use")

# fetch the arguments
args = parser.parse_args(argv)



VOpt = Opt(args)

# Data IO
from DataIO import DataImport
Array = DataImport(VOpt)

# Plotting
from plot import Plot    

plot = Plot(VisualOpt = VOpt, Array = Array)




