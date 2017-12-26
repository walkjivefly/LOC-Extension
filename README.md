LOC-Extension: LibreOffice calc Cryptocurrency market functions
===
The LOC extension allows you to create customized spreadsheets with cryptocurrency market data directly from the web. This version (0.2.3) provides 2 lookup functions: a dedicated getPoloniex() (for compatibility with version 0.1.0) and a generic ccxt() which uses an embedded snapshot of the amazing [ccxt](https://github.com/ccxt/ccxt) library. This means over 90 exchanges are now supported.

### Download   
You can download the current version of the LOC Extension here [0.2.3](https://github.com/walkjivefly/LOC-Extension/releases/tag/v0.2.3)

The LOC extension is also available from the [LibreOffice Extension Center](https://extensions.libreoffice.org/extensions/loc-extension-for-libreoffice-calc).

**NOTE**: The extension itself is LOC.oxt.  The example .ods worksheet demonstrates how to use the extension.

### Usage

The LOC Extension adds two new functions to Calc. The first is:  
```
GETPOLONIEX(Ticker,Datacode) 
```  

Quotes **must** be used when entering the ticker directly ex: ```GETPOLONIEX("BTC_ETH","last")```, but are **not** needed when referencing another cell ex: ```GETPOLONIEX(A1,A2)```.

In the latter case the data in A1 should be ```BTC_ETH```, not ```"BTC_ETH"```.

**NOTE**: The full set of datacodes are demonstrated in the example .ods worksheet included with the release. The worksheet also contains a full list of the available symbols/currency-pairs.

The second new function is:
```
CCXT(Exchange, Ticker, Datacode)
```

Exchange is any exchange name supported by the embedded ccxt snapshot (version 1.9.262). Quotes **must** be used according to the same rules as for GETPOLONIEX().

Ticker is a currency pair from the ccxt unified API.
**NOTE**: The format of the ticker is different from that for GETPOLONIEX(). The valid values depend on the exchange being addressed.

Datacode is one of the ccxt supported data items for the fetch_ticker function. The one you'll probably use most is "last" 

v0.2.3 introduces caching for some of the ccxt supported exchanges. This relies on the ccxt load_markets() function downloading data for every ticker combination supported by the exchange. The cached information is then used for every subsequent lookup for that exchange. If you're pulling the prices for many tickers and you have a slow internet connection this provides a very substantial, very worthwhile, performance improvementi after the first fetch. 

The exchanges which provide caching are bitmex, gatecoin, lakebtc, livecoin, luno, nova, poloniex, qryptos, quoine, therock and vaultoro.

#### Coinmarketcap

Coinmarketcap is supported by ccxt but it is not a regular exchange; it is an aggregator. It works slightly differently to a regular exchange. It doesn't provide coin/coin tickers. Instead, it provides coin/fiat tickers for 15 supported fiat currencies (AUD, BRL, CAD, CHF, CNY, EUR, GBP, HKD, IDR, INR, JPY, KRW, MXN, RUB, and USD). In addition it provides some special data like total market cap in USD and bitcoin percentage dominance. These are accessed using a special ticker, "GLOBAL" and datacode items "market_cap" and "dominance". Further, there are 2 special data items for each coin: market cap in USD, and rank. These are accessed from the coin/USD ticker with datacodes "market_cap" and "rank".

### Windows users

At the present time v0.2.2 is the only version recommended for Windows users. This is because some have experienced problems installing v0.2.0. LOC-Extension includes some logging which worked on the test Windows (7) machine I had access to but which is incompatible with (at least some) other machines. I do not currently have access to a Windows (any version) machine for testing.

Windows users are **STRONGLY** recommended to make a system snapshot before installing this or any other LibreOffice extension. Then when it goes horribly wrong you'll have a much simpler time recovering.
 
### Upgrading

The LibreOffice extension mechanism is poorly documented and extremely fragile. It is **STRONGLY** recommended that you remove the previous version of LOC-Extension before adding this one. If you use the replace option you might or might not end up with indecipherable error messages or an unusable extension. If you really screw things up I recommend closing LibreOffice, renaming the entire customisation directory (~/.config/libreoffice/4 on linux), restarting LibreOffice and re-installing (all) your extensions. 

Recovering from a messed-up extension installation/upgrade is much harder for Windows users. Really, make a system snapshot before installing or upgrading any LibreOffice extension. 

### Dependencies

LOC-Extension is fully standalone. It includes an embedded snapshot of Igor Kroitor's [ccxt](http://github.com/ccxt/ccxt). 

### Support

For general support please visit the [forums](http://forum.openoffice.org/en/forum/index.php). If you find a bug or wish to request a feature please file an issue at the [issue tracker](http://github.com/walkjivefly/LOC-Extension/issues).

### Contribute

Help is always welcome with development.  If you would like to contribute you will need to fork the main repo, make your changes, and send a [pull request](http://github.com/walkjivefly/LOC-Extension/pulls) to have your changes moderated and merged back into the main repo. Details on that process can be found [here](https://help.github.com/articles/set-up-git/).  


### License

The LOC Extension is released under the [![][shield:LGPL3]][License:3.0] which in layman's terms means:  

* You are permitted to use, copy and redistribute the work "as-is".
* You may adapt, remix, transform and build upon the material, releasing any derivatives under your own name.
* You may use the material for commercial purposes as long as the derivative is licenced under the GPL.
* You must track changes you make in the source files.
* You must include or make available the source code with your release.

ccxt is released under the MIT license.

### Warranty

There is **NO** warranty of any kind. You use the software entirely at your own risk. I am not responsible if anything goes wrong.

### Other Contributors and Thanks!
* madsailor - provided the original SMF Extension that LOC is based on
* Igor Kroitor - actively maintains the [ccxt](https://github.com/ccxt/ccxt) library

[GIT:release]: http://github.com/walkjivefly/LOC-Extension/releases/latest
[License:3.0]: http://www.gnu.org/licenses/lgpl.html
[shield:LGPL3]: http://img.shields.io/badge/license-LGPL%20v.3-blue.svg
