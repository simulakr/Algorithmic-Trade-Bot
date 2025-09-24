import os
from dotenv import load_dotenv
load_dotenv()  # .env dosyasındaki API anahtarlarını yükle

# MEXC Futures API Ayarları
MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")

# MEXC Futures API Base URL
MEXC_BASE_URL = "https://contract.mexc.com"

# Sembol ve Zaman Aralığı Ayarları
SYMBOLS = ["SUI_USDT", "1000PEPE_USDT", "SOL_USDT"]  # MEXC Futures formatında
INTERVAL = "Min15"  # MEXC formatında (Min1, Min5, Min15, Min30, Hour1, Hour4, Day1)

# Sembol bazlı ATR aralıkları (MEXC sembol formatına göre güncellendi)
atr_ranges = {
    'SOL_USDT': (0.44, 0.84),
    '1000PEPE_USDT': (0.74, 1.3),
    'SUI_USDT': (0.61, 1.13)
}

# Quantity Hesabı İçin Ondalık Sayıları (MEXC sembol formatına göre)
ROUND_NUMBERS = {
    'BTC_USDT': 3,
    'ETH_USDT': 2,
    'BNB_USDT': 2,
    'SOL_USDT': 1,
    '1000PEPE_USDT': -2,
    'ARB_USDT': 1,
    'SUI_USDT': -1,
    'DOGE_USDT': 0,
    'XRP_USDT': 0,
    'OP_USDT': 1,
}

TP_ROUND_NUMBERS = {
    'BTC_USDT': 2,
    'ETH_USDT': 2,
    'BNB_USDT': 2,
    'SOL_USDT': 3,
    '1000PEPE_USDT': 7,
    'ARB_USDT': 4,
    'SUI_USDT': 5,
    'DOGE_USDT': 5,
    'XRP_USDT': 4,
    'OP_USDT': 4,
}

# Risk Yönetimi
RISK_PER_TRADE_USDT = 5.0  # Her işlemde sabit 5 USDT risk
LEVERAGE = 10  # MEXC'de maksimum kaldıraç sembol bazlı değişir (genelde 125x'e kadar)

# Trading Ayarları
POSITION_MODE = 2  # MEXC Futures: 1=OneWay (tek yönlü), 2=Hedge (hedge modu)

# MEXC Futures API için ek parametreler
ORDER_TYPE = {
    'MARKET': 1,    # Market order
    'LIMIT': 2,     # Limit order
    'POST_ONLY': 3, # Post only order
    'IOC': 4,       # Immediate or Cancel
    'FOK': 5        # Fill or Kill
}

SIDE = {
    'BUY': 1,       # Long pozisyon açma
    'SELL': 2       # Short pozisyon açma
}

OPEN_TYPE = {
    'ISOLATED': 1,  # İzole margin
    'CROSS': 2      # Cross margin
}

# Rate Limiting (MEXC API limitleri)
API_RATE_LIMIT = {
    'REQUESTS_PER_SECOND': 20,
    'REQUESTS_PER_MINUTE': 1200
}

# Websocket ayarları (MEXC Futures)
WEBSOCKET_BASE_URL = "wss://contract.mexc.com/ws"
