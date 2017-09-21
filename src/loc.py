#  loc.py - Pyuno/LO bridge to implement new functions for LibreOffice Calc
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

import unohelper
from com.loc.crypto.getinfo2 import XLoc2
from urllib.request import urlopen, Request
import json
import ssl


class Poloniex():
    def __init__(self):
        # this is a nasty hack for an OpenSSL problem, the details of which I don't begin to understand.
        ssl._create_default_https_context = ssl._create_unverified_context
 
    def api_query(self, command, req={}):
        if(command == "returnTicker" or command == "return24Volume"):
            ret = urlopen(Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read().decode('utf8'))
        elif(command == "returnOrderBook"):
            ret = urlopen(Request('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif(command == "returnMarketTradeHistory"):
            ret = urlopen(Request('https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        else:
            return 'Unknown request'

    def returnTicker(self):
        return self.api_query("returnTicker")

    def return24Volume(self):
        return self.api_query("return24Volume")

    def returnOrderBook (self, currencyPair):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})


class Loc2Impl(unohelper.Base, XLoc2):
    """Define the main class for the LOC extension """    
    def __init__( self, ctx ):
        self.ctx = ctx

    def cf1( self, ticker, datacode='last' ):
        """Return Poloniex data. Mapped to PyUNO through the Xloc2.rdb file"""
        try:
            polo = Poloniex()
            result = float(polo.returnTicker()[ticker][datacode])
        except:
            result = 'Something bad happened'
        return result

    def cf2( self ):
        """Return whole market snapshot. For starters return the whole lot as one string. Later we will programmatically chop it up and insert it into a new sheet as a side effect."""
        try:
            polo = Poloniex()
            tickers = polo.returnTicker()
            result = ''
            for t in tickers:
                result = result + t + ':' + tickers[t]['last'] + ' '
        except:
            result = "Couldn't load market data"
        return result

    def cf3( self, parm1, parm2, parm3 ):
        """Placeholder function as interface to ccxt"""
        try:
            result = "Let's pretend the ccxt call worked!"
        except:
            result = "Something bad happened in the call to ccxt"
        return result


def createInstance( ctx ):
    return Loc2Impl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,"com.loc.crypto.getinfo2.python.Loc2Impl",
        ("com.sun.star.sheet.AddIn",),)
