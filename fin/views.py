from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import yfinance as yf
import pandas as pd
import json
import math
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
from dateutil.relativedelta import relativedelta

def calc_candles(stock):
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

        return stock_json

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

        stock_json = calc_candles(stock)

        return JsonResponse(json.loads(stock_json), safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_candles_hist(request, index, interval, period, start_date, end_date):
    """
    Example URL: /api/fin/hist/candles/AAPL/1d/1mo/2024-03-01/2025-03-01/
    """
    try:
        dat = yf.Ticker(index)
        stock = dat.history(start=start_date, end=end_date, interval=interval, period=period)
        stock = stock.sort_index()  # Ensure data is sorted by date

        stock_json = calc_candles(stock)

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
        # base_dir = os.path.abspath(os.path.join(current_dir, "../../"))

        # production
        base_dir = os.path.abspath(os.path.join(current_dir, "../../testProj3"))


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
        # base_dir = os.path.abspath(os.path.join(current_dir, "../../"))

        # production
        base_dir = os.path.abspath(os.path.join(current_dir, "../../testProj3"))        

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
    
def get_previous_year(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")  # Convert string to datetime
    prev_year_date = date_obj - relativedelta(years=1)  # Subtract one year
    return prev_year_date.strftime("%Y-%m-%d")  # Convert back to string

def calculate_rsi(data, period=14):
    # Calculate the daily price changes
    delta = data['Close'].diff()

    # Separate the gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate the exponential moving average of gains and losses
    avg_gain = gain.ewm(span=period, min_periods=1, adjust=False).mean()
    avg_loss = loss.ewm(span=period, min_periods=1, adjust=False).mean()

    # Calculate the RS (Relative Strength)
    rs = avg_gain / avg_loss

    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calc_macd(data):
    k = data['Close'].ewm(span=3, adjust=False, min_periods=3).mean()
    d = data['Close'].ewm(span=10, adjust=False, min_periods=10).mean()
    macd = k - d
    macd_s = macd.ewm(span=16, adjust=False, min_periods=16).mean()
    data['MACD_3_10_16'] = data.index.map(macd)
    data['MACDs_3_10_16'] = data.index.map(macd_s)
    return data
    
@csrf_exempt
@require_http_methods(["GET"])
def get_rsi_macd_hist(request, index, interval, period, start_date, end_date):
    try:
        year_before = get_previous_year(start_date)
        dat = yf.Ticker(index)
        hist = dat.history(start=year_before, end=end_date, interval=interval)
        hist = hist.sort_index() 

        if hist.empty:  # Corrected check for empty dataframe
            return JsonResponse({"error": "No history found."}, status=404)

        hist.index = hist.index.strftime('%Y-%m-%d')
        hist.reset_index(inplace=True)

        hist['RSI'] = calculate_rsi(hist)
        hist = calc_macd(hist)

        hist_json = hist.to_json(orient="records", date_format="iso")

        # Convert JSON string to Python object
        hist_data = json.loads(hist_json)

        return JsonResponse(hist_data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_point_and_figure(request, index, interval, period, reversal, start_date, end_date):
    try:
        dat = yf.Ticker(index)
        if end_date != "" and start_date != "":
            stock = dat.history(start=start_date, end=end_date, interval=interval)
        else:
            stock = dat.history(interval=interval, period=period)

        data = stock.sort_index()
        stock = stock.sort_index() 

        print(stock)

        def calculate_box_size(price):
            if price >= 500:
                return 5
            if price >= 200 and price <= 500:
                return 4
            if price >= 100 and price <= 200:
                return 2
            if price <= 100:
                return 1


        def get_box_row(price):
            for i in range(len(array_key) - 1, -1, -1):
                if math.floor(price) >= array_key[i]:
                    return i

        def new_column(size):
            value = ' '
            array = [value] * size
            return array

        min_price = math.floor(data['Low'].min())
        max_price = math.floor(data['High'].max())
        min_base = min_price - calculate_box_size(min_price) * 5 
        max_base = max_price + calculate_box_size(max_price) * 5 

        reversal = int(reversal)
        window_size = 3
        highest_highs = data['High'].rolling(window=window_size).max()
        lowest_lows = data['Low'].rolling(window=window_size).min()
        current_trend = 'undefined'
        trends = []
        array_key = []
        dict_key = {}

        def print_chart():
            reversed_columns = []
            for c in columns:
                rc = c.copy()
                rc.reverse()
                reversed_columns.append(rc)

            rev_key = array_key.copy()
            rev_key.reverse()        
            str = ""
            csv_str = ""
            for i in range(0, len(rev_key)):
                s = f"{rev_key[i]}\t"
                cs = f"{rev_key[i]},"
                for j in range(0, len(reversed_columns)):
                    s += f"{reversed_columns[j][i]}"
                    cs += f"{reversed_columns[j][i]},"
                s += f"\t{rev_key[i]}\n"
                cs += f"{rev_key[i]}\n"
                str += s
                csv_str += cs

            print(str)
            return str

        n = min_base
        i = 0

        while n < max_base:
            size = calculate_box_size(n)
            dict_key[n] = i
            array_key.append(n)
            n = n + size
            i = i + 1

        box_rows = []

        for i in range(len(data)):    
            if i < 1:
                box_rows.append(get_box_row(data['Close'].iloc[i]))
            else:
                if data['High'].iloc[i] > highest_highs.iloc[i - 1]:
                    box_rows.append(get_box_row(data['High'].iloc[i]))
                elif data['Low'].iloc[i] < lowest_lows.iloc[i - 1]:
                    box_rows.append(get_box_row(data['Low'].iloc[i]))
                else:
                    box_rows.append(get_box_row(data['Close'].iloc[i]))
                    
        data['box_row'] = box_rows

        last_box = 0
        for i in range(len(data)):
            if i < 1:
                trends.append(current_trend)
                last_box = data['box_row'].iloc[i]
            else:
                if data['box_row'].iloc[i] > last_box:
                    new_trend = 'up'
                elif data['box_row'].iloc[i] < last_box:
                    new_trend = 'down'
                else:
                    new_trend = 'sideways'
                if new_trend != current_trend:
                    current_trend = new_trend
                trends.append(current_trend)
                last_box = data['box_row'].iloc[i]
                
        data['trend'] = trends

        col = 0
        col_trend = -1
        columns = [new_column(len(array_key))]
        last_box = None
        #print(data.head())
        for index, row in data.iterrows():
            trend = row['trend']
            box_row = row['box_row']
            if last_box == None:
                last_box = box_row
            #print(f"Index: {index}, trend: {trend}, Box row: {box_row} ${array_key[box_row]}")
            if trend == 'up':
                if col_trend == -1:
                    col_trend = 1
                if col_trend == 0 and box_row - last_box >= reversal:
                    col += 1
                    col_trend = 1
                    a = new_column(len(array_key))
                    columns.append(a)
                    last_box += 1
                if col_trend == 1:
                    #fill in last_box to box_row with x's
                    for i in range(last_box, box_row + 1):
                        columns[col][i] = 'X'
                        last_box = box_row
            if trend == 'down':
                if col_trend == -1:
                    col_trend = 0
                if col_trend == 1 and last_box - box_row >= reversal:
                    col += 1
                    col_trend = 0
                    a = new_column(len(array_key))
                    columns.append(a)
                    last_box -= 1
                if col_trend == 0:
                    #fill in last_box to box_row with o's
                    for i in range(box_row, last_box + 1):
                        columns[col][i] = 'O'
                        last_box = box_row

        pf_str = print_chart()

        return JsonResponse(pf_str, safe=False, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)