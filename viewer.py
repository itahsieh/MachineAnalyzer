#!/usr/bin/env python3
import argparse
import sys

# usage
def usage():
        print ('''
viewer  -i < Input File >
        
        --show      : show the plot in GUI window, 
                      otherwise save the image file (png format) 
        
        --spec      : spectrum plot
        
        --series    : time series and histogram plot
        
        --waterfall : waterfall plot. 
                      (magnitude distribution of frequency and time)
                      The flag must be in '--spec' mode
        
        --contour   : contour plot 
                      (magnitude distribution of frequency and time)
                      The flag must be in '--spec' mode
''')


import sys
argv = sys.argv[1:]

if not argv:
        usage()
        sys.exit(2)


# parser
parser = argparse.ArgumentParser(prog='viewer', description = 'Vibrational data viewer')
parser.add_argument("-i", "--input", help="input data path", dest="data", default="default")
parser.add_argument('--series', dest='series_view', action='store_true',
                    default=False, help = "series data viewer")

parser.add_argument('--show', dest='show_gui', action='store_true',
                    default=False, help = "enable GUI window")

parser.add_argument('--spec', dest='spec_view', action='store_true',
                    default=False, help = "spectrum viewer")

parser.add_argument('--waterfall', dest='waterfall_plot', action='store_true',
                    default=False, help = "waterfall plot viewer")

parser.add_argument('--contour', dest='contour_plot', action='store_true',
                    default=False, help = "contour plot viewer")



# fetch the arguments
args = parser.parse_args(argv)


# Data IO
splitted_path = args.data.rsplit('/',1) 
DataDir = splitted_path[0]+'/'
filename = splitted_path[1]

from DataIO import DataImport
DataType, Array = DataImport(DataDir, filename)

# Plotting
from plot import VisualOpt, PlotClass
VOpt = VisualOpt(args)
plot = PlotClass(VisualOpt = VOpt, 
                 DataType = DataType, 
                 DataName = filename.split('.')[0],
                 Array = Array
                 )




