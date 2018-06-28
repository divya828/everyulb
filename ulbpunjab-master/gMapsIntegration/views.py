from django.shortcuts import render
from django.contrib.auth import (login,authenticate,get_user_model)
from .key import key
import requests
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import json
import geopy
from geopy.distance import vincenty
import re
from .models import Water, Landfills, Wells, Highway, Rivers, Airports, LandfillsExtra, LandfillsImages, LandfillConceptualModel, LandfillSample, LandfillSampleComments, LandfillProtocolComments, LandfillSampleData, LandfillForm1, LandfillForm4, States, Districts, LandfillsFinalSiteConceptualModel, LandfillsBaselineDataModel
from .forms import UserLoginForm,WaterForm, WellsForm, HighwayForm, RiversForm, AirportsForm, LandfillsForm, LandfillsExtraForm, LandfillsImagesForm, LandfillConceptualModelForm, LandfillSampleForm, LandfillSampleCommentsForm, LandfillProtocolCommentsForm, LandfillSampleDataForm, LandfillForm1Form, LandfillForm4Form, LandfillsFinalSiteConceptualModelForm, LandfillsBaselineDataModelForm
import math
import logging
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import serializers

#API URLS
# places_nearbysearch_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
# places_textsearch_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
# places_details_url = "https://maps.googleapis.com/maps/api/place/details/json"
# roads_nearestroads_url = "https://roads.googleapis.com/v1/nearestRoads"
geocode_reverse_url = "https://maps.googleapis.com/maps/api/geocode/json"

# logger = logging.getLogger(__name__)
# logger.error(your_variable)
def login_view(request):
    title='Login'
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
    return render(request,'gMapsIntegration/templates/form.html',{'form':form,'title':title})

def landfilladd(request):

    latitude = 26.193113
    longitude = 91.700108

    location = str(latitude) + "," + str(longitude)
    location = ''.join(location.split())

    name = ""
    area = 1

    if request.method == 'POST':
        location = str(request.POST['latlng'])
        location = ''.join(location.split())
        latitude = re.split(',', location)[0]
        longitude = re.split(',', location)[1]
        name = request.POST.get('name', "unnamed")
        area = round(float(request.POST['area']), 3)

    location = ''.join(location.split())

    nearestAirport1 = nearestAirport(location)
    nearestRoads1 = nearestHighway(location)
    nearestWater1 = nearestWater(location)
    nearestWell1 = nearestWell(location)
    nearestRiver1 = nearestRiver(location)
    state_district1 = state_district(location)

    json_in = {"latitude":latitude, "longitude":longitude, "distance_airport": nearestAirport1["distance"], "airport_name": nearestAirport1["name"], "distance_river": nearestRiver1["distance"], "river_name": nearestRiver1["name"], "distance_road": nearestRoads1["distance"], "road_name": nearestRoads1["name"], "distance_water": nearestWater1, "distance_well": nearestWell1, "state": state_district1["state"], "district": state_district1["district"], "area": area}

    if request.method == 'POST':
        if request.POST["button"] == 'ajax_request':
            return JsonResponse(json_in)
        elif request.POST["button"] == 'landfill':
            lf = add_landfill(location, area, name, json_in)
            lf_obj = Landfills.objects.get(pk=lf)
            landfill_extra_form = LandfillsExtraForm(data={"distance_water": float(nearestWater1), "area": float(area)/10000, "distance_airport": float(nearestAirport1["distance"])/1000, "distance_water_body": float(nearestRiver1["distance"])})
            if landfill_extra_form.is_valid():
                new_extra = landfill_extra_form.save(commit = False)
                new_extra.landfill = lf_obj
                new_extra.save()
            create_samples_data(lf_obj, area)

            LandfillsFinalSiteConceptualModel_form = LandfillsFinalSiteConceptualModel(landfill=lf_obj)
            LandfillsFinalSiteConceptualModel_form.save()
            LandfillsBaselineDataModel_form = LandfillsBaselineDataModel(landfill=lf_obj)
            LandfillsBaselineDataModel_form.save()

    return render(request, 'gMapsIntegration/landfilladd.html', {"key": key, "airport": nearestAirport1["name"], "airport_distance": nearestAirport1["distance"], "roads_distance": nearestRoads1["distance"], "latitude": latitude, "longitude": longitude, "roads": nearestRoads1["name"], "water_distance": nearestWater1, "water_well_distance": nearestWell1, "river_distance": nearestRiver1["distance"], "river_name": nearestRiver1["name"], "state": state_district1["state"], "district": state_district1["district"]})

#distance between two locations in degrees output in meteres
def distance(one, two):
    return vincenty(one, two).meters

def nearestWater(one):
    water = Water.objects.all()
    distance_min = float('inf')
    for x in water:
        lat = x.latitude
        lng = x.longitude
        latlng1 = str(lat) + ',' + str(lng)
        distance_between = distance(one, latlng1)
        if(distance_min > distance_between):
            distance_min = distance_between

    return round(distance_min, 3)

def nearestWell(one):
    wells = Wells.objects.all()
    distance_min = float('inf')
    for x in wells:
        lat = x.latitude
        lng = x.longitude
        latlng1 = str(lat) + ',' + str(lng)
        distance_between = distance(one, latlng1)
        if(distance_min > distance_between):
            distance_min = distance_between

    return round(distance_min, 3)


def nearestHighway(one):
    highway = Highway.objects.all()
    distance_min = float('inf')
    name = ""
    for x in highway:
        lat = x.latitude
        lng = x.longitude
        latlng1 = str(lat) + ',' + str(lng)
        distance_between = distance(one, latlng1)
        if(distance_min > distance_between):
            distance_min = distance_between
            name = x.name

    out_json = {"distance": round(distance_min, 3), "name": name}
    return out_json

def nearestRiver(one):
    river = Rivers.objects.all()
    distance_min = float('inf')
    name = ""
    for x in river:
        lat = x.latitude
        lng = x.longitude
        latlng1 = str(lat) + ',' + str(lng)
        distance_between = distance(one, latlng1)
        if(distance_min > distance_between):
            distance_min = distance_between
            name = x.name

    out_json = {"distance": round(distance_min, 3), "name": name}
    return out_json

def nearestAirport(one):
    airport = Airports.objects.all()
    distance_min = float('inf')
    name = ""
    for x in airport:
        lat = x.latitude
        lng = x.longitude
        latlng1 = str(lat) + ',' + str(lng)
        distance_between = distance(one, latlng1)
        if(distance_min > distance_between):
            distance_min = distance_between
            name = x.name

    out_json = {"distance": round(distance_min, 3), "name": name}
    return out_json

