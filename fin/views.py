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
        # stock = yf.download(ticker, interval=timeframe, period=lookback)
        dat = yf.Ticker(ticker)
        stock = dat.history(interval=timeframe, period=lookback)
        stock = stock.sort_index()  # Ensure data is sorted by date
        # Ensure data is available
        if stock.empty:
            return JsonResponse({"error": "No data found for the given parameters"}, status=404)

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
    
@csrf_exempt
@require_http_methods(["GET"])
def get_json_list(request, index, interval, period):
    """
    Returns list of json files that fit index, period, and interval
    """
    try:
        # Define the local file path (modify this to match your actual JSON file location)
    

        # Get the directory of the current file (views.py)
        current_dir = os.path.dirname(__file__)

        # local
        base_dir = os.path.abspath(os.path.join(current_dir, "../../"))

        # production
        # base_dir = os.path.abspath(os.path.join(current_dir, "../../testProj3"))


        # Construct the full path to the JSON file
        target_dir = os.path.join(base_dir, "scans/", index + "." + interval + "." + period +"/")

        print(target_dir)

        # Ensure the directory exists
        if not os.path.exists(target_dir):
            return JsonResponse({"error": "Directory not found"}, status=404)

        # Get all JSON files in the directory
        json_files = [f for f in os.listdir(target_dir) if f.endswith(".json")]

        # Return the list as a JSON response
        return JsonResponse({"json_files": json_files}, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_json_file(request, index, interval, period, filename):
    """
    Reads and returns the JSON content from a specific file.
    """
    try:
        # Get the directory of the current file (views.py)
        current_dir = os.path.dirname(__file__)

        # Move two directories up
        # local
        base_dir = os.path.abspath(os.path.join(current_dir, "../../"))

        # production
        # base_dir = os.path.abspath(os.path.join(current_dir, "../../testProj3"))        

        # Construct the full path to the JSON file
        json_file_path = os.path.join(base_dir, "scans", index + "." + interval + "." + period, filename)

        # Ensure the file exists
        if not os.path.exists(json_file_path):
            return JsonResponse({"error": "File not found"}, status=404)

        # Open and read the JSON file
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        # Return the JSON response
        return JsonResponse(data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_news(request, index):
    try:
        dat = yf.Ticker(index)
        news = dat.get_news()
        if news.count == 0:
            return JsonResponse({"error": "No new found."}, status=404)

        # Return the JSON response
        return JsonResponse(news, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_history(request, index, start_date, end_date, interval):
    try:
        dat = yf.Ticker(index)
        hist = dat.history(start=start_date, end=end_date, interval=interval)
        hist = hist.sort_index() 

        if hist.empty:  # Corrected check for empty dataframe
            return JsonResponse({"error": "No history found."}, status=404)

        hist.reset_index(inplace=True)
        hist_json = hist.to_json(orient="records", date_format="iso")

        # Convert JSON string to Python object
        hist_data = json.loads(hist_json)

        return JsonResponse(hist_data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
