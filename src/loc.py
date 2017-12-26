#  loc.py - Pyuno/LO bridge to implement new functions for LibreOffice calc
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
from com.loc.crypto.getinfo import LOC
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
# Create file handler and set level to debug
logfile = '/tmp/LOC_' + str(os.getpid())
fh = logging.FileHandler(logfile, mode='a', encoding=None, delay=False)
fh.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Add formatter to handlers
fh.setFormatter(formatter)
# Add handlers to logger
logger.addHandler(fh)

# ccxt function handles
handles = {}
for x in exchanges:
    handles[x] = None

# ccxt exchanges with caching
caching = ['bitmex', 'coinmarketcap', 'gatecoin', 'lakebtc', 'livecoin',
           'luno', 'nova', 'poloniex', 'qryptos', 'quoine', 'therock',
           'vaultoro']

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
                    if handles[exchng] == None:
                        xchng = bitmex()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
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
                    xchng = coingi()
                elif exchng == 'coinmarketcap':
                    if handles[exchng] == None:
                        xchng = coinmarketcap()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
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
                    if handles[exchng] == None:
                        xchng = gatecoin()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
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
                    if handles[exchng] == None:
                        xchng = lakebtc()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'livecoin':
                    if handles[exchng] == None:
                        xchng = livecoin()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'liqui':
                    xchng = liqui()
                elif exchng == 'luno':
                    if handles[exchng] == None:
                        xchng = luno()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'mercado':
                    xchng = mercado()
                elif exchng == 'mixcoins':
                    xchng = mixcoins()
                elif exchng == 'nova':
                    if handles[exchng] == None:
                        xchng = nova()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'okcoincny':
                    xchng = okcoincny()
                elif exchng == 'okcoinusd':
                    xchng = okcoinusd()
                elif exchng == 'okex':
                    xchng = okex()
                elif exchng == 'paymium':
                    xchng = paymium()
                elif exchng == 'poloniex':
                    if handles[exchng] == None:
                        xchng = poloniex()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'quadrigacx':
                    xchng = quadrigacx()
                elif exchng == 'qryptos':
                    if handles[exchng] == None:
                        xchng = qryptos()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'quoine':
                    if handles[exchng] == None:
                        xchng = quoine()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'southxchange':
                    xchng = southxchange()
                elif exchng == 'surbitcoin':
                    xchng = surbitcoin()
                elif exchng == 'tidex':
                    xchng = tidex()
                elif exchng == 'therock':
                    if handles[exchng] == None:
                        xchng = therock()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
                elif exchng == 'urdubit':
                    xchng = urdubit()
                elif exchng == 'vaultoro':
                    if handles[exchng] == None:
                        xchng = vaultoro()
                        handles[exchng] = xchng
                    else:
                        xchng = handles[exchng]
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

                if exchng == 'coinmarketcap':
                    if ticker == 'RELOAD':
                        markets = xchng.load_markets(True)
                        result = 'Reloaded all tickers for ' + exchng
                        logger.info('ccxt: {}'.format(result))
                    elif ticker == 'GLOBAL':
                        g = xchng.fetch_global()
                        if datacode == 'market_cap':
                            result = float(g['total_market_cap_usd'])
                        elif datacode == 'dominance':
                            result = float(g['bitcoin_percentage_of_market_cap'])
                        else:
                            result = 'Request market_cap or dominance with GLOBAL'
                        logger.info('ccxt: {} GLOBAL {} = {}'.format(exchng, datacode, result))
                    else:
                        markets = xchng.markets
                        if markets == None:
                            markets = xchng.load_markets()
                        if ticker in xchng.symbols:
                            if datacode == 'rank':
                                result=markets[ticker]['info']['rank']
                                logger.info('ccxt: {} {} rank = {}'.format(exchng, ticker, result))
                            elif datacode == 'market_cap':
                                result=markets[ticker]['info']['market_cap_usd']
                                logger.info('ccxt: {} {} market_cap_usd = {}'.format(exchng, ticker, result))
                            else:
                                t = xchng.fetch_ticker(ticker)
                                result = float(t[datacode])
                                logger.info('ccxt: {} {} {} = {:.8f}'.format(exchng, ticker, datacode, result))
                        else:
                            result = 'Unknown ' + exchng + ' pair: ' + ticker
                            logger.info('ccxt: {}'.format(result))
                    # end of coinmarketcap
                elif exchng in caching:
                    markets = xchng.markets
                    if markets == None:
                        markets = xchng.load_markets()
                    if ticker == 'RELOAD':
                        markets = xchng.load_markets(True)
                        result = 'Reloaded all tickers for ' + exchng
                        logger.info('ccxt: {}'.format(result))
                    elif ticker == 'NOP':
                        result = 'Specify RELOAD to refresh cached data' 
                        logger.info('ccxt: {}'.format(result))
                    elif ticker in xchng.symbols:
                        result = float(markets[ticker]['info'][datacode])
                        logger.info('ccxt: {} {} {}={:.8f}'.format(exchng, ticker, datacode, result))
                    else:
                        result = 'Unknown ' + exchng + ' pair: ' + ticker
                        logger.info('ccxt: {}'.format(result))
                    # end of exchanges with cached results
                else:
                    # no caching here
                    markets = xchng.load_markets()
                    if ticker in xchng.symbols: 
                        result = xchng.fetch_ticker(ticker)[datacode]
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