def state_district(one):

    geocode_payload = {"key": key, "latlng": one, "result_type": "administrative_area_level_1|administrative_area_level_2"}
    geocode_request = requests.get(geocode_reverse_url, params=geocode_payload)
    geocode_json = geocode_request.json()
    district = geocode_json["results"][0]["address_components"][0]["long_name"]
    state = geocode_json["results"][0]["address_components"][1]["long_name"]
    # logger = logging.getLogger(__name__)
    # logger.error(district)
    state_district1 = {"state": state ,"district": district}
    return state_district1

#The data page, where the latlan coordinates are given and it adds data to the database
def add_data(request):
    if request.method == 'POST':
        if request.POST["button"] == "water":
            latlan = request.POST['latlng']
            area = request.POST['area']
            add_water(latlan, area)
        elif request.POST["button"] == "well":
            latlan = request.POST['latlng']
            area = request.POST['area']
            add_well(latlan, area)
        elif request.POST["button"] == "airport":
            latlan = request.POST['latlng']
            area = request.POST['area']
            name = request.POST['name']
            add_airport(latlan, area, name)
        elif request.POST["button"] == "highway":
            latlan = request.POST['latlng']
            area = request.POST['area']
            name = request.POST['name']
            add_highway(latlan, area, name)
        elif request.POST["button"] == "river":
            latlan = request.POST['latlng']
            area = request.POST['area']
            name = request.POST['name']
            add_river(latlan, area, name)
    return render(request, 'gMapsIntegration/add_data.html', {"key": key})

def add_water(latlan, area):
    location = str(latlan)
    location = ''.join(location.split())
    latitude = re.split(',', location)[0]
    longitude = re.split(',', location)[1]
    water_form = WaterForm(data={"latitude": float(latitude), "longitude": float(longitude), "area": float(area)})
    if(water_form.is_valid()):
        new_postz = water_form.save(commit = False)
        new_postz.save()

    landfills = Landfills.objects.all()
    for x in landfills:
        latitude = x.latitude
        longitude = x.longitude
        landfill_loc = str(latitude) + ',' + str(longitude)
        x.distance_water = nearestWater(landfill_loc)
        x.save()

def add_well(latlan, area):
    location = str(latlan)
    location = ''.join(location.split())
    latitude = re.split(',', location)[0]
    longitude = re.split(',', location)[1]
    well_form = WellsForm(data={"latitude": float(latitude), "longitude": float(longitude), "area": float(area)})
    if(well_form.is_valid()):
        new_postz = well_form.save(commit = False)
        new_postz.save()

    landfills = Landfills.objects.all()
    for x in landfills:
        latitude = x.latitude
        longitude = x.longitude
        landfill_loc = str(latitude) + ',' + str(longitude)
        x.distance_well = nearestWell(landfill_loc)
        x.save()

def add_airport(latlan, area, name):
    location = str(latlan)
    location = ''.join(location.split())
    latitude = re.split(',', location)[0]
    longitude = re.split(',', location)[1]
    airport_form = AirportsForm(data={"latitude": float(latitude), "longitude": float(longitude), "area": float(area), "name": name})
    if(airport_form.is_valid()):
        new_postz = airport_form.save()

    landfills = Landfills.objects.all()
    for x in landfills:
        latitude = x.latitude
        longitude = x.longitude
        landfill_loc = str(latitude) + ',' + str(longitude)
        nearestAirport1 = nearestAirport(landfill_loc)
        x.distance_airport = nearestAirport1["distance"]
        x.airport_name = nearestAirport1["name"]
        x.save()

def add_river(latlan, area, name):
    location = str(latlan)
    location = ''.join(location.split())
    latitude = re.split(',', location)[0]
    longitude = re.split(',', location)[1]
    river_form = RiversForm(data={"latitude": float(latitude), "longitude": float(longitude), "area": float(area), "name": name})
    if(river_form.is_valid()):
        new_postz = river_form.save()

    landfills = Landfills.objects.all()
    for x in landfills:
        latitude = x.latitude
        longitude = x.longitude
        landfill_loc = str(latitude) + ',' + str(longitude)
        nearestRiver1 = nearestRiver(landfill_loc)
        x.distance_river = nearestRiver["distance"]
        x.road_name = nearestRiver1["name"]
        x.save()

def add_highway(latlan, area, name):
    location = str(latlan)
    location = ''.join(location.split())
    latitude = re.split(',', location)[0]
    longitude = re.split(',', location)[1]
    highway_form = HighwayForm(data={"latitude": float(latitude), "longitude": float(longitude), "area": float(area), "name": name})
    if(highway_form.is_valid()):
        new_postz = highway_form.save()

    landfills = Landfills.objects.all()
    for x in landfills:
        latitude = x.latitude
        longitude = x.longitude
        landfill_loc = str(latitude) + ',' + str(longitude)
        nearestHighway1 = nearestHighway(landfill_loc)
        x.distance_road = nearestHighway1["distance"]
        x.road_name = nearestHighway1["name"]
        x.save()

def add_landfill(latlan, area, name, json_in):
    location = str(latlan)
    location = ''.join(location.split())
    latitude = re.split(',', location)[0]
    longitude = re.split(',', location)[1]
    landfill_form = LandfillsForm(data={"latitude": float(latitude), "longitude": float(longitude), "area": float(area), "name": name, "distance_airport": float(json_in["distance_airport"]), "distance_water": float(json_in["distance_water"]), "distance_well": float(json_in["distance_well"]), "distance_road": float(json_in["distance_road"]), "distance_river": float(json_in["distance_river"]), "road_name": json_in["road_name"], "airport_name": json_in["airport_name"], "river_name": json_in["river_name"]})
    # logger = logging.getLogger(__name__)
    # logger.error(YOLO)
    if(landfill_form.is_valid()):
        new_postz = landfill_form.save(commit = False)
        current_state = States.objects.get(state=json_in["state"])
        current_district = current_state.districts.get(district=json_in["district"])
        new_postz.district = current_district
        new_postz.save()
        return new_postz.id


