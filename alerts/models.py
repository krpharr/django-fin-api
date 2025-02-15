from django.db import models

class Alert(models.Model):
    TREND_CHOICES = [
        ("Bullish", "Bullish"),
        ("Bearish", "Bearish"),
    ]

    LEVEL_CHOICES = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
    ]

    ticker = models.CharField(max_length=10)
    price_type = models.CharField(max_length=10, choices=[("open", "Open"), ("close", "Close"), ("high", "High"), ("low", "Low")])
    operator = models.CharField(max_length=2, choices=[(">=", "≥"), ("<=", "≤")])
    threshold = models.FloatField()
    alert_text = models.TextField(blank=True, null=True)
    trend = models.CharField(
        max_length=10,
        choices=TREND_CHOICES,
        default="Bullish"
    )
    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=3
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} {self.operator} {self.threshold} {self.trend} {self.level}"

