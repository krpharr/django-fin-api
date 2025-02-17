import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import Candlestick
import Pattern
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Process a string and an integer.")
    parser.add_argument("ticker_str_arg", type=str, help="Stock Ticker")
    parser.add_argument("chart_interval_str_arg", type=str, help="Chart Interval 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")
    parser.add_argument("period_str_arg", type=str, help="Period 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")

    args = parser.parse_args() 

    stock = yf.download(args.ticker_str_arg, 
                          interval=args.chart_interval_str_arg,
                          period=args.period_str_arg)
    
    # Check if the columns are multi-level (i.e., contain a "Ticker" level)
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.droplevel(0)  # Drop the first level (ticker name)

    
    # for testing
    # stock = yf.download("enph", 
    #                       interval='1d',
    #                       period='1mo')
    # chart_interval_str_arg = '5m'

    print(stock)

    candlesticks = []
    doji = Pattern.Doji()
    engulfing = Pattern.Engulfing()
    evening_star = Pattern.EveningStar()
    morning_star = Pattern.MorningStar()
    hanging_man = Pattern.HangingMan()
    hammer = Pattern.Hammer()
    invertedhammer = Pattern.InvertedHammer()
    shootingstar = Pattern.ShootingStar()
    upsidegaptwocrows = Pattern.UpsideGapTwoCrows()
    twocrows = Pattern.TwoCrows()
    threewhitesolders = Pattern.ThreeWhiteSolders()
    threeblackcrows = Pattern.ThreeBlackCrows()
    piercingline = Pattern.PiercingLine()
    darkcloudcover = Pattern.DarkCloudCover()
    spinningtop = Pattern.SpinningTop()
    marubozu = Pattern.Marubozu()
    harami = Pattern.Harami()
    haramicross = Pattern.HaramiCross()
    kicker = Pattern.Kicker()
    tweezers = Pattern.Tweezers()
    threeinside = Pattern.ThreeInside()
    threemethods = Pattern.ThreeMethods()
    neckline = Pattern.NeckLine()
    thrustingline = Pattern.ThrustingLine()
    gap = Pattern.Gap()
    abandonedbaby = Pattern.AbandonedBaby()
    belthold = Pattern.BeltHold()
    breakaway = Pattern.Breakaway()
    advanceblock = Pattern.AdvanceBlock()
    deliberation = Pattern.Deliberation()
    sticksandwich = Pattern.StickSandwich()
    tasukigap = Pattern.TasukiGap()
    sidebysidewhitelines = Pattern.SideBySideWhiteLines()
    threestars = Pattern.ThreeStars()
    threelinestrike = Pattern.ThreeLineStrike()
    uniquethreeriverbottom = Pattern.UniqueThreeRiverBottom()
    mathold = Pattern.MatHold()
    counterattacklines = Pattern.CounterattackLines()
    homingpigeon = Pattern.HomingPigeon()
    ladder = Pattern.Ladder()
    matching = Pattern.Matching()
    seperationglines = Pattern.SeperatingLines()
    tristar = Pattern.TriStar()
    # firstorderpivot = Pattern.FirstOrderPivot()
    # secondorderpivot = Pattern.SecondOrderPivot()
    # thirdorderpivot = Pattern.ThirdOrderPivot()
    spring = Pattern.Spring()

    # tests = [doji, engulfing, evening_star, morning_star, hanging_man, hammer, invertedhammer, shootingstar, upsidegaptwocrows,
    #       twocrows, threewhitesolders, threeblackcrows, piercingline, darkcloudcover, spinningtop, marubozu, harami, haramicross,
    #       kicker, tweezers, threeinside, threemethods, neckline, thrustingline, gap, abandonedbaby, belthold, breakaway, advanceblock, 
    #       deliberation, sticksandwich, tasukigap, sidebysidewhitelines, threestars, threelinestrike, uniquethreeriverbottom, mathold,
    #       counterattacklines, homingpigeon, ladder, matching, seperationglines, tristar, firstorderpivot, secondorderpivot, thirdorderpivot, spring]
    
    tests = [doji, engulfing, evening_star, morning_star, hanging_man, hammer, invertedhammer, shootingstar, upsidegaptwocrows,
          twocrows, threewhitesolders, threeblackcrows, piercingline, darkcloudcover, spinningtop, marubozu, harami, haramicross,
          kicker, tweezers, threeinside, threemethods, neckline, thrustingline, gap, abandonedbaby, belthold, breakaway, advanceblock, 
          deliberation, sticksandwich, tasukigap, sidebysidewhitelines, threestars, threelinestrike, uniquethreeriverbottom, mathold,
          counterattacklines, homingpigeon, ladder, matching, seperationglines, tristar, spring]

    # tests = [morning_star]
   
    all_results = []

    for i in stock.index:
        c = Candlestick.Candlestick(i, stock['Open'][i], stock['High'][i], stock['Low'][i], stock['Close'][i], stock['Volume'][i])
        candlesticks.append(c)
       
    # must be set to determine trend the candle is in.  Need to build a higher level class for apps to interact with.
    candlesticks[0].set_period_trends(candlesticks)
        
    for t in tests:
        results = t.get_matches(candlesticks)
        for r in results:
          all_results.append([r[1], r[0], r[2]])

    sorted_data = sorted(all_results, key=lambda x: x[0])

    bears = 0
    bulls = 0

    for r in sorted_data:
        if r[2] == 0:
            bears = bears + 1
        if r[2] == 1:
            bulls = bulls + 1
        print(f"{r[0]} {r[1]}")

    print(f"bull: {bulls}   bears: {bears}")

    # Convert `sorted_data` to a dictionary {date: [pattern1, pattern2, ...]}
    pattern_dict = {}
    for date, pattern, _ in sorted_data:  # Extract date and pattern name
        date_str = date.strftime('%Y-%m-%d')  # Convert Timestamp to string for indexing
        
        if date_str not in pattern_dict:
            pattern_dict[date_str] = []  # Initialize list if date is not present
        pattern_dict[date_str].append(pattern)  # Append pattern to list

    # Add a new column to the stock DataFrame
    stock["Patterns"] = stock.index.to_series().dt.strftime('%Y-%m-%d').apply(lambda date: ", ".join(pattern_dict.get(date, [])))

    print(stock)
    stock.reset_index(inplace=True)
    stock_json = stock.to_json(orient="records", date_format="iso", indent=4)

    print(stock_json)


if __name__ == "__main__":
    main()

