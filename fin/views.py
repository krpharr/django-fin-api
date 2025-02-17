from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import yfinance as yf
import pandas as pd
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Candlestick
import Pattern
from .Pattern import (
    Doji, Engulfing, EveningStar, MorningStar, HangingMan, Hammer, InvertedHammer, 
    ShootingStar, UpsideGapTwoCrows, TwoCrows, ThreeWhiteSolders, ThreeBlackCrows, 
    PiercingLine, DarkCloudCover, SpinningTop, Marubozu, Harami, HaramiCross, Kicker, 
    Tweezers, ThreeInside, ThreeMethods, NeckLine, ThrustingLine, Gap, AbandonedBaby, 
    BeltHold, Breakaway, AdvanceBlock, Deliberation, StickSandwich, TasukiGap, 
    SideBySideWhiteLines, ThreeStars, ThreeLineStrike, UniqueThreeRiverBottom, 
    MatHold, CounterattackLines, HomingPigeon, Ladder, Matching, SeperatingLines, 
    TriStar, Spring
)

from datetime import datetime


@csrf_exempt
@require_http_methods(["GET"])
def get_candles(request, ticker, timeframe, lookback):
    """
    Fetch candle data from Yahoo Finance, detect patterns, and return structured JSON.
    Example URL: /api/fin/candles/AAPL/1d/1mo/
    """
    try:
        # Fetch stock data from Yahoo Finance
        stock = yf.download(ticker, interval=timeframe, period=lookback)

        # Ensure data is available
        if stock.empty:
            return JsonResponse({"error": "No data found for the given parameters"}, status=404)

        # Reset index and rename columns to match JSON format
        #stock.reset_index(inplace=True)
        # stock.rename(columns={
        #     "Date": "date",
        #     "Open": "open_price",
        #     "High": "high_price",
        #     "Low": "low_price",
        #     "Close": "close_price",
        #     "Adj Close": "adj_close",
        #     "Volume": "volume",
        # }, inplace=True)

        # Prepare candlestick pattern analysis
        candlesticks = []
        doji = Doji()
        engulfing = Engulfing()
        evening_star = EveningStar()
        morning_star = MorningStar()
        hanging_man = HangingMan()
        hammer = Hammer()
        invertedhammer = InvertedHammer()
        shootingstar = ShootingStar()
        upsidegaptwocrows = UpsideGapTwoCrows()
        twocrows = TwoCrows()
        threewhitesolders = ThreeWhiteSolders()
        threeblackcrows = ThreeBlackCrows()
        piercingline = PiercingLine()
        darkcloudcover = DarkCloudCover()
        spinningtop = SpinningTop()
        marubozu = Marubozu()
        harami = Harami()
        haramicross = HaramiCross()
        kicker = Kicker()
        tweezers = Tweezers()
        threeinside = ThreeInside()
        threemethods = ThreeMethods()
        neckline = NeckLine()
        thrustingline = ThrustingLine()
        gap = Gap()
        abandonedbaby = AbandonedBaby()
        belthold = BeltHold()
        breakaway = Breakaway()
        advanceblock = AdvanceBlock()
        deliberation = Deliberation()
        sticksandwich = StickSandwich()
        tasukigap = TasukiGap()
        sidebysidewhitelines = SideBySideWhiteLines()
        threestars = ThreeStars()
        threelinestrike = ThreeLineStrike()
        uniquethreeriverbottom = UniqueThreeRiverBottom()
        mathold = MatHold()
        counterattacklines = CounterattackLines()
        homingpigeon = HomingPigeon()
        ladder = Ladder()
        matching = Matching()
        seperatinglines = SeperatingLines()
        tristar = TriStar()
        spring = Spring()

    
        pattern_tests = [doji, engulfing, evening_star, morning_star, hanging_man, hammer, invertedhammer, shootingstar, upsidegaptwocrows,
            twocrows, threewhitesolders, threeblackcrows, piercingline, darkcloudcover, spinningtop, marubozu, harami, haramicross,
            kicker, tweezers, threeinside, threemethods, neckline, thrustingline, gap, abandonedbaby, belthold, breakaway, advanceblock, 
            deliberation, sticksandwich, tasukigap, sidebysidewhitelines, threestars, threelinestrike, uniquethreeriverbottom, mathold,
            counterattacklines, homingpigeon, ladder, matching, seperatinglines, tristar, spring]        

        # pattern_tests = [doji]

        # Convert stock data into candlestick objects
        for i in stock.index:
            c = Candlestick.Candlestick(i, stock['Open'][i], stock['High'][i], stock['Low'][i], stock['Close'][i], stock['Volume'][i])
            candlesticks.append(c)


        # Set trend for candlestick patterns
        candlesticks[0].set_period_trends(candlesticks)

        # Analyze patterns and store results
        all_results = []
        for pattern in pattern_tests:
            results = pattern.get_matches(candlesticks)
            for r in results:
                all_results.append([r[1], r[0], r[2]])  # Format: [date, pattern_name, extra_data]

        # Organize pattern results by date
        sorted_data = sorted(all_results, key=lambda x: x[0])
        pattern_dict = {}
        for date, pattern_name, _ in sorted_data:
            date_str = date.strftime('%Y-%m-%d')
            if date_str not in pattern_dict:
                pattern_dict[date_str] = []
            pattern_dict[date_str].append(pattern_name)

        # Attach detected patterns to stock data
        stock["Patterns"] = stock.index.to_series().dt.strftime('%Y-%m-%d').apply(lambda date: ", ".join(pattern_dict.get(date, [])))
        # Convert to JSON format
        stock.reset_index(inplace=True)
        stock_json = stock.to_json(orient="records", date_format="iso", indent=4)

        return JsonResponse(json.loads(stock_json), safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
