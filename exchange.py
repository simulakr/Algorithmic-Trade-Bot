import os
import pandas as pd
import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import List, Optional, Dict
import logging

# Log ayarı
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

class MEXCFuturesAPI:
    def __init__(self, testnet: bool = False):
        """MEXC Futures API bağlantısını başlatır."""
        self.api_key = os.getenv('MEXC_API_KEY')
        self.api_secret = os.getenv('MEXC_API_SECRET')
        
        # MEXC Contract API base URL
        self.base_url = 'https://contract.mexc.com'
            
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'ApiKey': self.api_key
        })
        
        logger.info("MEXC Futures API bağlantısı başlatıldı")

    def _generate_signature(self, params: Dict) -> str:
        """API signature oluşturur"""
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _make_request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False) -> Dict:
        """API isteği yapar"""
        if params is None:
            params = {}
            
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
            
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=params)
            else:
                raise ValueError(f"Desteklenmeyen HTTP metodu: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error("API isteği hatası: %s", str(e))
            raise

    def get_ohlcv(
        self,
        symbol: str = 'SOL_USDT',
        interval: str = 'Min15',
        limit: int = 300,
        convert_to_float: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        MEXC Futures'tan OHLCV verisi çeker.
        
        Args:
            symbol: Trading çifti (örn: SOL_USDT, BTC_USDT)
            interval: Zaman dilimi (Min1, Min5, Min15, Min30, Min60, Hour4, Hour8, Day1)
            limit: Maksimum kayıt sayısı
            convert_to_float: Sayısal değerleri float'a çevir
        
        Returns:
            OHLCV verilerini içeren DataFrame
        """
        try:
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            
            response = self._make_request('GET', '/api/v1/contract/kline', params)
            
            if response.get('code') != 200:
                raise Exception(f"API Hatası: {response.get('msg', 'Bilinmeyen hata')}")
                
            klines = response.get('data', [])
            
            if not klines:
                logger.warning("Veri bulunamadı - Symbol: %s", symbol)
                return None
            
            # MEXC kline formatı: [timestamp, open, high, low, close, volume]
            df = pd.DataFrame(klines, columns=[
                'time', 'open', 'high', 'low', 'close', 'volume'
            ])
            
            # Timestamp'i datetime'a çevir (saniye cinsinden)
            df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')
            
            if convert_to_float:
                df[['open', 'high', 'low', 'close', 'volume']] = df[
                    ['open', 'high', 'low', 'close', 'volume']
                ].astype(float)
                
            # Index olarak time kullan
            df.set_index('time', inplace=True)
            
            # Kronolojik sırala (eskiden yeniye)
            df = df.sort_index()
            
            logger.info("Veri başarıyla çekildi - Symbol: %s, Rows: %d", symbol, len(df))
            return df
            
        except Exception as e:
            logger.error("Veri çekme hatası - Symbol: %s, Error: %s", symbol, str(e))
            return None

    def get_multiple_ohlcv(
        self,
        symbols: List[str],
        interval: str = 'Min15',
        limit: int = 300
    ) -> Dict[str, pd.DataFrame]:
        """
        Birden fazla sembol için OHLCV verisi çeker
        
        Args:
            symbols: Sembol listesi
            interval: Zaman dilimi
            limit: Kayıt sayısı
            
        Returns:
            Sembol-DataFrame sözlüğü
        """
        results = {}
        
        for symbol in symbols:
            logger.info("Veri çekiliyor: %s", symbol)
            df = self.get_ohlcv(symbol, interval, limit)
            
            if df is not None and not df.empty:
                results[symbol] = df
            else:
                logger.warning("Veri çekilemedi: %s", symbol)
                
        logger.info("Toplam %d sembol için veri çekildi", len(results))
        return results

    def get_ticker_price(self, symbol: str) -> Optional[float]:
        """
        Güncel fiyat bilgisini çeker
        
        Args:
            symbol: Trading çifti
            
        Returns:
            Güncel fiyat
        """
        try:
            params = {'symbol': symbol}
            response = self._make_request('GET', '/api/v1/contract/ticker', params)
            
            if response.get('code') != 200:
                raise Exception(f"API Hatası: {response.get('msg', 'Bilinmeyen hata')}")
                
            data = response.get('data', {})
            price = float(data.get('lastPrice', 0))
            
            logger.info("Güncel fiyat - %s: %f", symbol, price)
            return price
            
        except Exception as e:
            logger.error("Fiyat çekme hatası - Symbol: %s, Error: %s", symbol, str(e))
            return None

    def get_symbol_info(self, symbol: str = None) -> Dict:
        """
        Sembol bilgilerini çeker
        
        Args:
            symbol: Spesifik sembol (None ise tüm semboller)
            
        Returns:
            Sembol bilgileri
        """
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
                
            response = self._make_request('GET', '/api/v1/contract/detail', params)
            
            if response.get('code') != 200:
                raise Exception(f"API Hatası: {response.get('msg', 'Bilinmeyen hata')}")
                
            return response.get('data', {})
            
        except Exception as e:
            logger.error("Sembol bilgisi hatası: %s", str(e))
            return {}
