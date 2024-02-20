from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import pytz
from calendario.models import Events

def calendario(request):
    all_events = Events.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'calendario.html', context)

def all_events(request):
    all_events = Events.objects.all()
    out = []
    local_timezone = pytz.timezone('America/Mexico_City') 
    for event in all_events:
        start_local = event.start.astimezone(local_timezone)
        end_local = event.end.astimezone(local_timezone)
        out.append({
            'title': event.name,
            'id': event.id,
            'start': start_local.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': end_local.strftime("%Y-%m-%dT%H:%M:%S"),
        })
    return JsonResponse(out, safe=False)

def add_event(request):
    title = request.GET.get("title", None)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    local_timezone = pytz.timezone('America/Mexico_City')  
    start_local = timezone.datetime.fromisoformat(start).astimezone(local_timezone)
    end_local = timezone.datetime.fromisoformat(end).astimezone(local_timezone)
    event = Events(name=str(title), start=start_local, end=end_local)
    event.save()
    data = {}
    return JsonResponse(data)

def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)
