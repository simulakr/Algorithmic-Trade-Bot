from exchange import MEXCFuturesAPI

# API başlat
api = MEXCFuturesAPI()

# Tek sembol veri çek
df = api.get_ohlcv('SOL_USDT', 'Min15', 300)

# Çoklu sembol
symbols = ['SOL_USDT', 'BTC_USDT', 'ETH_USDT']
data = api.get_multiple_ohlcv(symbols, 'Min15', 300)

# Güncel fiyat
price = api.get_ticker_price('SOL_USDT')
