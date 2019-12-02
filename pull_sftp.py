#!/usr/bin/env python3

# prerequisite:
# pip3 install pysftp

# USAGE:
# 1. Change 'start_dt' to the starting date-time you want to get the CSV entries
#
# 2. Edit the parameter file 'sftp_par.py', in which
#   host        = "xxx.xxx.xxx.xxx"
#   user        = "USER_NAME"
#   password    = "PASSWORD
#
# 3. execute './pull_sftp.py'

import datetime
import pysftp
import sftp_par as sp


start_dt = datetime.datetime(2019, 12, 2, 19, 30)


cnopts = pysftp.CnOpts()
cnopts.hostkeys = None 

try:
    srv = pysftp.Connection( 
        host        = sp.host, 
        username    = sp.user,
        password    = sp.password, 
        cnopts      = cnopts,
        log         = "./pysftp.log"
        )
except ConnectionException:
    exit(1)

with srv.cd(sp.directory):
    dir_list = srv.listdir()
    for filename in dir_list:
        if filename[0:3] == 'fea':
            date_str = [ filename[4:8],
                        filename[8:10],
                        filename[10:12],
                        filename[13:15],
                        filename[15:17],
                        filename[17:19] ]
            dt = datetime.datetime  ( int(date_str[0]), 
                                int(date_str[1]), 
                                int(date_str[2]),
                                int(date_str[3]),
                                int(date_str[4]),
                                int(date_str[5])
                                )
            if  dt > start_dt:
                srv.get(filename)
                print('get file from server:', filename)

srv.close()
