from django.urls import path
from .views import get_candles, get_custom_index_candles, get_json_list, get_json_file, get_news, get_history, get_point_and_figure, get_candles_hist, get_rsi_macd_hist

urlpatterns = [
    path("candles/<str:ticker>/<str:timeframe>/<str:lookback>/", get_candles, name="candle-get"),
    path("candles/custom-index/<str:tickers>/<str:timeframe>/<str:lookback>/", get_custom_index_candles, name="candle-get_custom_index"),
    path("json/<str:index>/<str:interval>/<str:period>/", get_json_list, name="json-get-list"),
    path("json/<str:index>/<str:interval>/<str:period>/<str:filename>/", get_json_file, name="json-get-file"),
    path("news/<str:index>/", get_news, name="news-get"),
    path("hist/<str:index>/<str:start_date>/<str:end_date>/<str:interval>/", get_history, name="hist-get-history"),
    path("hist/pf/<str:index>/<str:interval>/<str:period>/<str:reversal>/<str:start_date>/<str:end_date>/", get_point_and_figure, name="hist-get-point-and-figure"),
    path("hist/candles/<str:index>/<str:interval>/<str:period>/<str:start_date>/<str:end_date>/", get_candles_hist, name="hist-get-candles-hist"),
    path("hist/rsi-macd/<str:index>/<str:interval>/<str:period>/<str:start_date>/<str:end_date>/", get_rsi_macd_hist, name="hist-get-rsi-macd-hist")
]