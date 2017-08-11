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

import os
import sys
import inspect
#Try/except is for LibreOffice Python3.x vs. OpenOffice Python2.x.
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError
from codecs import iterdecode
import unohelper
from com.loc.crypto.getinfo import XLoc
# Add current directory to path to import poloniex module
cmd_folder = os.path.realpath(os.path.abspath
                              (os.path.split(inspect.getfile
                                             ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from poloniex import Poloniex

class LocImpl(unohelper.Base, XLoc ):
    """Define the main class for the LOC extension """    
    def __init__( self, ctx ):
        self.ctx = ctx

    def getPoloniex( self, ticker, datacode='last' ):
        """Return Poloniex data. Mapped to PyUNO through the Xloc.rdb file"""
        try:
            polo = Poloniex()
            result = polo.returnTicker()[ticker][datacode]
        except:
            result = 'Something bad happened'
        return result

    
def createInstance( ctx ):
    return LocImpl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,"com.loc.crypto.getinfo.python.LocImpl",
        ("com.sun.star.sheet.AddIn",),)
