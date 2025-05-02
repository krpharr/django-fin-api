from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Alert
from .utils import get_latest_price  # ✅ Import the function


@csrf_exempt
@require_http_methods(["GET"])
def get_alerts(request):
    period = request.GET.get("period", "5m")  # Default to "5m" if not provided
    alerts = Alert.objects.all().order_by("ticker")

    for alert in alerts:
        alert.latest_price = get_latest_price(alert.ticker, period, alert.value_type)  # ✅ Now it works

    return JsonResponse(list(alerts.values()), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def add_alert(request):
    try:
        data = json.loads(request.body)
        alert = Alert.objects.create(
            ticker=data["ticker"],
            price_type=data["price_type"],
            operator=data["operator"],
            threshold=data["threshold"],
            trend=data["trend"],
            level=data["level"],
            alert_text=data.get("alert_text", "No additional info")
        )
        return JsonResponse({"message": "Alert added", "id": alert.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_alert(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        data = json.loads(request.body)
        
        # Update the fields if they are provided in the request body
        alert.ticker = data.get("ticker", alert.ticker)
        alert.value_type = data.get("price_type", alert.value_type)
        alert.operator = data.get("operator", alert.operator)
        alert.threshold = data.get("threshold", alert.threshold)
        alert.trend = data.get("trend", alert.trend)
        alert.level = data.get("level", alert.level)
        alert.alert_text = data.get("alert_text", alert.alert_text)
        
        alert.save()
        return JsonResponse({"message": "Alert updated", "id": alert.id}, status=200)
    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_alert(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.delete()
        return JsonResponse({"message": "Alert deleted"}, status=200)
    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert not found"}, status=404)

@csrf_exempt
@require_http_methods(["GET"])
def get_triggered_alerts(request):
    interval = request.GET.get("interval", "5m")  # Default to 5m
    alerts = Alert.objects.all().all().order_by("ticker")
    triggered_alerts = []

    for alert in alerts:
        latest_price = get_latest_price(alert.ticker, interval)
        if latest_price is not None:
            if (alert.operator == ">=" and latest_price >= alert.threshold) or \
               (alert.operator == "<=" and latest_price <= alert.threshold):
                triggered_alerts.append({
                    "id": alert.id,
                    "ticker": alert.ticker,
                    "price_type": alert.value_type,
                    "operator": alert.operator,
                    "threshold": alert.threshold,
                    "current_price": latest_price,
                    "alert_text": alert.alert_text,
                    "trend": alert.trend,
                    "level": alert.level
                })

    return JsonResponse(triggered_alerts, safe=False)

