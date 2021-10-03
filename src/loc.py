#  loc.py - Pyuno/LO bridge to implement new functions for LibreOffice calc
#
#  Copyright (c) 2017-2021 Mark Brooker (mark@walkjivefly.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#

import unohelper
from com.loc.crypto.getinfo import LOC
from urllib.request import urlopen, Request
#from .api_key_secret_util import get_api_key, get_api_secret
import json
import ssl
import sys
import os
import inspect
import logging
import ccxt as ikccxt

# Create Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Create file handler and set level to debug
logfile = '/tmp/LOC_' + str(os.getpid())
fh = logging.FileHandler(logfile, mode='a', encoding=None, delay=False)
fh.setLevel(logging.INFO)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Add formatter to handlers
fh.setFormatter(formatter)
# Add handlers to logger
logger.addHandler(fh)

class SouthXchange():
    def __init__(self):
        pass
    def api_query(self, command, ticker):
        if(command == 'returnTicker'):
            ret = urlopen(Request('https://www.southxchange.com/api/v4/price/' + ticker))
            return json.loads(ret.read().decode('utf8'))
        else:
            return 'Unknown request'
    def returnTicker(self, ticker):
        return self.api_query('returnTicker', ticker)


class Poloniex():
    def __init__(self):
        pass
 
    def api_query(self, command, req={}):
        if(command == 'returnTicker' or command == 'return24Volume'):
            ret = urlopen(Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read().decode('utf8'))
        elif(command == 'returnOrderBook'):
            ret = urlopen(Request('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif(command == 'returnMarketTradeHistory'):
            ret = urlopen(Request('https://poloniex.com/public?command=' + 'returnTradeHistory' + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        else:
            return 'Unknown request'

    def returnTicker(self):
        return self.api_query('returnTicker')

    def return24Volume(self):
        return self.api_query('return24Volume')

    def returnOrderBook (self, currencyPair):
        return self.api_query('returnOrderBook', {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair):
        return self.api_query('returnMarketTradeHistory', {'currencyPair': currencyPair})


class LocImpl(unohelper.Base, LOC):
    """Define the main class for the LOC extension """    
    def __init__( self, ctx ):
        self.ctx = ctx
        logger.info('========== New call ==========')
        # this is a nasty hack for an OpenSSL problem, the details of which I don't begin to understand.
        ssl._create_default_https_context = ssl._create_unverified_context
        exchanges = {}
        for id in ikccxt.exchanges:
            exchange = getattr(ikccxt, id)
            exchanges[id] = exchange()

    def runCommand( self, command ):
        """Run a command"""
        logger.info('runCommand attempting ' + command)
        try:
            result = os.popen(command).read().rstrip()
            logger.info('result=' + result)
        except:
            logger.error('runCommand: exception {}'.format(sys.exc_info()[0]))
            result = 'Exception encountered'
        return result


    def xrs( self, command, parms ):
        """Call XRouter service"""
        logger.info('xrs attempting ' + command + " " + parms)
        try:
            result = json.load(os.popen("blocknet-cli " + command + " " + parms))['reply']
            logger.info('result=' + str(result))
        except:
            logger.error('runCommand: exception {}'.format(sys.exc_info()[0]))
            logger.error('runCommand: exception {}'.format(sys.exc_info()[1]))
            logger.error('runCommand: exception {}'.format(sys.exc_info()[2]))
            result = 'Exception encountered'
        return result


    def xcs( self, command, parms ):
        """Call XCloud service"""
        logger.info('xcs attempting ' + command + " " + parms)
        try:
            result = json.load(os.popen("blocknet-cli xrservice " + command + " " + parms))['reply']
            logger.info('result=' + str(result))
        except:
            logger.error('runCommand: exception {}'.format(sys.exc_info()[0]))
            logger.error('runCommand: exception {}'.format(sys.exc_info()[1]))
            logger.error('runCommand: exception {}'.format(sys.exc_info()[2]))
            result = 'Exception encountered'
        return result


    def getSouthXchange( self, ticker, datacode='last' ):
        """Return SouthXchange data. Mapped to PyUNO through the LOC.rdb file"""
        ticker = ticker.upper()
        datacode = datacode.capitalize()
        logger.info('getSouthXchange: ticker={} datacode={}'.format(ticker, datacode))
        try:
            CB = SouthXchange()
            result = float(CB.returnTicker(ticker)[datacode])
            logger.info('getSouthXchange: result={:.8f}'.format(result))
        except:
            result = 'Something bad happened'
        return result

    def getPoloniex( self, ticker, datacode='last' ):
        """Return Poloniex data. Mapped to PyUNO through the LOC.rdb file"""
        ticker = ticker.upper()
        #datacode = datacode.lower()
        logger.info('getPoloniex: ticker={} datacode={}'.format(ticker, datacode))
        try:
            polo = Poloniex()
            result = float(polo.returnTicker()[ticker][datacode])
            logger.info('getPoloniex: result={:.8f}'.format(result))
        except:
            result = 'Something bad happened'
        return result

    def ccxt( self, exchng, ticker, datacode='last' ):
        """Let ccxt do the work"""
        exchng = exchng.lower()
        ticker = ticker.upper()
        datacode = datacode.lower()
        result = ''
        logger.info('ccxt: exchange={} ticker={} datacode={}'.format(exchng, ticker, datacode))
        try:
            # no caching for starters
            if exchng in ikccxt.exchanges: 
                xchng = getattr(ikccxt, exchng)
                actual_exchange = xchng()
                #if actual_exchange.has['publicAPI'] == false:
                if exchng == 'bibox':
                   actual_exchange.has['fetchCurrencies'] = False
                markets = actual_exchange.load_markets()
                if ticker in actual_exchange.symbols:
                    result = actual_exchange.fetch_ticker(ticker)[datacode]
                    logger.info('ccxt: {} {} {}={:.8f}'.format(exchng, ticker, datacode, result))
                else:
                    result = 'Unknown ' + exchng + ' pair: ' + ticker
                    logger.error('ccxt: {}'.format(result))
                # end of uncached exchanges
            # end of supported exchanges
            else:
                result = 'Unsupported exchange: ' + exchng
                logger.error('ccxt: {}'.format(result))
        except:
            logger.error('ccxt: exception {}'.format(sys.exc_info()[0]))
            result = 'Exception encountered'
        return result

def createInstance( ctx ):
    return LocImpl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,'com.loc.crypto.getinfo.python.LocImpl',
        ('com.sun.star.sheet.AddIn',),)
