from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("ticker", "price_type", "operator", "threshold", "created_at")
    search_fields = ("ticker", "alert_text")
    list_filter = ("price_type", "operator", "created_at")
    ordering = ("ticker", "created_at")

