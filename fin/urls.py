from django.urls import path
from .views import get_candles

urlpatterns = [
    path("candles/<str:ticker>/<str:timeframe>/<str:lookback>/", get_candles, name="candle-get"),
]