#!/usr/bin/env python3
import argparse
import sys


parser = argparse.ArgumentParser(description = 'Specrum viewer')
parser.add_argument('data', help = "path of the binary data")
parser.add_argument('--waterfall', dest='waterfall_plot', action='store_true',
                    default=False, help = "enable waterfall plot")
parser.add_argument('--show', dest='show_gui', action='store_true',
                    default=False, help = "enable GUI window")
args = parser.parse_args(sys.argv[1:])

splitted_path = args.data.rsplit('/',1) 
DataDir = splitted_path[0]+'/'
filename = splitted_path[1]


if args.watefall_plot:
    

from analyzer import Analyzer
Analyzer( DataDir, filename)
