from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from geoapp import models

def pagination(request, data_object):
        offset = request.GET.get('offset') if 'offset' in request.GET else 10
        page = request.GET.get('page') if 'page' in request.GET else 1
        total_count = len(data_object)
        paginator = Paginator(data_object, int(offset))
        page_obj = paginator.get_page(int(page)) 
        return page_obj, total_count

def geo_locations(request):
#   template = loader.get_template('./geo.html')
#   return HttpResponse(template.render())
    values = models.geo_locations.objects.all().values('latitude','longitude','code','foglio','p4')
    return JsonResponse({'status':'success','response':f'{values}'})

def tasks(request):
    type = request.GET.get('type') if 'type' in request.GET else None
    active = request.GET.get('active') if 'active' in request.GET else None
    tasks_obj = models.tasks.objects
    if active:
        tasks_obj.filter(is_enabled=True)
    if type:
        tasks_obj.filter(type=type)
    records = tasks_obj.values('type','description','start_date','end_date')
    # data = pagination(request,records)
    return JsonResponse({'status':'success','response':f'{records}'})

def notes(request):
    type = request.GET.get('type') if 'type' in request.GET else None
    active = request.GET.get('active') if 'active' in request.GET else None
    tasks_obj = models.notes.objects
    if active:
        tasks_obj.filter(is_enabled=True)
    if type:
        tasks_obj.filter(type=type)
    records = tasks_obj.values('type','notes','created_by_user_id','added_date')
    data = pagination(request,records)
    return JsonResponse({'status':'success','response':f'{data}'})