def details(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    add_more_cpy = edit_add_more_copy(ids)
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    x = landfill.landfill_conceptual_model.all()
    amount_of_subarea_area = round(float(landfill.area)/10000, 4)
    amount_of_subarea = 2*math.sqrt(float(landfill.area)/10000)
    amount_of_drillings = int(round(6*amount_of_subarea, 0))
    completed0 = landfill.landfill_sample.filter(sample_type = 0).filter(completed = 1).count()
    completed1 = landfill.landfill_sample.filter(sample_type = 1).filter(completed = 1).count()
    completed2 = landfill.landfill_sample.filter(sample_type = 2).filter(completed = 1).count()
    completed3 = landfill.landfill_sample.filter(sample_type = 3).filter(completed = 1).count()

    landfill.area = round(landfill.area, 2)

    completed = {"c0": completed0, "c1": completed1, "c2": completed2, "c3": completed3, "c00": round(100*completed0/amount_of_drillings, 2), "c11": round(100*completed1/amount_of_drillings, 2), "c22": round(100*completed2/amount_of_drillings, 2), "c33": round(100*completed3/amount_of_drillings, 2)}

    landfill_final_site_conceptual_model_send = landfill.landfill_final_site_conceptual_model.all()[0]
    landfill_landfill_baseline_data_model_send = landfill.landfill_baseline_data.all()[0]

    return render(request, 'gMapsIntegration/details.html', {"key": key, "landfill": landfill, "details_extra": add_more_cpy["details_extra"], "sen": add_more_cpy["sen"], "score": add_more_cpy["score"], "states": states, "districts": districts, "amount_of_drillings": amount_of_drillings, "completed": completed, "site_concep": landfill_final_site_conceptual_model_send, "baselinedata": landfill_landfill_baseline_data_model_send})

def home(request):
    landfills = Landfills.objects.all()
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/home.html', {"key": key, "landfills": landfills, "states": states, "districts": districts})

def search(request):
    results = request.POST.get('search')
    list_landfill = Landfills.objects.filter(name__icontains=results).all()
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/search.html', {"key": key, 'landfills': list_landfill, 'search':results, "districts": districts, "states": states})

def grtr(weight, data, one, two ,three, four):
    if(data>two and data<=one):
        x1 = data - two;
        x2= one - two;
        sens = 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data > three and data <= two):
        x1 = data - three;
        x2= two - three;
        sens = 0.25 + 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data > four and data <= three):
        x1 = data - four;
        x2= three - four;
        sens = 0.5 + 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data <= four):
        x1 = data;
        x2= four;
        sens = 0.75 + 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif (data > one):
        sens = 0
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}


def lsr(weight, data, one, two ,three, four):
    if(data>three and data<=four):
        x1 = data - three;
        x2= four - three;
        sens = 0.75 + 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data > two and data <= three):
        x1 = data - two;
        x2= three - two;
        sens = 0.5 + 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data > one and data <= two):
        x1 = data - one;
        x2= two - one;
        sens = 0.25 + 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data <= one):
        x1 = data;
        x2= one;
        sens = 0.25*(x1/x2)
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}
    elif(data > four):
        sens = 1
        return {"score": round(weight*sens, 3) ,"sensitivity": round(sens, 3)}

