import requests, json

def request_16_day_forecast(latitude, longitude, day_to_depart):
    url = "https://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(latitude) + "&lon=" + str(longitude) + "&cnt=" + str(day_to_depart + 1) + "&appid=" + #YOUR OPEN WEATHER API KEY
    response = requests.get(url)
    return json.loads(response.text)

def get_weather_conditions_for_routes(routes, day_to_depart):
    weather_conditions_for_routes = []
    weather_for_uniqe_roads = get_weather_for_roads(get_uniqe_roads_in_routes(routes), day_to_depart)
    for r in routes:
        weather_conditions_for_r = []
        for ro in r:
            ro_latitude = ro['midLatitude']
            ro_longitude = ro['midLongitude']
            for i in range(0, len(weather_for_uniqe_roads)):
                if weather_for_uniqe_roads[i]['midLatitude'] == ro_latitude and weather_for_uniqe_roads[i]['midLongitude'] == ro_longitude:
                    weather_conditions_for_r.append(weather_for_uniqe_roads[i])
        weather_conditions_for_routes.append(weather_conditions_for_r)
    return weather_conditions_for_routes

def get_uniqe_roads_in_routes(routes):
    list_of_uniqe_roads = []
    for r in routes:
        for ro in r:
            ro_length = ro['length']
            if ro_length > 0:
                list_of_uniqe_roads.append(ro) if ro not in list_of_uniqe_roads else list_of_uniqe_roads
    return list_of_uniqe_roads

def get_weather_for_roads(uniqe_roads, day_to_depart):
    weather_for_list_of_roads = []
    for r in uniqe_roads:
        r_latitude = r['midLatitude']
        r_longitude = r['midLongitude']
        r_km_range = r['kmRange']
        r_number = r['number']
        weather = request_16_day_forecast(r['midLatitude'], r['midLongitude'], day_to_depart)
        temp = float(weather['list'][day_to_depart]['temp']['min'])
        precipitation = float(weather['list'][day_to_depart]['pop'])
        if precipitation != 0: 
            try:
                pop_index = float(weather['list'][day_to_depart]['rain'])
            except:
                pop_index = 5
        else:
            pop_index = 0
        weather_json = {'midLatitude' : r_latitude, 'midLongitude' : r_longitude, 'kmRange' : r_km_range, 'number' : r_number, 'temp' : temp, 'pop' : precipitation, 'popIndex' : pop_index, 'isBad' : is_weather_bad(temp, precipitation, day_to_depart), 'weatherIndex' : get_weather_index_for_road(r, pop_index), 'safetyIndex' : get_safety_index_for_road(r, pop_index)}
        weather_for_list_of_roads.append(weather_json)   
    return weather_for_list_of_roads

def is_weather_bad(temp, precipitation, day_to_depart):
    if day_to_depart <= 3:
        return temp <= 274.15 and precipitation >= 0.375
    elif day_to_depart <= 8 and day_to_depart > 3:
        return temp <= 275.15 and precipitation >= 0.25
    else:
        return temp <= 276.15 and precipitation >= 0.13

def get_weather_index_for_road(road, pop_index):
    ro_length = road['length']
    max_pre_in_pl = 300
    if pop_index > 0 and ro_length > 0:
        return round((pop_index/max_pre_in_pl * ro_length), 4)
    else:
        return 1

def get_safety_index_for_road(road, pop_index):
    ro_traffic_factor = road['trafficFactor']
    if pop_index > 0:
        safety_index = ro_traffic_factor * get_weather_index_for_road(road, pop_index)
    else:
        safety_index = 1
    return round(safety_index, 4)

def get_only_bad_weather(weather_for_roads):
    roads_with_bad_weather = []
    for w in weather_for_roads:
        w_is_bad = w['isBad']
        if w_is_bad == True:
            roads_with_bad_weather.append(w)
    return roads_with_bad_weather
