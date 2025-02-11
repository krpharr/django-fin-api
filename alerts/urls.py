from django.urls import path
from .views import get_alerts, get_triggered_alerts, add_alert, delete_alert



urlpatterns = [
    path("alerts/", get_alerts, name="get_alerts"),
    path("alerts/add/", add_alert, name="add_alert"),
    path("alerts/delete/<int:alert_id>/", delete_alert, name="delete_alert"),
    path("alerts/triggered/", get_triggered_alerts, name="get_triggered_alerts"),
]
