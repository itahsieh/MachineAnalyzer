#!/usr/bin/env python3
import argparse
import sys


parser = argparse.ArgumentParser(description = 'Specrum viewer')
parser.add_argument('--path', help = "path of the binary data")
args = parser.parse_args(sys.argv[1:])

splitted_path = args.path.rsplit('/',1) 
DataDir = splitted_path[0]+'/'
filename = splitted_path[1]

from analyzer import Analyzer
Analyzer( DataDir, filename)