def add_more(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    # The details pertaining to landfill
    x = landfill.landfill_extra.all()[0]
    #sensitivity index
    distance_water = grtr(69, float(x.distance_water), 10000, 5000, 2500, 1000)
    depth_waste = lsr(64, float(x.depth_waste), 3, 10, 20, 100)
    area = lsr(61, float(x.area), 5, 10, 20, 100)
    groundwater_depth = grtr(54, float(x.groundwater_depth), 100, 20, 10, 3)
    soil_perm = lsr(54, float(x.soil_perm), 0.1, 1, 10, 100)
    groundwater_quality = {"score": 50*float(x.groundwater_quality)/4, "sensitivity": float(x.groundwater_quality)/4}
    distance_habitat = grtr(46, float(x.distance_habitat), 100, 25, 10, 5)
    distance_airport = grtr(46, float(x.distance_airport), 100, 20, 10, 5)
    distance_water_body = grtr(41, float(x.distance_water_body), 10000, 8000, 1500, 500)
    type_soil = grtr(41, float(x.type_soil), 100, 50, 30, 15)
    life_future = lsr(36, float(x.life_future), 5, 10, 20, 100)
    waste_type = {"score": 30*float(x.waste_type)/4, "sensitivity": float(x.waste_type)/4}
    waste_quantity_site = lsr(30, float(x.waste_quantity_site), 10000, 100000, 1000000, 10000000)
    waste_quantity_disposed = lsr(24, float(x.waste_quantity_disposed), 250, 500, 1000, 10000)
    distance_village = grtr(21, float(x.distance_village), 10000, 1000, 600, 300)
    flood = grtr(16, float(x.flood), 1000, 100, 30, 10)
    rainfall_annual = lsr(11, float(x.rainfall_annual), 25, 125, 250, 10000)
    distance_city = lsr(7, float(x.distance_city), 100, 20, 10, 5)
    public_acceptance = {"score": 7*float(x.public_acceptance)/4, "sensitivity": float(x.public_acceptance)/4}
    ambient_air = lsr(3, float(x.ambient_air), 0.01, 0.05, 0.1, 100)
    waste_hazard = lsr(71, float(x.waste_hazard), 10, 20, 30, 100)
    biodegradable_waste = lsr(71, float(x.biodegradable_waste), 10, 30, 60, 100)
    age_filing = grtr(58, float(x.age_filing), 100, 30, 20, 10)
    waste_moisture = lsr(71, float(x.waste_moisture), 10, 20, 40, 100)
    bod = lsr(36, float(x.bod), 30, 60, 100, 1000)
    cod = lsr(19, float(x.cod), 250, 350, 500, 10000)
    tds = lsr(13, float(x.tds), 2100, 3000, 4000, 10000)

    sen_index = {"distance_water": distance_water,
    "depth_waste": depth_waste,
    "area": area,
    "groundwater_depth": groundwater_depth,
    "soil_perm": soil_perm,
    "groundwater_quality": groundwater_quality,
    "distance_habitat": distance_habitat,
    "distance_airport": distance_airport,
    "distance_water_body": distance_water_body,
    "type_soil": type_soil,
    "life_future": life_future,
    "waste_type": waste_type,
    "waste_quantity_site": waste_quantity_site,
    "waste_quantity_disposed": waste_quantity_disposed,
    "distance_village": distance_village,
    "flood": flood,
    "rainfall_annual": rainfall_annual,
    "distance_city": distance_city,
    "public_acceptance": public_acceptance,
    "ambient_air": ambient_air,
    "waste_hazard": waste_hazard,
    "biodegradable_waste": biodegradable_waste,
    "age_filing": age_filing,
    "waste_moisture": waste_moisture,
    "bod": bod,
    "cod": cod,
    "tds": tds}


    score = distance_water["score"] + depth_waste["score"] + area["score"] + groundwater_depth["score"] + soil_perm["score"] + groundwater_quality["score"] + distance_habitat["score"] + distance_airport["score"] + distance_water_body["score"] + type_soil["score"] + life_future["score"] + waste_type["score"] + waste_quantity_site["score"] + waste_quantity_disposed["score"] + distance_village["score"] + flood["score"] + rainfall_annual["score"] + distance_city["score"] + public_acceptance["score"] + ambient_air["score"] +  waste_hazard["score"] + biodegradable_waste["score"] + age_filing["score"] + waste_moisture["score"] + bod["score"] + cod["score"] + tds["score"]

    return render(request, 'gMapsIntegration/add_more.html', {"key": key, "details_extra": x, "sen": sen_index, "score": score})

def edit_add_more(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    # The details pertaining to landfill
    x = landfill.landfill_extra.all()[0]
    if request.method == 'POST':
        x.distance_water = request.POST['distance_water']
        x.depth_waste = request.POST['depth_waste']
        x.area = request.POST['area']
        x.groundwater_depth = request.POST['groundwater_depth']
        x.soil_perm = request.POST['soil_perm']
        x.groundwater_quality = request.POST['groundwater_quality']
        x.distance_habitat = request.POST['distance_habitat']
        x.distance_airport = request.POST['distance_airport']
        x.distance_water_body = request.POST['distance_water_body']
        x.type_soil = request.POST['type_soil']
        x.life_future = request.POST['life_future']
        x.waste_type = request.POST['waste_type']
        x.waste_quantity_site = request.POST['waste_quantity_site']
        x.waste_quantity_disposed = request.POST['waste_quantity_disposed']
        x.distance_village = request.POST['distance_village']
        x.flood = request.POST['flood']
        x.rainfall_annual = request.POST['rainfall_annual']
        x.distance_city = request.POST['distance_city']
        x.public_acceptance = request.POST['public_acceptance']
        x.ambient_air = request.POST['ambient_air']
        x.waste_hazard = request.POST['waste_hazard']
        x.biodegradable_waste = request.POST['biodegradable_waste']
        x.age_filing = request.POST['age_filing']
        x.waste_moisture = request.POST['waste_moisture']
        x.bod = request.POST['bod']
        x.cod = request.POST['cod']
        x.tds = request.POST['tds']
        x.save()
        return HttpResponseRedirect(reverse('details', kwargs={'ids': ids}))
    #sensitivity index
    distance_water = grtr(69, float(x.distance_water), 10000, 5000, 2500, 1000)
    depth_waste = lsr(64, float(x.depth_waste), 3, 10, 20, 100)
    area = lsr(61, float(x.area), 5, 10, 20, 100)
    groundwater_depth = grtr(54, float(x.groundwater_depth), 100, 20, 10, 3)
    soil_perm = lsr(54, float(x.soil_perm), 0.1, 1, 10, 100)
    groundwater_quality = {"score": 50*float(x.groundwater_quality)/4, "sensitivity": float(x.groundwater_quality)/4}
    distance_habitat = grtr(46, float(x.distance_habitat), 100, 25, 10, 5)
    distance_airport = grtr(46, float(x.distance_airport), 100, 20, 10, 5)
    distance_water_body = grtr(41, float(x.distance_water_body), 10000, 8000, 1500, 500)
    type_soil = grtr(41, float(x.type_soil), 100, 50, 30, 15)
    life_future = lsr(36, float(x.life_future), 5, 10, 20, 100)
    waste_type = {"score": 30*float(x.waste_type)/4, "sensitivity": float(x.waste_type)/4}
    waste_quantity_site = lsr(30, float(x.waste_quantity_site), 10000, 100000, 1000000, 10000000)
    waste_quantity_disposed = lsr(24, float(x.waste_quantity_disposed), 250, 500, 1000, 10000)
    distance_village = grtr(21, float(x.distance_village), 10000, 1000, 600, 300)
    flood = grtr(16, float(x.flood), 1000, 100, 30, 10)
    rainfall_annual = lsr(11, float(x.rainfall_annual), 25, 125, 250, 10000)
    distance_city = lsr(7, float(x.distance_city), 100, 20, 10, 5)
    public_acceptance = {"score": 7*float(x.public_acceptance)/4, "sensitivity": float(x.public_acceptance)/4}
    ambient_air = lsr(3, float(x.ambient_air), 0.01, 0.05, 0.1, 100)
    waste_hazard = lsr(71, float(x.waste_hazard), 10, 20, 30, 100)
    biodegradable_waste = lsr(71, float(x.biodegradable_waste), 10, 30, 60, 100)
    age_filing = grtr(58, float(x.age_filing), 100, 30, 20, 10)
    waste_moisture = lsr(71, float(x.waste_moisture), 10, 20, 40, 100)
    bod = lsr(36, float(x.bod), 30, 60, 100, 1000)
    cod = lsr(19, float(x.cod), 250, 350, 500, 10000)
    tds = lsr(13, float(x.tds), 2100, 3000, 4000, 10000)

    sen_index = {"distance_water": distance_water,
    "depth_waste": depth_waste,
    "area": area,
    "groundwater_depth": groundwater_depth,
    "soil_perm": soil_perm,
    "groundwater_quality": groundwater_quality,
    "distance_habitat": distance_habitat,
    "distance_airport": distance_airport,
    "distance_water_body": distance_water_body,
    "type_soil": type_soil,
    "life_future": life_future,
    "waste_type": waste_type,
    "waste_quantity_site": waste_quantity_site,
    "waste_quantity_disposed": waste_quantity_disposed,
    "distance_village": distance_village,
    "flood": flood,
    "rainfall_annual": rainfall_annual,
    "distance_city": distance_city,
    "public_acceptance": public_acceptance,
    "ambient_air": ambient_air,
    "waste_hazard": waste_hazard,
    "biodegradable_waste": biodegradable_waste,
    "age_filing": age_filing,
    "waste_moisture": waste_moisture,
    "bod": bod,
    "cod": cod,
    "tds": tds}

    score = distance_water["score"] + depth_waste["score"] + area["score"] + groundwater_depth["score"] + soil_perm["score"] + groundwater_quality["score"] + distance_habitat["score"] + distance_airport["score"] + distance_water_body["score"] + type_soil["score"] + life_future["score"] + waste_type["score"] + waste_quantity_site["score"] + waste_quantity_disposed["score"] + distance_village["score"] + flood["score"] + rainfall_annual["score"] + distance_city["score"] + public_acceptance["score"] + ambient_air["score"] +  waste_hazard["score"] + biodegradable_waste["score"] + age_filing["score"] + waste_moisture["score"] + bod["score"] + cod["score"] + tds["score"]

    return render(request, 'gMapsIntegration/edit_add_more.html', {"key": key, "details_extra": x, "sen": sen_index, "score": score})

def edit_add_more_copy(ids):
    landfill = Landfills.objects.get(pk=ids)
    # The details pertaining to landfill
    x = landfill.landfill_extra.all()[0]



    distance_water = grtr(69, float(x.distance_water), 10000, 5000, 2500, 1000)
    depth_waste = lsr(64, float(x.depth_waste), 3, 10, 20, 100)
    area = lsr(61, float(x.area), 5, 10, 20, 100)
    groundwater_depth = grtr(54, float(x.groundwater_depth), 100, 20, 10, 3)
    soil_perm = lsr(54, float(x.soil_perm), 0.1, 1, 10, 100)
    groundwater_quality = {"score": 50*float(x.groundwater_quality)/4, "sensitivity": float(x.groundwater_quality)/4}
    distance_habitat = grtr(46, float(x.distance_habitat), 100, 25, 10, 5)
    distance_airport = grtr(46, float(x.distance_airport), 100, 20, 10, 5)
    distance_water_body = grtr(41, float(x.distance_water_body), 10000, 8000, 1500, 500)
    type_soil = grtr(41, float(x.type_soil), 100, 50, 30, 15)
    life_future = lsr(36, float(x.life_future), 5, 10, 20, 100)
    waste_type = {"score": 30*float(x.waste_type)/4, "sensitivity": float(x.waste_type)/4}
    waste_quantity_site = lsr(30, float(x.waste_quantity_site), 10000, 100000, 1000000, 10000000)
    waste_quantity_disposed = lsr(24, float(x.waste_quantity_disposed), 250, 500, 1000, 10000)
    distance_village = grtr(21, float(x.distance_village), 10000, 1000, 600, 300)
    flood = grtr(16, float(x.flood), 1000, 100, 30, 10)
    rainfall_annual = lsr(11, float(x.rainfall_annual), 25, 125, 250, 10000)
    distance_city = lsr(7, float(x.distance_city), 100, 20, 10, 5)
    public_acceptance = {"score": 7*float(x.public_acceptance)/4, "sensitivity": float(x.public_acceptance)/4}
    ambient_air = lsr(3, float(x.ambient_air), 0.01, 0.05, 0.1, 100)
    waste_hazard = lsr(71, float(x.waste_hazard), 10, 20, 30, 100)
    biodegradable_waste = lsr(71, float(x.biodegradable_waste), 10, 30, 60, 100)
    age_filing = grtr(58, float(x.age_filing), 100, 30, 20, 10)
    waste_moisture = lsr(71, float(x.waste_moisture), 10, 20, 40, 100)
    bod = lsr(36, float(x.bod), 30, 60, 100, 1000)
    cod = lsr(19, float(x.cod), 250, 350, 500, 10000)
    tds = lsr(13, float(x.tds), 2100, 3000, 4000, 10000)

    sen_index = {"distance_water": distance_water,
    "depth_waste": depth_waste,
    "area": area,
    "groundwater_depth": groundwater_depth,
    "soil_perm": soil_perm,
    "groundwater_quality": groundwater_quality,
    "distance_habitat": distance_habitat,
    "distance_airport": distance_airport,
    "distance_water_body": distance_water_body,
    "type_soil": type_soil,
    "life_future": life_future,
    "waste_type": waste_type,
    "waste_quantity_site": waste_quantity_site,
    "waste_quantity_disposed": waste_quantity_disposed,
    "distance_village": distance_village,
    "flood": flood,
    "rainfall_annual": rainfall_annual,
    "distance_city": distance_city,
    "public_acceptance": public_acceptance,
    "ambient_air": ambient_air,
    "waste_hazard": waste_hazard,
    "biodegradable_waste": biodegradable_waste,
    "age_filing": age_filing,
    "waste_moisture": waste_moisture,
    "bod": bod,
    "cod": cod,
    "tds": tds}

    score = round(distance_water["score"] + depth_waste["score"] + area["score"] + groundwater_depth["score"] + soil_perm["score"] + groundwater_quality["score"] + distance_habitat["score"] + distance_airport["score"] + distance_water_body["score"] + type_soil["score"] + life_future["score"] + waste_type["score"] + waste_quantity_site["score"] + waste_quantity_disposed["score"] + distance_village["score"] + flood["score"] + rainfall_annual["score"] + distance_city["score"] + public_acceptance["score"] + ambient_air["score"] +  waste_hazard["score"] + biodegradable_waste["score"] + age_filing["score"] + waste_moisture["score"] + bod["score"] + cod["score"] + tds["score"], 3)

    #Changing default long long decimal to rounded up 3 digits for beter readability
    x.distance_water = round(float(x.distance_water), 3)
    x.area = round(float(x.area), 3)
    x.distance_habitat = round(float(x.distance_habitat), 3)
    x.distance_airport = round(float(x.distance_airport), 3)
    x.distance_water_body = round(float(x.distance_water_body), 3)
    x.distance_village = round(float(x.distance_village), 3)
    x.distance_city = round(float(x.distance_city), 3)

    return {"details_extra": x, "sen": sen_index, "score": score}

def sampling_protocol(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        if request.POST.get('source', False):
            source = request.POST["source"]
            source_form = LandfillConceptualModelForm(data={"index": int(0), "data": str(source)})
            if(source_form.is_valid()):
                new_source = source_form.save(commit = False)
                new_source.landfill = landfill
                new_source.save()
        elif request.POST.get('pathways', False):
            source = request.POST["pathways"]
            source_form = LandfillConceptualModelForm(data={"index": int(1), "data": str(source)})
            if(source_form.is_valid()):
                new_source = source_form.save(commit = False)
                new_source.landfill = landfill
                new_source.save()
        elif request.POST.get('receptor', False):
            source = request.POST["receptor"]
            source_form = LandfillConceptualModelForm(data={"index": int(2), "data": str(source)})
            if(source_form.is_valid()):
                new_source = source_form.save(commit = False)
                new_source.landfill = landfill
                new_source.save()
        elif request.POST.get('layers', False):
            source = request.POST["layers"]
            source_form = LandfillConceptualModelForm(data={"index": int(3), "data": str(source)})
            if(source_form.is_valid()):
                new_source = source_form.save(commit = False)
                new_source.landfill = landfill
                new_source.save()
        elif request.POST.get('concern', False):
            source = request.POST["concern"]
            source_form = LandfillConceptualModelForm(data={"index": int(4), "data": str(source)})
            if(source_form.is_valid()):
                new_source = source_form.save(commit = False)
                new_source.landfill = landfill
                new_source.save()
    x = landfill.landfill_conceptual_model.all()

    amount_of_subarea_area = round(float(landfill.area)/10000, 4)
    amount_of_subarea = 2*math.sqrt(float(landfill.area)/10000)
    amount_of_drillings = int(round(6*amount_of_subarea, 0))

    completed0 = landfill.landfill_sample.filter(sample_type = 0).filter(completed = 1).count()
    completed1 = landfill.landfill_sample.filter(sample_type = 1).filter(completed = 1).count()
    completed2 = landfill.landfill_sample.filter(sample_type = 2).filter(completed = 1).count()
    completed3 = landfill.landfill_sample.filter(sample_type = 3).filter(completed = 1).count()

    completed = {"c0": completed0, "c1": completed1, "c2": completed2, "c3": completed3, "c00": round(100*completed0/amount_of_drillings, 2), "c11": round(100*completed1/amount_of_drillings, 2), "c22": round(100*completed2/amount_of_drillings, 2), "c33": round(100*completed3/amount_of_drillings, 2)}

    images = landfill.images.all()

    return render(request, 'gMapsIntegration/sampling_protocol.html', {"key": key, "conceptual": x, "landfill": landfill, "amount_of_subarea_area": amount_of_subarea_area, "amount_of_subarea": amount_of_subarea, "amount_of_drillings": amount_of_drillings, "completed": completed, "images": images})

def create_samples_data(landfill, area):
    amount_of_subarea = 2*math.sqrt(float(area)/10000)
    amount_of_drillings = range(int(round(6*amount_of_subarea, 0)))
    for x in amount_of_drillings:
        sample_form = LandfillSampleForm(data={"sample_type": int(0), "index": int(x)})
        sample_form1 = LandfillSampleForm(data={"sample_type": int(1), "index": int(x)})
        sample_form2 = LandfillSampleForm(data={"sample_type": int(2), "index": int(x)})
        sample_form3 = LandfillSampleForm(data={"sample_type": int(3), "index": int(x)})

        if(sample_form.is_valid()):
            sample_form = sample_form.save(commit = False)
            sample_form.landfill = landfill
            sample_form.save()
            for y in range(22):
                data_form = LandfillSampleDataForm(data={"data": float(0), "index": int(y)})
                if data_form.is_valid():
                    data_form = data_form.save(commit = False)
                    data_form.landfill_sample = sample_form
                    data_form.save()

        if(sample_form1.is_valid()):
            sample_form1 = sample_form1.save(commit = False)
            sample_form1.landfill = landfill
            sample_form1.save()
            for y in range(16):
                data_form = LandfillSampleDataForm(data={"data": float(0), "index": int(y)})
                if data_form.is_valid():
                    data_form = data_form.save(commit = False)
                    data_form.landfill_sample = sample_form1
                    data_form.save()

        if(sample_form2.is_valid()):
            sample_form2 = sample_form2.save(commit = False)
            sample_form2.landfill = landfill
            sample_form2.save()
            for y in range(15):
                data_form = LandfillSampleDataForm(data={"data": float(0), "index": int(y)})
                if data_form.is_valid():
                    data_form = data_form.save(commit = False)
                    data_form.landfill_sample = sample_form2
                    data_form.save()

        if(sample_form3.is_valid()):
            sample_form3 = sample_form3.save(commit = False)
            sample_form3.landfill = landfill
            sample_form3.save()
            for y in range(15):
                data_form = LandfillSampleDataForm(data={"data": float(0), "index": int(y)})
                if data_form.is_valid():
                    data_form = data_form.save(commit = False)
                    data_form.landfill_sample = sample_form3
                    data_form.save()

def surface_water(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        if request.POST.get('comment', False):
            comment = request.POST["comment"]
            comment_form = LandfillSampleCommentsForm(data={"sample_type": int(0), "comment": str(comment)})
            if(comment_form.is_valid()):
                new_comment = comment_form.save(commit = False)
                new_comment.landfill = landfill
                new_comment.save()
    x = landfill.landfill_sample_comments.all()
    amount_of_subarea = 2*math.sqrt(float(landfill.area)/10000)
    amount_of_drillings = range(int(round(6*amount_of_subarea, 0)))
    landfill_sam = landfill.landfill_sample.filter(sample_type = 0)
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/surface_water.html', {"key": key, "landfill": landfill, "comments": x, "range1": amount_of_drillings, "landfill_sample": landfill_sam, "districts": districts, "states": states})

def surface_water_sample(request, ids, sam_num):
    landfill = Landfills.objects.get(pk=ids)
    landfill_sam =landfill.landfill_sample.filter(sample_type = 0).get(index = (int(sam_num)-1))
    landfill_sam_data = landfill_sam.landfill_sample_data.all()
    if request.method == 'POST':
        x = 0
        for y in landfill_sam_data:
            y.data = request.POST.get("s"+str(x), 0)
            y.save()
            x = x+1
        if request.POST.get("check"):
            landfill_sam.completed = 1
            landfill_sam.save()
        else:
            landfill_sam.completed = 0
            landfill_sam.save()
        return HttpResponseRedirect(reverse('surface_water', kwargs={'ids': ids}))
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/surface_water_sample.html', {"key": key, "landfill": landfill, "sam_num": sam_num, "landfill_sam_data": landfill_sam_data, "districts": districts, "states": states})

def ground_water(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        if request.POST.get('comment', False):
            comment = request.POST["comment"]
            comment_form = LandfillSampleCommentsForm(data={"sample_type": int(1), "comment": str(comment)})
            if(comment_form.is_valid()):
                new_comment = comment_form.save(commit = False)
                new_comment.landfill = landfill
                new_comment.save()
    x = landfill.landfill_sample_comments.all()
    amount_of_subarea = 2*math.sqrt(float(landfill.area)/10000)
    amount_of_drillings = range(int(round(6*amount_of_subarea, 0)))
    landfill_sam = landfill.landfill_sample.filter(sample_type = 1)
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/ground_water.html', {"key": key, "landfill": landfill, "comments": x, "range1": amount_of_drillings, "landfill_sample": landfill_sam, "districts": districts, "states": states})

def ground_water_sample(request, ids, sam_num):
    landfill = Landfills.objects.get(pk=ids)
    landfill_sam =landfill.landfill_sample.filter(sample_type = 1).get(index = (int(sam_num)-1))
    landfill_sam_data = landfill_sam.landfill_sample_data.all()
    if request.method == 'POST':
        x = 0
        for y in landfill_sam_data:
            y.data = request.POST.get("s"+str(x), 0)
            y.save()
            x = x+1
        if request.POST.get("check"):
            landfill_sam.completed = 1
            landfill_sam.save()
        else:
            landfill_sam.completed = 0
            landfill_sam.save()
        return HttpResponseRedirect(reverse('ground_water', kwargs={'ids': ids}))
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/ground_water_sample.html', {"key": key, "landfill": landfill, "sam_num": sam_num, "landfill_sam_data": landfill_sam_data, "districts": districts, "states": states})

def sediment(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        if request.POST.get('comment', False):
            comment = request.POST["comment"]
            comment_form = LandfillSampleCommentsForm(data={"sample_type": int(2), "comment": str(comment)})
            if(comment_form.is_valid()):
                new_comment = comment_form.save(commit = False)
                new_comment.landfill = landfill
                new_comment.save()
    x = landfill.landfill_sample_comments.all()
    amount_of_subarea = 2*math.sqrt(float(landfill.area)/10000)
    amount_of_drillings = range(int(round(6*amount_of_subarea, 0)))
    landfill_sam = landfill.landfill_sample.filter(sample_type = 2)
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/sediment.html', {"key": key, "landfill": landfill, "comments": x, "range1": amount_of_drillings, "landfill_sample": landfill_sam, "districts": districts, "states": states})

def sediment_sample(request, ids, sam_num):
    landfill = Landfills.objects.get(pk=ids)
    landfill_sam =landfill.landfill_sample.filter(sample_type = 2).get(index = (int(sam_num)-1))
    landfill_sam_data = landfill_sam.landfill_sample_data.all()
    if request.method == 'POST':
        x = 0
        for y in landfill_sam_data:
            y.data = request.POST.get("s"+str(x), 0)
            y.save()
            x = x+1
        if request.POST.get("check"):
            landfill_sam.completed = 1
            landfill_sam.save()
        else:
            landfill_sam.completed = 0
            landfill_sam.save()
        return HttpResponseRedirect(reverse('sediment', kwargs={'ids': ids}))
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/sediment_sample.html', {"key": key, "landfill": landfill, "sam_num": sam_num, "landfill_sam_data": landfill_sam_data, "districts": districts, "states": states})

def soil(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        if request.POST.get('comment', False):
            comment = request.POST["comment"]
            comment_form = LandfillSampleCommentsForm(data={"sample_type": int(3), "comment": str(comment)})
            if(comment_form.is_valid()):
                new_comment = comment_form.save(commit = False)
                new_comment.landfill = landfill
                new_comment.save()
    x = landfill.landfill_sample_comments.all()
    amount_of_subarea = 2*math.sqrt(float(landfill.area)/10000)
    amount_of_drillings = range(int(round(6*amount_of_subarea, 0)))
    landfill_sam = landfill.landfill_sample.filter(sample_type = 3)
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/soil.html', {"key": key, "landfill": landfill, "comments": x, "range1": amount_of_drillings, "landfill_sample": landfill_sam, "districts": districts, "states": states})

def soil_sample(request, ids, sam_num):
    landfill = Landfills.objects.get(pk=ids)
    landfill_sam =landfill.landfill_sample.filter(sample_type = 3).get(index = (int(sam_num)-1))
    landfill_sam_data = landfill_sam.landfill_sample_data.all()
    if request.method == 'POST':
        x = 0
        for y in landfill_sam_data:
            y.data = request.POST.get("s"+str(x), 0)
            y.save()
            x = x+1
        if request.POST.get("check"):
            landfill_sam.completed = 1
            landfill_sam.save()
        else:
            landfill_sam.completed = 0
            landfill_sam.save()
        return HttpResponseRedirect(reverse('soil', kwargs={'ids': ids}))
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    return render(request, 'gMapsIntegration/soil_sample.html', {"key": key, "landfill": landfill, "sam_num": sam_num, "landfill_sam_data": landfill_sam_data, "districts": districts, "states": states})

def upload_images(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        image_form = LandfillsImagesForm(files=request.FILES)
        if image_form.is_valid():
            new_image = image_form.save(commit = False)
            new_image.landfill = landfill
            new_image.save()
    return HttpResponseRedirect(reverse('sampling_protocol', kwargs={'ids': ids}))

def form1(request, ids, langs):
    landfill = Landfills.objects.get(pk=ids)

    if landfill.landfill_form1.exists() :
        if request.method == 'POST':
            form1 = landfill.landfill_form1.all()[0]
            form1.s0 = request.POST.get("s0", "")
            form1.s1 = request.POST.get("s1", "")
            form1.s2 = request.POST.get("s2", "")
            form1.s3 = request.POST.get("s3", "")
            form1.s4 = request.POST.get("s4", "")
            form1.s5 = request.POST.get("s5", "")
            form1.s6 = request.POST.get("s6", "")
            form1.s7 = request.POST.get("s7", "")
            form1.s8 = request.POST.get("s8", "")
            form1.s9 = request.POST.get("s9", "")
            form1.s10 = request.POST.get("s10", "")
            form1.s11 = request.POST.get("s11", "")
            form1.save()
    else:
        if request.method == 'POST':
            s0 = request.POST.get("s0", "")
            form1_form = LandfillForm1Form(data={"s0": str(s0)})
            if form1_form.is_valid():
                new_form1 = form1_form.save(commit = False)
                new_form1.landfill = landfill
                new_form1.s1 = request.POST.get("s1", "")
                new_form1.s2 = request.POST.get("s2", "")
                new_form1.s3 = request.POST.get("s3", "")
                new_form1.s4 = request.POST.get("s4", "")
                new_form1.s5 = request.POST.get("s5", "")
                new_form1.s6 = request.POST.get("s6", "")
                new_form1.s7 = request.POST.get("s7", "")
                new_form1.s8 = request.POST.get("s8", "")
                new_form1.s9 = request.POST.get("s9", "")
                new_form1.s10 = request.POST.get("s10", "")
                new_form1.s11 = request.POST.get("s11", "")
                new_form1.save()
        else:
            b = LandfillForm1(landfill=landfill)
            b.save()


    landfill_form1 = landfill.landfill_form1.all()[0]

    if langs == "1":
        return render(request, 'gMapsIntegration/form1_hindi.html', {"key": key, "landfill": landfill, "landfill_form1": landfill_form1})

    elif langs == "2":
        return render(request, 'gMapsIntegration/form1_tamil.html', {"key": key, "landfill": landfill, "landfill_form1": landfill_form1})
    else:
        return render(request, 'gMapsIntegration/form1.html', {"key": key, "landfill": landfill, "landfill_form1": landfill_form1})

def form4(request, ids):
    landfill = Landfills.objects.get(pk=ids)

    if landfill.landfill_form4.exists() :
        if request.method == 'POST':
            form1 = landfill.landfill_form4.all()[0]
            form1.s0 = request.POST.get("s0", "")
            form1.s1 = request.POST.get("s1", "")
            form1.s2 = request.POST.get("s2", "")
            form1.s3 = request.POST.get("s3", "")
            form1.s4 = request.POST.get("s4", "")
            form1.s5 = request.POST.get("s5", "")
            form1.s6 = request.POST.get("s6", "")
            form1.s7 = request.POST.get("s7", "")
            form1.s8 = request.POST.get("s8", "")
            form1.s9 = request.POST.get("s9", "")
            form1.s10 = request.POST.get("s10", "")
            form1.s11 = request.POST.get("s11", "")
            form1.save()
    else:
        b = LandfillForm4(landfill=landfill)
        b.save()

    landfill_form4 = landfill.landfill_form4.all()[0]

    return render(request, 'gMapsIntegration/form4.html', {"key": key, "landfill": landfill, "landfill_form4": landfill_form4})

def populate_states_districts_data(request):
    states = []
    states_file = staticfiles_storage.path('media/states.geojson')
    with open(states_file) as data_file1:
        data1 = json.load(data_file1)

    for x in data1["features"]:
        if x["properties"]["ST_NM"] in states:
            pass
        else:
            states.append(x["properties"]["ST_NM"])

    data_file1.close()

    districts_file = staticfiles_storage.path('media/districts.geojson')

    with open(districts_file) as data_file:
        data = json.load(data_file)

    for z in states:

        if not (States.objects.filter(state=z).exists()):
            state_unsaved = States(state=z)
            state_unsaved.save()


        current_state = States.objects.get(state=z)

        for x in data["features"]:
            if x["properties"]["ST_NM"] == z:
                if not (Districts.objects.filter(state=current_state, district=x["properties"]["DISTRICT"]).exists()):
                    district_unsaved = Districts(state=current_state, district=x["properties"]["DISTRICT"])
                    district_unsaved.save()

    return HttpResponseRedirect(reverse('home'))

def api_sendDistricts(request):
    if request.method == "POST":
        state_received = str(request.POST["state"])
        state = States.objects.get(state = state_received)
        districts = state.districts.all()
        # json_in = serializers.serialize("json", districts)
        json_in = dict(districts=list(districts.values('district')))
        return JsonResponse(json_in)

def monitoring(request, ids):
    states = States.objects.all()
    districts = (States.objects.get(state="Andaman & Nicobar Island")).districts.all()
    landfill = Landfills.objects.get(pk=ids)

    if request.method == 'POST':
        if request.POST["button"] == 'soil_get_data':
            response_data_landfill = []
            response_data_data = []
            value_of_request = int(str(request.POST["value"]).lstrip('s'))
            x = landfill
            landfills_samples = x.landfill_sample.filter(sample_type=3, completed=1).all()
            for y in landfills_samples:
                landfill_sample_data1 = LandfillSampleData.objects.filter(landfill_sample_id = y.id)[value_of_request]
                landfill_sample_data2 = float(landfill_sample_data1.data)
                response_data_data.append(landfill_sample_data2)
                response_data_landfill.append("Site " + str(y.index + 1))

        if request.POST["button"] == 'surface_water_get_data':
            response_data_landfill = []
            response_data_data = []
            value_of_request = int(str(request.POST["value"]).lstrip('s'))
            x = landfill
            landfills_samples = x.landfill_sample.filter(sample_type=0, completed=1).all()
            for y in landfills_samples:
                landfill_sample_data1 = LandfillSampleData.objects.filter(landfill_sample_id = y.id)[value_of_request]
                landfill_sample_data2 = float(landfill_sample_data1.data)
                response_data_data.append(landfill_sample_data2)
                response_data_landfill.append("Site " + str(y.index + 1))

        if request.POST["button"] == 'ground_water_get_data':
            response_data_landfill = []
            response_data_data = []
            value_of_request = int(str(request.POST["value"]).lstrip('s'))
            x = landfill
            landfills_samples = x.landfill_sample.filter(sample_type=1, completed=1).all()
            for y in landfills_samples:
                landfill_sample_data1 = LandfillSampleData.objects.filter(landfill_sample_id = y.id)[value_of_request]
                landfill_sample_data2 = float(landfill_sample_data1.data)
                response_data_data.append(landfill_sample_data2)
                response_data_landfill.append("Site " + str(y.index + 1))

        if request.POST["button"] == 'sediment_get_data':
            response_data_landfill = []
            response_data_data = []
            value_of_request = int(str(request.POST["value"]).lstrip('s'))
            x = landfill
            landfills_samples = x.landfill_sample.filter(sample_type=2, completed=1).all()
            for y in landfills_samples:
                landfill_sample_data1 = LandfillSampleData.objects.filter(landfill_sample_id = y.id)[value_of_request]
                landfill_sample_data2 = float(landfill_sample_data1.data)
                response_data_data.append(landfill_sample_data2)
                response_data_landfill.append("Site " + str(y.index + 1))

        return JsonResponse(dict(landfill=response_data_landfill, data=response_data_data), safe=False)


    return render(request, 'gMapsIntegration/monitoring.html', {"landfill": landfill, "key": key, "districts": districts, "states": states})

def LandfillsFinalSiteConceptualModelSubmit(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        form1 = landfill.landfill_final_site_conceptual_model.all()[0]

        form1.s0 = request.POST.get("s0", "")
        form1.s1 = request.POST.get("s1", "")
        form1.s2 = request.POST.get("s2", "")
        form1.s3 = request.POST.get("s3", "")
        form1.s4 = request.POST.get("s4", "")
        form1.s5 = request.POST.get("s5", "")
        form1.s6 = request.POST.get("s6", "")
        form1.s7 = request.POST.get("s7", "")
        form1.s8 = request.POST.get("s8", "")
        form1.s9 = request.POST.get("s9", "")
        form1.s10 = request.POST.get("s10", "")
        form1.s11 = request.POST.get("s11", "")
        form1.save()

    return HttpResponseRedirect(reverse('details', kwargs={'ids': ids}))

def LandfillsBaselineDataSubmit(request, ids):
    landfill = Landfills.objects.get(pk=ids)
    if request.method == 'POST':
        form1 = landfill.landfill_baseline_data.all()[0]

        form1.x0 = request.POST.get("x0", "")
        form1.x1 = request.POST.get("x1", "")
        print(request.POST.get("x1", ""))
        form1.x2 = request.POST.get("x2", "")
        form1.x3 = request.POST.get("x3", "")
        form1.x4 = request.POST.get("x4", "")
        form1.x5 = request.POST.get("x5", "")
        form1.x6 = request.POST.get("x6", "")
        form1.x7 = request.POST.get("x7", "")
        form1.x8 = request.POST.get("x8", "")
        form1.save()

    return HttpResponseRedirect(reverse('details', kwargs={'ids': ids}))
