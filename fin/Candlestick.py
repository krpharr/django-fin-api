import yfinance as yf
import datetime
import pandas as pd

class Candlestick:
    def __init__(self, timestamp, open, high, low, close, volume):
        self.timestamp = timestamp
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.trend = 1
        self.bodytop = close
        self.bodybottom = open
        if close < open:
            self.trend = 0
            self.bodytop = open
            self.bodybottom = close
        self.bodysize = self.bodytop - self.bodybottom
        self.midpoint = self.bodytop - (self.bodysize / 2)
        self.wick = self.high - self.bodytop
        self.shadow = self.bodybottom - self.low
        self.height = self.high - self.low
        self.DOJIFACTOR = 0.08
        self.period_trend = 'undefined'

    def get_candles(self, ticker, num_days):
        current_date = datetime.date.today()
        end_date = current_date.strftime('%Y-%m-%d')
        start_date = current_date - datetime.timedelta(days=num_days)

        dat = yf.Ticker(ticker)
        stock = dat.history(start=start_date, 
                            end=end_date, 
                            progress=False)
        stock = stock.sort_index()  # Ensure data is sorted by date

        candlesticks = []
        for i in stock.index:
            c = Candlestick(i, round(stock['Open'][i], 2), round(stock['High'][i], 2), round(stock['Low'][i], 2), round(stock['Close'][i], 2), stock['Volume'][i])
            candlesticks.append(c)

        return candlesticks            

    def get_average_bodysize(self, candlesticks):
        s = 0
        for c in candlesticks:
            s = s + c.bodysize
        return s / len(candlesticks)
    
    def get_average_volume(self, candlesticks):
        s = 0
        for c in candlesticks:
            s = s + c.volume
        return s / len(candlesticks)
    
    def get_average_height(self, candlesticks):
        s = 0
        for c in candlesticks:
            s = s + c.height
        return s / len(candlesticks)
    
    def get_tallest_height(self, candlesticks):
        s = 0
        for c in candlesticks:
            if c.height > s:
                s = c.height
        return s 

    def get_average_close(self, candlesticks):
        s = 0
        for c in candlesticks:
            s = s + c.close
        return s / len(candlesticks)
    
    def get_highest_close(self, candlesticks):
        s = candlesticks[0].close
        for c in candlesticks:
            if c.close > s:
                s = c.close
        return s 
    
    def get_peaks(self, candlesticks):
        peaks = []
        for i in range(1, len(candlesticks)-1):
            a = candlesticks[i-1]
            b = candlesticks[i]
            c = candlesticks[i+1]
            if a.close < b.close and b.close > c.close:
                peaks.append(b)
        return peaks

    def get_bottoms(self, candlesticks):
        bottoms = []
        for i in range(1, len(candlesticks)-1):
            a = candlesticks[i-1]
            b = candlesticks[i]
            c = candlesticks[i+1]
            if a.close > b.close and b.close < c.close:
                bottoms.append(b)
        return bottoms
    
    def get_springs(self, candlesticks):
        springs = []
        bottoms = self.get_bottoms(candlesticks)
        for c in bottoms:
            if self.longShadow(c):
                springs.append(c)
        return springs

    
    def isIn(self, candle, candlesticks):
        for c in candlesticks:
            if candle == c:
                return True
        return False
    
    def insideRange(self, candle):
        # does this fit entirely inside of candle.range
        if self.high <= candle.high and self.low >= candle.low:
            return True
        return False
    
    def price_in_range(self, price, candle):
        if price <= candle.high and price >= candle.low:
            return True
        return False

    def price_in_body(self, price, candle):
        if price <= candle.bodytop and price >= candle.bodybottom:
            return True
        return False
    
    def within_range(self, num, reference, percentage):
        lower_bound = reference * (1 - percentage / 100)
        upper_bound = reference * (1 + percentage / 100)
        return lower_bound <= num <= upper_bound
     
    def is_small_body(self, average_body_size):
        if self.bodysize <= average_body_size:
            return True
        return False
    
    def is_large_body(self, average_body_size):
        if self.bodysize >= average_body_size:
            return True
        return False
    
    def isDoji(self, average_body_height):
        if self.open == self.close:
            return True
        if self.bodysize / average_body_height <= self.DOJIFACTOR:
            return True
        return False
    
    def gapsLower(self, candle):
        if self.open < candle.low:
            return True
        return False
    
    def bodyLower(self, candle):
        if self.bodytop < candle.bodybottom:
            return True
        return False
    
    def gapsHigher(self, candle):
        if self.open > candle.high:
            return True
        return False
    
    def bodyHigher(self, candle):
        if self.bodybottom > candle.bodytop:
            return True
        return False
    
    def noWick(self):
        if self.wick == 0.0:
            return True
        return False
                     
    def noShadow(self):
        if self.shadow <= self.height * 0.0346:
            return True
        return False
    
    def longWick(self):
        if self.wick >= self.height * 0.5:
            return True
        return False
                     
    def longShadow(self):
        if self.shadow >= self.height * 0.346:
            return True
        return False
    
    def isMarubozu(self):
        if self.trend == 0:
            if self.noWick() and self.noShadow():
                return True
            if self.noShadow() and self.wick > 0.0 and self.wick <= self.height * 0.0346:
                return True
            if self.noWick() and self.shadow > 0.0 and self.shadow <= self.height * 0.0346:
                return True

        if self.trend == 1:
            if self.noWick() and self.noShadow():
                return True
            if self.noShadow() and self.wick > 0.0 and self.wick <= self.height * 0.0346:
                return True
            if self.noWick() and self.shadow > 0.0 and self.shadow <= self.height * 0.0346:
                return True

        return False

            
    def set_period_trends(self, candlesticks):
        data = []
        for c in candlesticks:
            data.append({'timestamp': c.timestamp, 'high': c.high, 'low': c.low})
            df = pd.DataFrame(data)

        window_size = 5  
        highest_highs = df['high'].rolling(window=window_size).max()
        lowest_lows = df['low'].rolling(window=window_size).min()
        current_trend = 'undefined'
        trends = []
        
        for i in range(len(df)):
            if i < window_size - 1:
                trends.append(current_trend)
            else:
                if df['high'].iloc[i] > highest_highs.iloc[i - 1]:
                    new_trend = 'up'
                elif df['low'].iloc[i] < lowest_lows.iloc[i - 1]:
                    new_trend = 'down'
                else:
                    new_trend = 'sideways'

                if new_trend != current_trend:
                    current_trend = new_trend
                trends.append(current_trend)

        df['trend'] = trends

        for i in range(len(df)):
            candlesticks[i].period_trend = df['trend'].iloc[i]


    def print(self):
        s = "Bullish"
        if self.trend == 0:
            s = "Bearish"
        print(f"{s} {self.timestamp}")

    def __eq__(self, other):
        if not isinstance(other, Candlestick):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.timestamp == other.timestamp)