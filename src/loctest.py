#  loctest.py - Test LOC functions through the Python console
#
#  Copyright (c) 2017 Mark Brooker (mark@walkjivefly.com)
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
sys.path.append('/opt/libreoffice5.3/program')

# Add current directory to path to import loc module
cmd_folder = os.path.realpath(os.path.abspath
                              (os.path.split(inspect.getfile
                                             ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)  
import loc

def main(argv):
    main_loc = loc.Loc2Impl(argv)
    arg_funct = ''
    arg_ticker = ''
    arg_datacode = ''
    try:
        opts, args = getopt.getopt(argv, "f:t:d:",
                                         ["function=","ticker=","datacode="])
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-f", "--function"):
            arg_funct = arg
        elif opt in ("-t", "--ticker"):
            arg_ticker = arg
        elif opt in ("-d", "--datacode"):
            arg_datacode = arg
    print ("Function tested is", arg_funct)
    print ("Ticker used is", arg_ticker)
    print ("Datacode used is", arg_datacode)
    if arg_funct == "poloniex":
        poloniex_test(main_loc, arg_ticker, arg_datacode)
    elif arg_funct == "market":
        poloniex_test2(main_loc)
    elif arg_funct == "ccxt":
        poloniex_test3(main_loc, arg_ticker, arg_datacode, "dummy")
    else:
        usage(0)


def poloniex_test(loc_py, ticker, datacode):
    result = loc_py.getPoloniex(ticker, datacode)
    print (result)
    sys.exit()
    
def poloniex_test2(loc_py):
    result = loc_py.getMarket()
    print (result)
    sys.exit()
    
def poloniex_test3(loc_py, exchange, function, ticker):
    result = loc_py.passccxt(exchange, function, ticker)
    print (result)
    sys.exit()
    
        
def usage(err):
    print ("Usage: loctest.py -f <function> -t <ticker> -d <datacode>")
    print ("Available functions are poloniex|market|passccxt")
    print ("When the function is poloniex, ticker is the crypto currency")
    print ("you want data for, datacode is the data you require, one of:")
    print ("quoteVolume, lowestAsk, percentChange, last, low24hr, high24hr, " \
           " baseVolume, id, isFrozen")
    sys.exit(err)
        
if __name__ == "__main__":
    main(sys.argv[1:])
