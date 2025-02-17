from django.db import models

class Candle(models.Model):
    date = models.DateTimeField()  # Store date as DateTime
    open_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_price = models.DecimalField(max_digits=10, decimal_places=4)
    low_price = models.DecimalField(max_digits=10, decimal_places=4)
    close_price = models.DecimalField(max_digits=10, decimal_places=4)
    adj_close = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.BigIntegerField()  # Large numbers for volume
    patterns = models.TextField(blank=True)  # Optional string patterns

    def __str__(self):
        return f"{self.date} - Open: {self.open_price}, Close: {self.close_price}"


