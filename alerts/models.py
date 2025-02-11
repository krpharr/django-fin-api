from django.db import models

from django.db import models

class Alert(models.Model):
    ticker = models.CharField(max_length=10)
    price_type = models.CharField(max_length=10, choices=[("open", "Open"), ("close", "Close"), ("high", "High"), ("low", "Low")])
    operator = models.CharField(max_length=2, choices=[(">=", "≥"), ("<=", "≤")])
    threshold = models.FloatField()
    alert_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} {self.operator} {self.threshold}"

