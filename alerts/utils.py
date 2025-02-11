import yfinance as yf

def get_latest_price(ticker, period="5m", price_type="Close"):
    try:
        stock = yf.Ticker(ticker)
        latest_price = stock.history(interval=period, period="1d")[price_type].iloc[-1]
        return round(latest_price, 2)
    except Exception:
        return None
