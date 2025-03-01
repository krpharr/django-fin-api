from django.urls import path
from .views import get_candles, get_json_list, get_json_file, get_news, get_history

urlpatterns = [
    path("candles/<str:ticker>/<str:timeframe>/<str:lookback>/", get_candles, name="candle-get"),
    path("json/<str:index>/<str:interval>/<str:period>/", get_json_list, name="json-get-list"),
    path("json/<str:index>/<str:interval>/<str:period>/<str:filename>/", get_json_file, name="json-get-file"),
    path("news/<str:index>/", get_news, name="news-get"),
    path("hist/<str:index>/<str:start_date>/<str:end_date>/<str:interval>/", get_history, name="hist-get-history")
]