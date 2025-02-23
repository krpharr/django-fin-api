from django.urls import path
from .views import get_alerts, get_triggered_alerts, add_alert, delete_alert, update_alert

urlpatterns = [
    path("", get_alerts, name="get_alerts"),
    path("add/", add_alert, name="add_alert"),
    path("delete/<int:alert_id>/", delete_alert, name="delete_alert"),
    path("update/<int:alert_id>/", update_alert, name="update_alert"),
    path("triggered/", get_triggered_alerts, name="get_triggered_alerts"),
]
