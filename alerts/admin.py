from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("ticker", "value_type", "operator", "threshold", "trend", "level", "created_at")
    search_fields = ("ticker", "alert_text", "trend")
    list_filter = ("value_type", "operator", "trend", "level", "created_at")
    ordering = ("ticker", "created_at")

