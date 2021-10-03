#  loctest.py - Test LOC functions through the Python console
#
#  Copyright (c) 2017-2019 Mark Brooker (mark@walkjivefly.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
from __future__ import print_function
import sys
import os
import inspect
import getopt
#Add path to LO/OO components.
#sys.path.append('/opt/libreoffice5.3/program')

# Add current directory to path to import loc module
cmd_folder = os.path.realpath(os.path.abspath
                              (os.path.split(inspect.getfile
                                             ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)  
import loc

def main(argv):
    main_loc = loc.LocImpl(argv)
    arg_funct = ''
    arg_exchange = ''
    arg_ticker = ''
    arg_datacode = ''
    try:
        opts, args = getopt.getopt(argv, 'f:e:t:d:',
                                         ['function=','exchange=','ticker=','datacode='])
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-f', '--function'):
            arg_funct = arg
        elif opt in ('-e', '--exchange'):
            arg_exchange = arg
        elif opt in ('-t', '--ticker'):
            arg_ticker = arg
        elif opt in ('-d', '--datacode'):
            arg_datacode = arg
    print ('Function tested is', arg_funct)
    if arg_funct == 'ccxt':
        print ('Exchange used is', arg_exchange)
    print ('Ticker used is', arg_ticker)
    print ('Datacode used is', arg_datacode)

    if arg_funct == 'poloniex':
        loc_test(main_loc, arg_ticker, arg_datacode)
    elif arg_funct == 'ccxt':
        loc_test2(main_loc, arg_exchange, arg_ticker, arg_datacode)
    elif arg_funct == 'cb':
        loc_test3(main_loc, arg_ticker, arg_datacode)
    elif arg_funct == 'merge':
        loc_test4(main_loc, arg_ticker, arg_datacode)
    else:
        usage(0)

def loc_test(loc_py, ticker, datacode):
    result = loc_py.getPoloniex(ticker, datacode)
    print (result)
    sys.exit()
    
def loc_test2(loc_py, exchange, ticker, datacode):
    result = loc_py.ccxt(exchange, ticker, datacode)
    print (result)
    sys.exit()
    
def loc_test3(loc_py, ticker, datacode):
    result = loc_py.getCryptoBridge(ticker, datacode)
    print (result)
    sys.exit()
    
def loc_test4(loc_py, ticker, datacode):
    result = loc_py.getBirake(ticker, datacode)
    print (result)
    sys.exit()
    
def usage(err):
    print ('Usage: loctest.py -f poloniex -t <ticker> -d <datacode>')
    print ('       -- or --')
    print ('       loctest.py -f ccxt -e <exchange> -t <ticker> -d <datacode>')
    print ('')
    print ('        ticker is the crypto currency you want data for,')
    print ('        datacode is the data you require, most likely "last"')
    print ('        exchange is the exchange to query when using the ccxt library')
    sys.exit(err)
        
if __name__ == '__main__':
    main(sys.argv[1:])
