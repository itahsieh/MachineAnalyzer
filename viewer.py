#!/usr/bin/env python3
import argparse
import sys


parser = argparse.ArgumentParser(description = 'Vibrational data viewer')
parser.add_argument('data', help = "path of the binary data")

spec_parser = argparse.ArgumentParser(description = 'Spectrum plot', parents=[parser])
spec_parser.add_argument('--spec', dest='spec_view', action='store_true',
                    default=False, help = "spectrum viewer")

wf_parser = parser.add_subparsers(dest='type')
wf_parser.add_argument('--waterfall', dest='waterfall_plot', action='store_true', parent=parser['--spec'],
                    default=False, help = "enable waterfall plot")


parser.add_argument('--series', dest='series_view', action='store_true',
                    default=False, help = "series data viewer")





parser.add_argument('--show', dest='show_gui', action='store_true',
                    default=False, help = "enable GUI window")
args = parser.parse_args(sys.argv[1:])

splitted_path = args.data.rsplit('/',1) 
DataDir = splitted_path[0]+'/'
filename = splitted_path[1]

print(args)
print(parser.parse_args())
exit(0)

if args.watefall_plot:
    pass

from analyzer import Analyzer
Analyzer( DataDir, filename)
