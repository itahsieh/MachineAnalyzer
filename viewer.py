#!/usr/bin/env python3
import argparse
import sys


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



args = parser.parse_args(sys.argv[1:])

splitted_path = args.data.rsplit('/',1) 
DataDir = splitted_path[0]+'/'
filename = splitted_path[1]

print(args) 

exit(0)

#if args.watefall_plot:
    #pass

from analyzer import Analyzer   
Analyzer( DataDir, filename)
