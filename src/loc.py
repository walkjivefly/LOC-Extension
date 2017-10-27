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
import sys
import os
import inspect
import logging

# Add current directory to path to import ccxt modules
cmd_folder = os.path.realpath(os.path.abspath
                              (os.path.split(inspect.getfile
                                             ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from exchange import *  # noqa: F403
from exchanges import * # noqa: F403

# Create Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
# Create file handler and set level to debug
logfile = "/tmp/LOC_" + str(os.getpid())
fh = logging.FileHandler(logfile, mode='a', encoding=None, delay=False)
fh.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Add formatter to handlers
#ch.setFormatter(formatter)
fh.setFormatter(formatter)
# Add handlers to logger
#logger.addHandler(ch)
logger.addHandler(fh)


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
        logger.info('========== New call ==========')
        # this is a nasty hack for an OpenSSL problem, the details of which I don't begin to understand.
        ssl._create_default_https_context = ssl._create_unverified_context

    def getPoloniex( self, ticker, datacode='last' ):
        """Return Poloniex data. Mapped to PyUNO through the Xloc2.rdb file"""
        ticker = ticker.upper()
        datacode = datacode.lower()
        logger.info('getPoloniex ticker={} datacode={}'.format(ticker, datacode))
        try:
            polo = Poloniex()
            result = float(polo.returnTicker()[ticker][datacode])
            logger.info('getPoloniex result={:.8f}'.format(result))
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
            if exchng in exchanges:
                if exchng == '_1broker':
                    xchng = _1broker()
                elif exchng == '_1btcxe':
                    xchng = _1btcxe()
                elif exchng == 'acx':
                    xchng = acx()
                elif exchng == 'allcoin':
                    xchng = allcoin()
                elif exchng == 'anxpro':
                    xchng = anxpro()
                elif exchng == 'binance':
                    xchng = binance()
                elif exchng == 'bit2c':
                    xchng = bit2c()
                elif exchng == 'bitbay':
                    xchng = bitbay()
                elif exchng == 'bitcoincoid':
                    xchng = bitcoincoid()
                elif exchng == 'bitfinex':
                    xchng = bitfinex()
                elif exchng == 'bitfinex2':
                    xchng = bitfinex2()
                elif exchng == 'bitflyer':
                    xchng = bitflyer()
                elif exchng == 'bithumb':
                    xchng = bithumb()
                elif exchng == 'bitlish':
                    xchng = bitlish()
                elif exchng == 'bitmarket':
                    xchng = bitmarket()
                elif exchng == 'bitmex':
                    xchng = bitmex()
                elif exchng == 'bitso':
                    xchng = bitso()
                elif exchng == 'bitstamp1':
                    xchng = bitstamp1()
                elif exchng == 'bitstamp':
                    xchng = bitstamp()
                elif exchng == 'bittrex':
                    xchng = bittrex()
                elif exchng == 'bl3p':
                    xchng = bl3p()
                elif exchng == 'bleutrade':
                    xchng = bleutrade()
                elif exchng == 'btcbox':
                    xchng = btcbox()
                elif exchng == 'btcchina':
                    xchng = btcchina()
                elif exchng == 'btcexchange':
                    xchng = btcexchange()
                elif exchng == 'btcmarkets':
                    xchng = btcmarkets()
                elif exchng == 'btctradeua':
                    xchng = btctradeua()
                elif exchng == 'btcturk':
                    xchng = btcturk()
                elif exchng == 'btcx':
                    xchng = btcx()
                elif exchng == 'bter':
                    xchng = bter()
                elif exchng == 'bxinth':
                    xchng = bxinth()
                elif exchng == 'ccex':
                    xchng = ccex()
                elif exchng == 'cex':
                    xchng = cex()
                elif exchng == 'chbtc':
                    xchng = chbtc()
                elif exchng == 'chilebit':
                    xchng = chilebit()
                elif exchng == 'coincheck':
                    xchng = coincheck()
                elif exchng == 'coinfloor':
                    xchng = coinfloor()
                elif exchng == 'coingi':
                    xchng = coinigi()
                elif exchng == 'coinmarketcap':
                    xchng = coinmarketcap()
                elif exchng == 'coinmate':
                    xchng = coinmate()
                elif exchng == 'coinsecure':
                    xchng = coinsecure()
                elif exchng == 'coinspot':
                    xchng = coinspot()
                elif exchng == 'cryptopia':
                    xchng = cryptopia()
                elif exchng == 'dsx':
                    xchng = dsx()
                elif exchng == 'exmo':
                    xchng = exmo()
                elif exchng == 'flowbtc':
                    xchng = flowbtc()
                elif exchng == 'foxbit':
                    xchng = foxbit()
                elif exchng == 'fybse':
                    xchng = fybse()
                elif exchng == 'fybsg':
                    xchng = fybsg()
                elif exchng == 'gatecoin':
                    xchng = gatecoin()
                elif exchng == 'gateio':
                    xchng = gateio()
                elif exchng == 'gdax':
                    xchng = gdax()
                elif exchng == 'gemini':
                    xchng = gemini()
                elif exchng == 'hitbtc':
                    xchng = hitbtc()
                elif exchng == 'hitbtc2':
                    xchng = hitbtc2()
                elif exchng == 'huobi':
                    xchng = huobi()
                elif exchng == 'huobicny':
                    xchng = huobicny()
                elif exchng == 'huobipro':
                    xchng = huobipro()
                elif exchng == 'independentreserve':
                    xchng = independentreserve()
                elif exchng == 'itbit':
                    xchng = itbit()
                elif exchng == 'jubi':
                    xchng = jubi()
                elif exchng == 'kraken':
                    xchng = kraken()
                elif exchng == 'kuna':
                    xchng = kuna()
                elif exchng == 'lakebtc':
                    xchng = lakebtc()
                elif exchng == 'livecoin':
                    xchng = livecoin()
                elif exchng == 'liqui':
                    xchng = liqui()
                elif exchng == 'luno':
                    xchng = luno()
                elif exchng == 'mercado':
                    xchng = mercado()
                elif exchng == 'mixcoins':
                    xchng = mixcoins()
                elif exchng == 'nova':
                    xchng = nova()
                elif exchng == 'okcoincny':
                    xchng = okcoincny()
                elif exchng == 'okcoinusd':
                    xchng = okcoinusd()
                elif exchng == 'okex':
                    xchng = okex()
                elif exchng == 'paymium':
                    xchng = paymium()
                elif exchng == 'poloniex':
                    xchng = poloniex()
                elif exchng == 'quadrigacx':
                    xchng = quadrigacx()
                elif exchng == 'qryptos':
                    xchng = qryptos()
                elif exchng == 'quoine':
                    xchng = quoine()
                elif exchng == 'southxchange':
                    xchng = southexchange()
                elif exchng == 'surbitcoin':
                    xchng = surbitcoin()
                elif exchng == 'tidex':
                    xchng = tidex()
                elif exchng == 'therock':
                    xchng = therock()
                elif exchng == 'urdubit':
                    xchng = urdubit()
                elif exchng == 'vaultoro':
                    xchng = vaultpro()
                elif exchng == 'vbtc':
                    xchng = vbtc()
                elif exchng == 'virwox':
                    xchng = virwox()
                elif exchng == 'wex':
                    xchng = wex()
                elif exchng == 'xbtce':
                    xchng = xbtce()
                elif exchng == 'yobit':
                    xchng = yobit()
                elif exchng == 'yunbi':
                    xchng = yunbi()
                elif exchng == 'zaif':
                    xchng = zaif()
                markets = xchng.load_markets()
                if ticker in ('CACHE', 'RELOAD'):
                    xchng.fetch_tickers()
                    result = "Fetched all tickers for " + exchng
                    logger.info('ccxt: {}'.format(result))
                elif ticker in xchng.symbols: 
                    result = float(xchng.fetch_ticker(ticker)[datacode])
                    logger.info('ccxt {} {} {}={:.8f}'.format(exchng, ticker, datacode, result))
                else:
                    result = "Unknown " + exchng + " pair: " + ticker
                    logger.error('ccxt: {}'.format(result))
            else:
                result = "Unsupported exchange: " + exchng
                logger.error('ccxt: {}'.format(result))
        except:
            logging.error('ccxt: exception {}'.format(sys.exc_info()[0]))
            result = "Exception encountered"
        return result

def createInstance( ctx ):
    return Loc2Impl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,"com.loc.crypto.getinfo2.python.Loc2Impl",
        ("com.sun.star.sheet.AddIn",),)
