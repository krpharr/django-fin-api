from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/alerts/", include("alerts.urls")),  # Alerts API
    path("api/fin/", include("fin.urls")),  # ✅ Ensure this matches the app name
]


