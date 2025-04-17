from Candlestick import Candlestick

class Pattern:
    def __init__(self, name, trend, window, indicator, desc=""):
        self.name = name
        self.trend = trend
        self.window = window #number of candles in pattern
        self.indicator = indicator # which candle back from the left edge is the indicating candle ie: [-1]
        # self.candles = []
        self.desc = desc

    def seek(self, candlesticks):
        matches = []
        return matches
    
    def get_matches(self, candlesticks):
        # return array that contains ["Description" + "Bull or Bear", timestamp, [array of candlesticks that comprise the window of pattern]]
        matches = []
        return matches

       
class Doji(Pattern):
    def __init__(self):
        super().__init__("Doji", 1, 1, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_height = Candlestick.get_average_height(self, candlesticks)
        for c in candlesticks:
          if c.isDoji(average_body_height):
              # if has a wick and a shadow
              if c.wick > 0.0 and c.shadow > 0.0 and c.period_trend != 'sideways':
                  # is long-legged?
                  if c.height >= average_body_height:
                      if c.open == c.close or c.bodysize <= average_body_height * 0.05:
                          if c.wick <= c.height * 0.2:
                            matches.append([c, "Dragonfly "])
                          if c.shadow <= c.height * 0.2:
                            matches.append([c, "Gravestone "])
                          if c.wick <= c.height * 0.346 and c.wick > c.height * 0.2:
                            matches.append([c, "Rickshaw Man "])
                      else:
                          matches.append([c, "Long-Legged "])      
                  else:
                      matches.append([c, ""])     
              if c.wick <= 0 and c.shadow > 0:
                    matches.append([c, "Dragonfly "])  
              if c.shadow <= 0 and c.wick > 0:
                    matches.append([c, "Gravestone "])
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d[0].trend == 0:
                t = "Bearish"
            matches.append([d[1] + "Doji " + t, d[0].timestamp, d[0].trend])
        return matches
    
class Engulfing(Pattern):
    def __init__(self):
        super().__init__("Engulfing", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if b.bodytop > a.bodytop and b.bodybottom < a.bodybottom and a.trend != b.trend:
                matches.append([a,b])
        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d[1].trend == 0:
                t = "Bearish"
            matches.append(["Engulfing " + t, d[1].timestamp, d[1].trend])
        return matches
    
class EveningStar(Pattern):
    def __init__(self):
        super().__init__("Evening Star", 0, 3, 1)
    
    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.trend == 1 and c.trend == 0:
                if b.bodybottom > a.bodytop:
                  if c.open < b.bodybottom:
                      #check b bodysize to see if its small
                      if b.bodysize <= a.bodysize / 8:
                          # does the body of c penetrate deep into body of a 
                          if c.bodybottom < a.bodytop:
                              matches.append([a,b,c])

            # if a.trend == 0 and c.trend == 1:
            #     if b.bodytop < a.bodybottom:
            #       if c.open > b.bodytop:
            #           #check b bodysize to see if its small
            #           if b.bodysize <= a.bodysize / 8:
            #               # does the body of c penetrate deep into body of a 
            #               if c.bodytop > a.bodybottom:
            #                   matches.append([a,b,c])


        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Evening Star Bearish ", d[2].timestamp, 0])
        return matches
    
class MorningStar(Pattern):
    def __init__(self):
        super().__init__("Morning Star", 1, 3, 1)
    
    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 0 and c.trend == 1:
                if b.bodytop < a.bodybottom:
                  if c.open > b.bodytop:
                      #check b bodysize to see if its small
                      if b.bodysize <= average_body_size:
                          # does the body of c penetrate deep into body of a 
                          if c.bodytop > a.bodybottom:
                              matches.append([a,b,c])

            # if a.trend == 1 and c.trend == 0:             
            #     if b.bodybottom > a.bodytop:
            #         if c.open < b.bodybottom:
            #             #check b bodysize to see if its small
            #             if b.bodysize <= a.bodysize / 8:
            #                 # does the body of c penetrate deep into body of a 
            #                 if c.bodybottom < a.bodytop:
            #                     matches.append([a,b,c])

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Morning Star Bullish ", d[2].timestamp, 1])
        return matches

class HangingMan(Pattern):
    def __init__(self):
        # start with a 10 bar window and test penultimate  bar to see if in range, %10 percent price of top of bullish trend
        # then test last bar to see if closes lower than penultimate
        super().__init__("Hanging Man", 0, 2, 2)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        # average_close = Candlestick.get_average_close(self, candlesticks)
        # peaks = Candlestick.get_peaks(self, candlesticks)

        # find all hangingman bodys, wick and shadow matches regardless of price 
        # - include following candle to later check for confirmation
        hangingmen = []

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            # is a within %10 of top prices and higher than the first candle open
            if a.period_trend == 'up' and b.trend == 0 and b.close < a.close:
                if a.bodysize <= a.height * 0.33 and a.bodysize > average_body_size * a.DOJIFACTOR:
                    if a.shadow >= a.bodysize * 2.0:
                        if a.wick > 0 and a.wick < a.shadow * 0.2:
                            hangingmen.append([a, b])
        
        # for h in hangingmen:
        #     for p in peaks:
        #         if p == h[0]:
        #            # check to see if b h[1].trend == 0 and closes lower 
        #             if h[1].trend == 0 and h[1].close < h[0].close:
        #                 matches.append(h)

        for h in hangingmen:
            matches.append(h)

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Hanging Man Bearish ", d[0].timestamp, 0])
        return matches    
    
class ShootingStar(Pattern):
    def __init__(self):
        # start with a 10 bar window and test penultimate  bar to see if in range, %10 percent price of top of bullish trend
        # then test last bar to see if closes lower than penultimate
        super().__init__("Shooting Star", 0, 3, 2)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        average_close = Candlestick.get_average_close(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)

        # find all hangingman bodys, wick and shadow matches regardless of price 
        # - include following candle to later check for confirmation
        shootingstars = []

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.period_trend == 'up' and c.trend == 0 and b.bodyHigher(a) and c.close < b.close:
                if b.bodysize <= b.height / 3 and b.bodysize < average_body_size:
                    if b.wick > b.bodysize * 1.8:
                        if b.shadow >= 0 and b.shadow <= b.wick * 0.1:
                            matches.append([a, b, c])
    
        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Shooting Star Bearish ", d[1].timestamp, 2])
        return matches    
    
class Hammer(Pattern):
    def __init__(self):
        super().__init__("Hammer", 1, 2, 2)

    def seek(self, candlesticks):
        matches = []
        hammers = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.period_trend == 'down' and b.trend == 1 and b.close > a.close:
                if a.bodysize <= a.height * 0.33 and a.bodysize > average_body_size * a.DOJIFACTOR:
                    if a.shadow >= a.bodysize * 2.0:
                        if a.wick >= 0 and a.wick < a.bodysize * 0.2:
                            hammers.append([a, b])
        
        for h in hammers:
            matches.append(h)

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Hammer Bullish ", d[0].timestamp, 1])
        return matches 

class InvertedHammer(Pattern):
    def __init__(self):
        super().__init__("Inverted Hammer", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        hammers = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.period_trend == 'down' and b.trend == 1 and b.close > a.close:
                if a.bodysize <= a.height * 0.33 and a.bodysize > average_body_size * a.DOJIFACTOR:
                    if a.wick >= a.bodysize * 2:
                        if a.shadow > 0 and a.shadow < a.bodysize * 0.2:
                            hammers.append([a, b])      
        
        for h in hammers:
            matches.append(h)

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Inverted Hammer Confirmed Bullish ", d[1].timestamp, 1])
        return matches    

class TwoCrows(Pattern):
    def __init__(self):
        # start with a 10 bar window and test penultimate  bar to see if in range, %10 percent price of top of bullish trend
        # then test last bar to see if closes lower than penultimate
        super().__init__("Two Crows", 0, 3, 3)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        average_close = Candlestick.get_average_close(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)

        crows = []

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.trend == 1 and b.trend == 0 and c.trend == 0:
                if a.bodysize > average_body_size:
                    if b.open > a.close and b.close <= a.close and b.close >= a.open:
                        if c.open <= b.close and c.open >= b.open and c.close >= a.open:
                            crows.append([b,c])   

        for c in crows:
            for p in peaks:
                if p == c[0]:
                     matches.append(c)

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Two Crows Bearish ", d[0].timestamp, 0])
        return matches    

class UpsideGapTwoCrows(Pattern):
    def __init__(self):
        # start with a 10 bar window and test penultimate  bar to see if in range, %10 percent price of top of bullish trend
        # then test last bar to see if closes lower than penultimate
        super().__init__("Two Crows UpsideGap", 0, 3, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        average_close = Candlestick.get_average_close(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)

        crows = []

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.trend == 1 and b.trend == 0 and c.trend == 0:
                if a.bodysize > average_body_size:
                    if b.bodybottom > a.bodytop:
                        if c.open > b.open and c.close < b.close and c.close > a.close:
                            crows.append([b,c])   

        for c in crows:
            for p in peaks:
                if p == c[0]:
                     matches.append(c)

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Upside Gap Two Crows Bearish ", d[1].timestamp, 0])
        return matches    
    
class ThreeWhiteSolders(Pattern):
    def __init__(self):
        super().__init__("Three White Solders", 1, 3, 1)
    
    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)

        bottoms = Candlestick.get_bottoms(self, candlesticks)
      
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 1 and b.trend == 1 and c.trend == 1:
                if a.open < b.open and b.open < c.open:
                    if a.bodysize >= average_body_size * 0.66 and b.bodysize >= average_body_size * 0.66 and c.bodysize >= average_body_size * 0.66:
                        if a.wick < a.bodysize * 0.4 and b.wick < b.bodysize * 0.4 and c.wick < c.bodysize * 0.4:
                            if a.shadow < a.bodysize * 0.4 and b.shadow < b.bodysize * 0.4 and c.shadow < c.bodysize * 0.4:
                                if b.open >= a.close - (a.bodysize * 0.5) and b.open <= a.close:
                                    if c.open >= b.close - (a.bodysize * 0.5) and c.open <= b.close:
                                        matches.append([a, b, c])                     

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Three White Solders Bullish", d[2].timestamp, 1])
        return matches
    
class ThreeBlackCrows(Pattern):
    def __init__(self):
        super().__init__("Three Black Crows", 0, 4, 1)
    
    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)

        highs = Candlestick.get_peaks(self, candlesticks)

        for i in range(0, len(candlesticks)-(self.window-1)):
            h = candlesticks[i]
            a = candlesticks[i+1]
            b = candlesticks[i+2]
            c = candlesticks[i+3]

            if Candlestick.isIn(self, h, highs):
              if a.trend == 0 and b.trend == 0 and c.trend == 0:
                  if a.close > b.close and b.close > c.close:
                      if a.bodysize >= average_body_size * 0.66 and b.bodysize >= average_body_size * 0.66 and c.bodysize >= average_body_size * 0.66:
                          if a.wick < a.bodysize * 0.4 and b.wick < b.bodysize * 0.4 and c.wick < c.bodysize * 0.4:
                              if a.shadow < a.bodysize * 0.4 and b.shadow < b.bodysize * 0.4 and c.shadow < c.bodysize * 0.4:
                                  if b.open <= a.close + (a.bodysize * 0.5) and b.open >= a.close:
                                      if c.open <= b.close + (a.bodysize * 0.5) and c.open >= b.close:
                                          matches.append([a, b, c])                             

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Three Black Crows Bearish", d[2].timestamp, 0])
        return matches
            
class PiercingLine(Pattern):
    def __init__(self):
        super().__init__("Peircing Line", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        bottoms = Candlestick.get_bottoms(self, candlesticks)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if Candlestick.isIn(self, a, bottoms):
                if a.trend == 0 and b.trend == 1:
                    if a.bodysize >= average_body_size * 0.66 and b.bodysize >= average_body_size * 0.66:
                        if b.open < a.low and b.close >= a.midpoint - (a.bodysize * 0.075) and b.close <= a.bodytop:
                            matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Peircing Line Bullish", d[1].timestamp, 1])
        return matches    

class DarkCloudCover(Pattern):
    def __init__(self):
        super().__init__("Dark Cloud Cover", 0, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if Candlestick.isIn(self, a, peaks):
                if a.trend == 1 and b.trend == 0:
                    if a.bodysize >= average_body_size * 0.66 and b.bodysize >= average_body_size * 0.66:
                        if b.open > a.high and b.close <= a.midpoint + (a.bodysize * 0.075) and b.close >= a.bodybottom:
                            matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Dark Cloud Cover - Bearish", d[1].timestamp, 0])
        return matches         

class SpinningTop(Pattern):
    def __init__(self):
        super().__init__("Spinning Top", 1, 1, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        bottoms = Candlestick.get_bottoms(self, candlesticks)
            
        for c in candlesticks:
            if c.bodysize / average_body_size > c.DOJIFACTOR and c.bodysize < average_body_size:
                if c.wick <= c.shadow + (c.shadow * .2) and c.wick >= c.shadow - (c.shadow * .2):
                    if c.shadow <= c.wick + (c.wick * .2) and c.shadow >= c.wick - (c.wick * .2):
                      for p in peaks:
                          if c == p:
                            #   c.trend == 0
                              matches.append(c)
                      for b in bottoms:
                          if c == b:
                            #   c.trend = 1
                              matches.append(c)
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d.trend == 0:
                t = "Bearish"
            matches.append(["Spinning Top " + t, d.timestamp, d.trend])
        return matches
    
class Marubozu(Pattern):
    def __init__(self):
        super().__init__("Marubozu", 1, 1, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
            
        for c in candlesticks:
            if c.bodysize >= average_body_size:

                if c.trend == 0:
                    if c.noWick() and c.noShadow():
                        matches.append([c, "Marubozu"])
                    if c.noShadow() and c.wick > 0.0:
                        matches.append([c, "Marubozu Close"])
                    if c.noWick() and c.shadow > 0.0:
                        matches.append([c, "Marubozu Open"])

                if c.trend == 1:
                    if c.noWick() and c.noShadow():
                        matches.append([c, "Marubozu"])
                    if c.noShadow() and c.wick > 0.0:
                        matches.append([c, "Marubozu Open"])
                    if c.noWick() and c.shadow > 0.0:
                        matches.append([c, "Marubozu Close"])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d[0].trend == 0:
                t = "Bearish"
            matches.append([d[1] + " " + t, d[0].timestamp, d[0].trend])
        return matches    
    
class Harami(Pattern):
    def __init__(self):
        super().__init__("Harami", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        lows = Candlestick.get_bottoms(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.trend != b.trend:
                if a.bodysize >= average_body_size and b.bodysize > average_body_size * a.DOJIFACTOR and b.high < a.bodytop and b.low > a.bodybottom:
                    if a.trend == 0:
                        for l in lows:
                            if a == l:
                                matches.append([a, b])
                    if a.trend == 1:
                        for p in peaks:
                            if a == p:
                                matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d[1].trend == 0:
                t = "Bearish"
            matches.append(["Harami " + t, d[1].timestamp, d[1].trend])
        return matches    
    
class HaramiCross(Pattern):
    def __init__(self):
        super().__init__("Harami Cross", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        lows = Candlestick.get_bottoms(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.trend != b.trend:
                if a.bodysize >= average_body_size and b.bodysize <= average_body_size * a.DOJIFACTOR and b.bodytop < a.bodytop and b.bodybottom > a.bodybottom:
                    if a.trend == 0:
                        for l in lows:
                            if a == l:
                                matches.append([a, b])
                    if a.trend == 1:
                        for p in peaks:
                            if a == p:
                                matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d[1].trend == 0:
                t = "Bearish"
            matches.append(["Harami Cross " + t, d[1].timestamp, d[1].trend])
        return matches    
    
class Kicker(Pattern):
    def __init__(self):
        super().__init__("Kicker", 1, 2, 2)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.trend != b.trend:
                if a.trend == 0:
                    if b.low > a.high:
                        matches.append([a, b])
                if a.trend == 1:
                    if b.high < a.low:
                        matches.append([a, b])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            t = "Bullish"
            if d[1].trend == 0:
                t = "Bearish"
            matches.append([t + " Kicker", d[0].timestamp, d[1].trend])
        return matches    
    
class Tweezers(Pattern):
    def __init__(self):
        super().__init__("Tweezers", 1, 3, 2)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        lows = Candlestick.get_bottoms(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.period_trend == "up" and c.trend == 0:
                if b.high <= a.high + (a.high * .0015) and b.high >= a.high - (a.high * .0015):
                    for p in peaks:
                        if a == p:
                            matches.append([a, b, c])
            if a.period_trend == "down" and c.trend == 1:
                if b.low <= a.low + (a.low * .0015) and b.low >= a.low - (a.low * .0015):
                    for l in lows:
                        if a == l:
                            matches.append([a, b, c])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        t = ""
        for d in f:
            if d[2].trend == 0:
                t = " Tops Bearish"
            else:
                t = " Bottoms Bullish"
            matches.append(["Tweezer" + t, d[1].timestamp, d[2].trend])
        return matches   

class ThreeInside(Pattern):
    def __init__(self):
        super().__init__("Three Inside", 1, 3, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        lows = Candlestick.get_bottoms(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.period_trend == "up"  and a.trend == 1 and b.trend == 0 and c.trend == 0:
                if a.bodysize >= average_body_size and b.open >= a.close and b.close <= a.midpoint and b.close > a.open:
                    if c.price_in_body(c.open, a) and c.close < a.low:
                        matches.append([a, b, c])
            if a.period_trend == "down" and a.trend == 0 and b.trend == 1 and c.trend == 1:
                if a.bodysize >= average_body_size and b.open <= a.close and b.close >= a.midpoint and b.close < a.open:
                    if c.price_in_body(c.open, a) and  c.close > a.high:
                        matches.append([a, b, c])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        t = ""
        for d in f:
            if d[2].trend == 0:
                t = " Down"
            else:
                t = " Up"
            matches.append(["Three Inside" + t, d[2].timestamp, d[2].trend])
        return matches     
    
class ThreeMethods(Pattern):
    def __init__(self):
        super().__init__("Three Methods", 1, 5, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        lows = Candlestick.get_bottoms(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            d = candlesticks[i+3]
            e = candlesticks[i+4]
            if a.trend == 1 and e.trend == 1:
                if a.bodysize >= average_body_size and e.bodysize >= average_body_size and e.close > a.close:
                    if b.insideRange(a) and c.insideRange(a) and d.insideRange(a):
                        for p in peaks:
                            if a == p:
                                matches.append([a,b,c,d,e])
            if a.trend == 0 and e.trend == 0:
                if a.bodysize >= average_body_size and e.bodysize >= average_body_size and e.close < a.close:
                    if b.insideRange(a) and c.insideRange(a) and d.insideRange(a):
                        for l in lows:
                            if a == l:
                                matches.append([a,b,c,d,e])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        t = ""
        tt = ""
        for d in f:
            if d[4].trend == 0:
                t = "Falling "
                tt = "Bearish"
            else:
                t = "Rising "
                tt = "Bullish"
            matches.append([t + "Three Methods " + tt, d[4].timestamp, d[4].trend])
        return matches     
    
class NeckLine(Pattern):
    def __init__(self):
        super().__init__("Neck Line", 0, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.trend == 0 and a.bodysize >= average_body_size:
                if b.trend == 1 and b.open < a.low and b.bodysize <= average_body_size:
                    if b.close >= a.low and b.close < a.bodybottom:
                        matches.append([a, b, "On"])
                    if b.close >= a.bodybottom and b.close < a.bodybottom + (a.bodysize * 0.25):
                        matches.append([a, b, "In"])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
                matches.append([d[2] + " Neck Line Bearish", d[1].timestamp, 0])
        return matches     
    
class ThrustingLine(Pattern):
    def __init__(self):
        super().__init__("Thrusting Line", 0, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.trend == 0 and b.trend == 1:
                if a.bodysize >= average_body_size and b.open > a.low + (a.bodysize * 0.346) and b.close <= a.midpoint and b.close > a.bodybottom:
                    matches.append([a, b])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
                matches.append(["Thrusting Line - watch for breakout in either direction", d[1].timestamp, 1])
        return matches   
    
class Gap(Pattern):
    def __init__(self):
        super().__init__("Gap", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if b.low > a.high and b.close > b.open:
                matches.append([b, "Up"])
            if b.high < a.low and b.close < b.open:
                matches.append([b, "Low"])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
                t = ""
                if d[1] == "Up":
                    t = " Bullish"
                    trend = 1
                else:
                    t = " Bearish"
                    trend = 0
                matches.append(["Gap " + d[1] + t, d[0].timestamp, trend])
        return matches   
    
class AbandonedBaby(Pattern):
    def __init__(self):
        super().__init__("Abandoned Baby", 1, 3, 3)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
          
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.trend == 0 and c.trend == 1:
                if a.bodysize >= average_body_size and c.bodysize >= average_body_size:
                    if b.high < a.low and c.low > b.high:
                        if b.isDoji(average_body_size):
                            matches.append([a, b, c])

            if a.trend == 1 and c.trend == 0:
                if a.bodysize >= average_body_size and c.bodysize >= average_body_size:
                    if b.low > a.high and c.high < b.low:
                        if b.isDoji(average_body_size):
                            matches.append([a, b, c])
 
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
                t = ""
                if d[2].trend == 1:
                    t = " Bullish"
                else:
                    t = " Bearish"
                matches.append(["Abandoned Baby " + t, d[2].timestamp, d[2].trend])
        return matches   

class BeltHold(Pattern):
    def __init__(self):
        super().__init__("Belt Hold", 1, 1, 1)

    def seek(self, candlesticks):
        matches = []
        average_height = Candlestick.get_average_height(self, candlesticks)
          
        for a in candlesticks:
            if a.height >= average_height: 
                if a.trend == 0:
                    if a.open >= a.high - (a.height * 0.25) and a.wick <= a.height * 0.25 and a.shadow < a.height * 0.025 and a.wick > a.shadow:
                        matches.append(a)
                if a.trend == 1:
                    if a.open <= a.low + (a.height * 0.25) and a.shadow < a.height * 0.25 and a.wick < a.height * 0.025 and a.wick < a.shadow:
                        matches.append(a)
                
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
                t = ""
                if d.trend == 1:
                    t = " Bullish"
                else:
                    t = " Bearish"
                matches.append(["Belt Hold " + t, d.timestamp, d.trend])
        return matches   
    
class Breakaway(Pattern):
    def __init__(self):
        super().__init__("Breakaway", 1, 5, 5)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        peaks = Candlestick.get_peaks(self, candlesticks)
        lows = Candlestick.get_bottoms(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            d = candlesticks[i+3]
            e = candlesticks[i+4]
            if a.trend == 0 and e.trend == 1:
                 if a.bodysize >= average_body_size and e.bodysize >= average_body_size:
                     if b.bodyLower(a) and b.trend == 0 and c.close < b.close and d.close < c.close:
                        if e.price_in_range(e.open, d) and e.close > b.high and e.close < a.low:
                                matches.append([a,b,c,d,e])

            if a.trend == 1 and e.trend == 0:
                 if a.bodysize >= average_body_size and e.bodysize >= average_body_size:
                    if b.bodyHigher(a) and b.trend == 1 and c.close > b.close and d.close > c.close:
                        if e.price_in_range(e.open, d) and e.close < b.low and e.close > a.high:
                                matches.append([a,b,c,d,e])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        t = ""
        tt = ""
        for d in f:
            if d[4].trend == 0:
                t = "Bearish"
            else:
                t = "Bullish"
            matches.append(["Breakaway " + t, d[4].timestamp, d[4].trend])
        return matches     
    
class AdvanceBlock(Pattern):
    def __init__(self):
        super().__init__("Advance Block", 0, 3, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 1 and b.trend == 1 and c.trend == 1:
                if b.price_in_body(b.open, a) and b.close > a.close and b.wick > a.wick and b.bodysize < a.bodysize: 
                    if c.price_in_body(c.open, b) and c.close > b.close and c.wick > b.wick and c.bodysize < b.bodysize:
                        matches.append([a, b, c])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            matches.append(["Advance Block Bearish", d[2].timestamp, 0])
        return matches    

class Deliberation(Pattern):
    def __init__(self):
        super().__init__("Deliberation", 0, 3, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 1 and b.trend == 1:
                # print(f"{a.timestamp}")
                if a.is_large_body(average_body_size) and b.is_large_body(average_body_size) and c.is_small_body(average_body_size):
                    # print("bodysize")
                    if b.open > a.open and b.close > a.close:
                        # print("b bullish")
                        if c.open >= b.close and c.open <= b.close + (b.height * 0.20) and c.close > b.close:
                            # print("c good")
                            matches.append([a, b, c])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            matches.append(["Deliberation Bearish", d[2].timestamp, 0])
        return matches        

class StickSandwich(Pattern):
    def __init__(self):
        super().__init__("Stick Sandwich", 0, 3, 1)

    def seek(self, candlesticks):
        matches = []
        abs = Candlestick.get_average_bodysize(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.within_range(a.bodytop, c.bodytop, 1) and a.within_range(a.bodybottom, c.bodybottom, 1):

                if a.period_trend == 'down' and a.trend == 0 and b.trend == 1 and c.trend == 0:
                    if a.bodysize > abs and b.bodysize > abs and c.bodysize > abs:
                        mh = a.high if a.high >= c.high else c.high
                        ml = a.low if a.low <= c.low else c.low
                        if b.high <= mh and b.low >= ml:
                            matches.append([a, b, c])

                if a.period_trend == 'up' and a.trend == 1 and b.trend == 0 and c.trend == 1:
                    if a.bodysize > abs and b.bodysize > abs and c.bodysize > abs:
                        mh = a.high if a.high >= c.high else c.high
                        ml = a.low if a.low <= c.low else c.low
                        if b.high <= mh and b.low >= ml:
                            matches.append([a, b, c])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = "Bearish"
            trend = 0
            if d[0].trend == 0:
                t = "Bullish"
                trend = 1
            matches.append(["Stick Sandwich " + t, d[2].timestamp, trend])
        return matches   

class TasukiGap(Pattern):
    def __init__(self):
        super().__init__("Tasuki Gap", 1, 3, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 0 and a.is_large_body(average_body_size) and b.trend == 0 and c.trend == 1 and c.is_small_body(average_body_size):
                if b.gapsLower(a) and c.price_in_body(c.open, b) and c.close > b.bodytop and c.close < a.bodybottom:
                    matches.append([a, b, c])

            if a.trend == 1 and a.is_large_body(average_body_size) and b.trend == 1 and c.trend == 0 and c.is_small_body(average_body_size):
                if b.gapsHigher(a) and c.price_in_body(c.open, b) and c.close < b.bodybottom and c.close > a.bodytop:
                    matches.append([a, b, c])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = "Bullish"
            if d[0].trend == 0:
                t = "Bearish"
            matches.append(["Tasuki Gap " + t, d[2].timestamp, d[0].trend])
        return matches            

class SideBySideWhiteLines(Pattern):
    def __init__(self):
        super().__init__("Side-By=Side White Lines", 1, 3, 3)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 0 and a.is_large_body(average_body_size):
                if b.trend == 1 and c.trend == 1:
                    if b.bodyLower(a) and c.bodytop <= b.bodytop + (b.height * 0.1) and c.bodybottom >= b.bodybottom - (b.height * 0.1):
                        d = 1.0
                        if b.bodysize > c.bodysize:
                            d = c.bodysize / b.bodysize
                        if b.bodysize < c.bodysize:
                            d = b.bodysize / c.bodysize
                        if d > 0.66:
                            matches.append([a, b, c])

            if a.trend == 1 and a.is_large_body(average_body_size):
                if b.trend == 0 and c.trend == 0:
                    if b.bodyHigher(a) and c.bodytop <= b.bodytop + (b.height * 0.1) and c.bodybottom >= b.bodybottom - (b.height * 0.1):
                        d = 1.0
                        if b.bodysize > c.bodysize:
                            d = c.bodysize / b.bodysize
                        if b.bodysize < c.bodysize:
                            d = b.bodysize / c.bodysize
                        if d > 0.66:
                            matches.append([a, b, c])
        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = "Bullish"
            if d[2].trend == 0:
                t = "Bearish"
            matches.append(["Side-By=Side White Lines " + t, d[2].timestamp, d[2].trend])
        return matches            

class ThreeStars(Pattern):
    def __init__(self):
        super().__init__("Three Stars", 1, 3, 3)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            if a.trend == 0 and b.trend == 0 and c.trend == 0:
                if a.is_large_body(average_body_size) and a.longWick():
                    if b.low > a.low and b.wick and c.isMarubozu() and c.insideRange(b):
                        matches.append([a, b, c])

            if a.trend == 1 and b.trend == 1 and c.trend == 1:
                if a.is_large_body(average_body_size) and a.longWick():
                    if b.high < a.high and b.wick and c.isMarubozu() and c.insideRange(b):
                        matches.append([a, b, c])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = "in the North Reversal - Bearish Signal"
            trend = 0
            if d[0].trend == 0:
                t = "in the South Reversal - Bullish Signal"
                trend = 1
            matches.append(["Three Stars " + t, d[2].timestamp, trend])
        return matches         

class ThreeLineStrike(Pattern):
    def __init__(self):
        super().__init__("Three Line Strike", 1, 5, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            d = candlesticks[i+3]
            e = candlesticks[i+4]

            if a.trend == 0 and b.trend == 0 and c.trend == 0 and d.trend == 1 and d.is_large_body(average_body_size) and e.close < d.low:
                if b.close < a.close and c.close < b.close:
                    if d.open < b.close and d.close > a.open:
                        matches.append([a, b, c, d, e])
 
            if a.trend == 1 and b.trend == 1 and c.trend == 1  and d.trend == 0 and d.is_large_body(average_body_size) and e.close > d.high:
                if b.close > a.close and c.close > b.close: 
                    if d.open > c.close and d.close < a.open:
                        matches.append([a, b, c, d, e]) 

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = "Bearish"
            if d[3].trend == 1:
                t = "Bullish"
            matches.append(["Three Line Strike " + t, d[4].timestamp, d[4].trend])
        return matches                      

class UniqueThreeRiverBottom(Pattern):
    def __init__(self):
        super().__init__("Unique Three River Bottom", 0, 3, 3)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
 
            if a.is_large_body(average_body_size) and a.trend == 0:
                if b.low <= a.low and b.price_in_range(b.bodytop, a) and b.price_in_range(b.bodybottom, a):
                    if c.close > b.close and c.open < b.close and c.price_in_body(c.close, b):
                        matches.append([a, b, c])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            matches.append(["Unique Three River Bottom - Bearish", d[2].timestamp, 0])
        return matches                      

class MatHold(Pattern):
    def __init__(self):
        super().__init__("Mat Hold", 1, 5, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            d = candlesticks[i+3]
            e = candlesticks[i+4]
 
            if a.trend == 1 and a.is_large_body(average_body_size) and e.trend == 1 and e.is_large_body(average_body_size):
                    if b.insideRange(a) and c.insideRange(a) and d.insideRange(a):
                        if e.close > d.high:
                            matches.append([a, b, c, d, e])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            matches.append(["Mat Hold - Bullish", d[4].timestamp, 1])
        return matches                      

class CounterattackLines(Pattern):
    def __init__(self):
        super().__init__("Counterattack Lines", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]

            if a.trend == 0 and b.trend == 1:
                if a.is_large_body(average_body_size) and b.is_large_body(average_body_size):
                    if b.open < a.low and b.close <= a.close + (a.bodysize * 0.05) and b.close >= a.close - (a.bodysize * 0.05):
                        matches.append([a, b])

            if a.trend == 1 and b.trend == 0:
                if a.is_large_body(average_body_size) and b.is_large_body(average_body_size):
                    if b.open > a.high and b.close <= a.close + (a.bodysize * 0.05) and b.close >= a.close - (a.bodysize * 0.05):
                        matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = "Bearish"
            if d[1].trend == 1:
                t = "Bullish"
            matches.append(["Counterattack Lines " + t, d[1].timestamp, d[1].trend])
        return matches                      

class HomingPigeon(Pattern):
    def __init__(self):
        super().__init__("Homing Pigeon", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]

            if a.period_trend == 'down' and a.trend == 0 and a.is_large_body(average_body_size) and b.trend == '0':
                if b.high < a.high and b.low > a.low:
                    matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            matches.append(["Homing Pigeon Bullish", d[1].timestamp, 1])
        return matches      

class Ladder(Pattern):
    def __init__(self):
        super().__init__("Ladder", 1, 5, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            d = candlesticks[i+3]
            e = candlesticks[i+4]

            if a.trend == 0 and b.trend == 0 and c.trend == 0 and d.trend == 0 and e.trend == 1:
                if a.is_large_body(average_body_size) and  e.is_large_body(average_body_size):
                    if b.open < a.open and b.price_in_body(b.open, a) and b.close < a.close and c.open < b.open and c.price_in_body(c.open, b) and c.close < b.close:
                        if d.is_small_body(average_body_size) and d.open < c.open and d.close < c.close:
                            if e.open > d.bodytop:
                                matches.append([a, b, c, d, e])



            if a.trend == 1 and b.trend == 1 and c.trend == 1 and d.trend == 1 and e.trend == 0:
                if a.is_large_body(average_body_size) and e.is_large_body(average_body_size):
                    if b.open > a.open and b.price_in_body(b.open, a) and b.close > a.close and c.open > b.open and c.price_in_body(c.open, b) and c.close > b.close:
                        if d.is_small_body(average_body_size) and d.open > c.open and d.close > c.close:
                            if e.open < d.bodybottom:
                                matches.append([a, b, c, d, e])


        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            t = " Top - Bearish"
            if d[4].trend == 1:
                t = " Bottom - Bullish"
            matches.append(["Ladder" + t, d[4].timestamp, d[4].trend])
        return matches                       

class Matching(Pattern):
    def __init__(self):
        super().__init__("Matching Low", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]

            if a.trend == 0 and b.trend == 0 and a.is_large_body(average_body_size):
                if b.close >= a.close - (a.height * 0.01) and b.close <= a.close + (a.height * 0.01):
                    matches.append([a, b])

            if a.trend == 1 and b.trend == 1 and a.is_large_body(average_body_size):
                if b.close >= a.close - (a.height * 0.01) and b.close <= a.close + (a.height * 0.01):
                    matches.append([a, b])


        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            if d[1].trend == 1:
                t = "High"
                trend = 0
            else:
                t = "Low"
                trend = 1
            matches.append(["Matching " + t + " - Reversal", d[1].timestamp, trend])
        return matches     

class SeperatingLines(Pattern):

    def __init__(self):
        super().__init__("Seperating Lines", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]

            if a.trend == 0 and a.is_large_body(average_body_size):
                if b.trend == 1 and b.is_large_body(average_body_size):
                    if b.open <= a.open + (a.height * 0.001) and b.open >= a.open - (a.height * 0.001):
                        matches.append([a, b])

            if a.trend == 1 and a.is_large_body(average_body_size):
                if b.trend == 0 and b.is_large_body(average_body_size):
                    if b.open <= a.open + (a.height * 0.001) and b.open >= a.open - (a.height * 0.001):
                        matches.append([a, b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []

        for d in f:
            if d[1].trend == 1:
                t = "Bullish"
            else:
                t = "Bearish"
            matches.append(["Seperating Lines " + t, d[1].timestamp, d[1].trend])
        return matches         

class TriStar(Pattern):
    def __init__(self):
        super().__init__("Tri-Star", 1, 3, 3)

    def seek(self, candlesticks):
        matches = []
        peaks = Candlestick.get_peaks(self, candlesticks)
        bottoms = Candlestick.get_bottoms(self, candlesticks)
        avgh = Candlestick.get_average_height(self, candlesticks)

        stars = []

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]
            if a.isDoji(avgh) and b.isDoji(avgh) and c.isDoji(avgh):
                stars.append([a, b, c])

        for s in stars:
            for p in peaks:
                for i in range(0, 3):
                    if s[i] == p:
                        matches.append(["Bearish", s])
            for b in bottoms:
                for i in range(0, 3):
                    if s[i] == b:
                        matches.append(["Bullish", s])

        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            if d[0] == "Bullish":
                t = 1
            else:
                t = 0
            matches.append(["Tri-Star " + d[0], d[1][2].timestamp, t])
        return matches    

class FirstOrderPivot(Pattern):
    def __init__(self):
        super().__init__("First Order Pivot", 1, 3, 3)

    def seek(self, candlesticks):
        matches = []
        peaks = Candlestick.get_peaks(self, candlesticks)
        bottoms = Candlestick.get_bottoms(self, candlesticks)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            for p in peaks:
                if b == p:
                    if b in bottoms:
                        matches.append(["High & Low Pivot", b])
                    else:
                        matches.append(["High Pivot", b])
            for p in bottoms:
                if b == p:
                    if b in peaks:
                        matches.append(["High & Low Pivot", b])
                    else:
                        matches.append(["Low Pivot", b])
 
        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append([d[0] + " First Order", d[1].timestamp, ""])
        return matches   

class SecondOrderPivot(Pattern):
    def __init__(self):
        super().__init__("Second Order Pivot", 1, 3, 3)

    
    def seek(self, candlesticks):
        firstorderpivot = FirstOrderPivot() 

        results = firstorderpivot.get_matches(candlesticks)
        ts = [] 
        for r in results:
            ts.append(r[1])
        print(ts)

        pivots = []

        for candle in candlesticks:
            if candle.timestamp in ts:
                pivots.append(candle)

        matches = []
        peaks = Candlestick.get_peaks(self, pivots)
        bottoms = Candlestick.get_bottoms(self, pivots)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            for p in peaks:
                if b == p:
                    if b in bottoms:
                        matches.append(["High & Low Pivot", b])
                    else:
                        matches.append(["High Pivot", b])
            for p in bottoms:
                if b == p:
                    if b in peaks:
                        matches.append(["High & Low Pivot", b])
                    else:
                        matches.append(["Low Pivot", b])
 
        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append([d[0] + " Second Order", d[1].timestamp, ""])
        return matches   

class ThirdOrderPivot(Pattern):
    def __init__(self):
        super().__init__("Third Order Pivot", 1, 3, 3)

    
    def seek(self, candlesticks):
        secondorderpivot = SecondOrderPivot() 

        results = secondorderpivot.get_matches(candlesticks)
        ts = [] 
        for r in results:
            ts.append(r[1])
        print(ts)

        pivots = []

        for candle in candlesticks:
            if candle.timestamp in ts:
                pivots.append(candle)

        matches = []
        peaks = Candlestick.get_peaks(self, pivots)
        bottoms = Candlestick.get_bottoms(self, pivots)

        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            c = candlesticks[i+2]

            for p in peaks:
                if b == p:
                    if b in bottoms:
                        matches.append(["High & Low Pivot", b])
                    else:
                        matches.append(["High Pivot", b])
            for p in bottoms:
                if b == p:
                    if b in peaks:
                        matches.append(["High & Low Pivot", b])
                    else:
                        matches.append(["Low Pivot", b])
 
        return matches

    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append([d[0] + " Third Order", d[1].timestamp, ""])
        return matches   

class Spring(Pattern):
    def __init__(self):
        super().__init__("Spring", 1, 2, 1)

    def seek(self, candlesticks):
        matches = []
        # bottoms = Candlestick.get_bottoms(self, candlesticks)
        average_body_size = Candlestick.get_average_bodysize(self, candlesticks)
        average_height = Candlestick.get_average_height(self, candlesticks)
        average_volume = Candlestick.get_average_volume(self, candlesticks)
       
        for i in range(0, len(candlesticks)-(self.window-1)):
            a = candlesticks[i]
            b = candlesticks[i+1]
            if a.period_trend == 'down':
                if b.bodysize >= average_body_size * 0.68 and b.height > average_height and b.volume >= average_volume * 2:
                    if b.shadow >= b.bodysize * 2  and b.low < a.low:
                        matches.append([b])

        return matches
    
    def get_matches(self, candlesticks):
        f = self.seek(candlesticks)
        matches = []
        for d in f:
            matches.append(["Spring Bullish", d[0].timestamp, 1])
        return matches      