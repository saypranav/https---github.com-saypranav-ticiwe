from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
# from django.contrib.gis.db.models import Union
# from django.contrib.gis.geos import Point, Polygon
# from django.contrib.gis.measure import D

from geoapp import models

def pagination(request, data_object):
    offset = request.GET.get('offset') if 'offset' in request.GET else 10
    page = request.GET.get('page') if 'page' in request.GET else 1
    total_count = len(data_object)
    paginator = Paginator(data_object, int(offset))
    page_obj = paginator.get_page(int(page)) 
    return page_obj, total_count

@api_view(['GET', 'POST'])
def geo_locations(request):
#   template = loader.get_template('./geo.html')
#   return HttpResponse(template.render())
    if request.method == 'GET':
        values = models.geo_locations.objects.all().values('latitude','longitude','code','foglio','particella')
        return JsonResponse({'status':'success','response':f'{values}'})
    if request.method == 'POST':
        request_body = JSONParser().parse(request)
        latitude = request_body['latitude']
        longitude = request_body['longitude']
        models.geo_locations.objects.create(latitude=latitude,longitude=longitude)
        return JsonResponse({'status':'success','response':'saved'})

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

# # Enable spatial indexing for faster querying

# # Query to find locations within a certain distance of a given point
# nearby_locations = models.Location.objects.filter(coordinates__distance_lte=(point, D(m=1000)))

# # Perform a spatial union on all Area objects
# unioned_area = models.Area.objects.aggregate(union=Union('boundary'))['union']

# # Get a buffer of 100 meters around a location
# location = models.Location.objects.get(pk=1)
# buffered_location = location.coordinates.buffer(100)

# # Get the intersection of two areas
# area1 = models.Area.objects.get(pk=1)
# area2 = models.Area.objects.get(pk=2)
# intersection = area1.boundary.intersection(area2.boundary)