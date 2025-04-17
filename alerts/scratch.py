import math
import yfinance as yf
import webbrowser
import csv
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Process a string and an integer.")
    parser.add_argument("ticker", type=str, help="Stock Ticker")
    parser.add_argument("interval", type=str, help="Chart Interval 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")
    parser.add_argument("period", type=str, help="Period 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")
    parser.add_argument("reversal", type=str, help="1, 2, 3, 5")
    parser.add_argument("start_date", type=str, nargs='?', default=None, help="Start date (optional, format: YYYY-MM-DD)")
    parser.add_argument("end_date", type=str, nargs='?', default=None, help="End date (optional, format: YYYY-MM-DD)")

    args = parser.parse_args() 


    dat = yf.Ticker(args.ticker)
    if args.end_date != None and args.start_date != None:
        stock = dat.history(start=args.start_date, end=args.end_date, interval=args.interval)
    else:
        stock = dat.history(interval=args.interval, period=args.period)

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

    reversal = int(args.reversal)
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

    print_chart()

if __name__ == "__main__":
    main()