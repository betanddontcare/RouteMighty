from math import ceil

#ROUTE WITHOUT REPEATING THE SAME NODE
def collect_valid_routes(routes):
    valid_routes = []
    for r in routes:
        if is_route_without_node_rep(r) != False:
            valid_routes.append(r)
    return valid_routes

def is_route_without_node_rep(route):
    if route != []:
        sorted_ids = sort_end_point_id(route)
        for i in range(0, len(sorted_ids)):
            if sorted_ids[i] == sorted_ids[i - 1]:
                return False

def sort_end_point_id(route):
    ids = []
    for r in route:
        r_end_point = r['endPoint']
        ids.append(r_end_point)
    sorted_ids = sorted(ids)
    return sorted_ids

#TRAFFIC FACTOR
def get_trafficpara_of_shortest_paths(list_of_routes):
    route_by_trafficpara = []
    for r in list_of_routes:
        trafficpara = round(get_route_traffic_factor(r), 4)
        route_by_trafficpara.append(trafficpara)
    return route_by_trafficpara

def get_route_traffic_factor(route):
    if route != []:
        traffic_factor = 0
        for r in route:
            r_traffic_factor = r['trafficFactor']
            r_km_range = r['length']
            if type(r_traffic_factor) != None:
                if r_traffic_factor >= 1:
                    traffic_factor += r_traffic_factor * r_km_range
                else:
                    r_traffic_factor = 1
                    traffic_factor += r_traffic_factor * r_km_range
        return traffic_factor / get_route_length(route)
    else:
        print('Route does not exist')

#LENGTH
def get_length_of_shortest_paths(list_of_routes):
    route_by_length = []
    for r in list_of_routes:
        lenght = round(get_route_length(r), 4)
        route_by_length.append(lenght)
    return route_by_length

def get_route_length(route):
    if route != []:
        km_range = 0
        for r in route:
            r_km_range = r['length']
            km_range += r_km_range
        return round(km_range, 4)
    else:
        print('Route does not exist')

def get_road_length(r):
    if len(r) == 2:
        return round(abs(r[0] - r[1]), 4)
    else:
        return 0

#TRAVEL TIME
def get_route_time_travel(list_of_routes):
    route_by_time = []
    for r in list_of_routes:
        time = ceil(get_time_of_travel(r))
        route_by_time.append(time)
    return route_by_time

def get_time_of_travel(route):
    if route != []:
        time_of_travel = 0
        for r in route:
            r_type = r['type']
            r_traffic_factor = r['trafficFactor']
            r_km_range = r['length']
            time_of_travel += get_time_of_road_travel(r_type, r_km_range, r_traffic_factor)
        return ceil(time_of_travel)   

def get_time_of_road_travel(r_type, r_km_range, r_traffic_factor):
    g, gp, s, a = get_km_min(60), get_km_min(70), get_km_min(80), get_km_min(80)
    if r_type == g:
        return r_km_range * r_traffic_factor / g
    elif r_type == gp:
        return r_km_range * r_traffic_factor / gp
    elif r_type == s:
        return r_km_range * r_traffic_factor / s
    else:
        return r_km_range * r_traffic_factor / a

def get_km_min(r):
    return r / 60

#PARKINGS ON ROUTES
def show_all_stops_on_routes(list_of_stops, list_of_routes, input_params):
    your_restpoints = []
    for r in list_of_routes:
        if do_you_need_stop(get_time_of_travel(r), input_params) == True:
            restpoints_on_route = get_all_stops_on_route(r, list_of_stops)
            specific_restpoints_on_route = show_me_restpoints_on_route(r, restpoints_on_route, input_params)   
            if 'Invalid' not in specific_restpoints_on_route:
                restpoint_params_calculator(restpoints_on_route)
            your_restpoints.append(specific_restpoints_on_route)   
        else:
            your_restpoints.append(['Shorter'])
    return your_restpoints

def restpoint_params_calculator(restpoints_on_route):
    prob_index = 0
    sum_of_slots = 0
    slots_index = 0
    for r in restpoints_on_route:
        occupancy = r['occupancy']
        slots = r['generalSlots']
        prob_index += occupancy * slots
        sum_of_slots += slots
        slots_index += slots*(1 - occupancy)

def do_you_need_stop(time_travel, input_params):
    single_drive_time = input_params.single_drive_time
    return time_travel > single_drive_time

def get_all_stops_on_route(route, list_of_stops):
    stops_on_route = []
    for n in route:
        n_start_id = n['endPointID']
        for s in list_of_stops:
            s_identity = s['identity']
            s_latitude = s['latitude']
            s_longitude = s['longitude']
            s_name = s['name']
            s_milestone = s['milestone']
            s_number = s['number']
            s_restpoint_type = s['restpointType']
            s_occupancy = s['occupancy']
            s_general_slots = s['generalSlots']
            s_slot_length = s['slotLength']
            s_slot_width = s['slotWidth']
            s_hazardous_slots = s['hazardousSlots']
            s_oversize_length = s['oversizeLength']
            s_oversize_width = s['oversizeWidth']
            s_barriers = s['barriers']
            s_cctv = s['cctv']
            s_security = s['security']
            s_lighting = s['lighting']
            if n_start_id == s_identity:
                stop = {'identity' : s_identity, 'milestone' : s_milestone, 'name' : s_name, 'roadNumber' : [s_number], 'latitude' : s_latitude, 'longitude' : s_longitude, 'restpointType' : s_restpoint_type, 'generalSlots' : s_general_slots, 'occupancy' : s_occupancy, 'slotLength' : s_slot_length, 'slotWidth' : s_slot_width, 'hazardousSlots' : s_hazardous_slots, 'oversizeLength' : s_oversize_length, 'oversizeWidth' : s_oversize_width, 'security' : s_security, 'cctv' : s_cctv, 'barriers' : s_barriers, 'lighting' : s_lighting}
                stops_on_route.append(stop)
    return stops_on_route

def show_me_restpoints_on_route(route, restpoints_on_route, input_params):
    single_time = input_params.single_drive_time
    daily_time = input_params.daily_drive_time
    weekly_time = input_params.weekly_drive_time
    route_list = route
    rest_route = []
    roads_checked = []
    time_of_single_travel = 0
    time_of_daily_travel = 0
    time_of_weekly_travel = 0
    thats_your_restpoints = []
    flag = True
    while len(roads_checked) < len(route) and flag == True:
        for r in route_list:
            r_type = r['type']
            r_km_range = r['length']
            r_traffic_factor = r['trafficFactor']
            if time_of_single_travel < single_time and time_of_daily_travel < daily_time and time_of_weekly_travel < weekly_time:
                road_travel_time = get_time_of_road_travel(r_type, r_km_range, r_traffic_factor)
                time_of_single_travel += road_travel_time 
                time_of_daily_travel += road_travel_time
                time_of_weekly_travel += road_travel_time
                roads_checked.append(r)
            elif time_of_single_travel > single_time and time_of_daily_travel < daily_time and time_of_weekly_travel < weekly_time:
                restpoint = calculate_the_best_rest_point(roads_checked, restpoints_on_route)
                if restpoint is not None and restpoint not in thats_your_restpoints: 
                    rest_route = return_the_rest_of_route(roads_checked, restpoint)
                    time_reviewer = get_time_by_step_back(roads_checked, rest_route)
                    roads_checked = rest_route
                    time_of_daily_travel = time_of_daily_travel - time_reviewer
                    time_of_weekly_travel = time_of_weekly_travel - time_reviewer
                    time_of_single_travel = 0
                    thats_your_restpoints.append(restpoint)
                    route_list = [e for e in route if e not in rest_route]
                    break
                else: 
                    thats_your_restpoints.append('Invalid')
                    flag = False
                    break
            elif (time_of_single_travel < single_time and time_of_daily_travel > daily_time and time_of_weekly_travel < weekly_time) or (time_of_single_travel > single_time and time_of_daily_travel > daily_time and time_of_weekly_travel < weekly_time):
                restpoint = calculate_the_best_rest_point(roads_checked, restpoints_on_route)
                if restpoint is not None and restpoint not in thats_your_restpoints: 
                    rest_route = return_the_rest_of_route(roads_checked, restpoint)
                    time_reviewer = get_time_by_step_back(roads_checked, rest_route)
                    roads_checked = rest_route
                    time_of_weekly_travel = time_of_weekly_travel - time_reviewer
                    time_of_single_travel = 0
                    time_of_daily_travel = 0
                    thats_your_restpoints.append(restpoint)
                    route_list = [e for e in route if e not in rest_route]
                    break
                else: 
                    thats_your_restpoints.append('Invalid')
                    flag = False
                    break
            elif time_of_single_travel < single_time and time_of_daily_travel < daily_time and time_of_weekly_travel > weekly_time:
                restpoint = calculate_the_best_rest_point(roads_checked, restpoints_on_route)
                if restpoint is not None and restpoint not in thats_your_restpoints:
                    rest_route = return_the_rest_of_route(roads_checked, restpoint)
                    time_reviewer = get_time_by_step_back(roads_checked, rest_route)
                    roads_checked = rest_route
                    time_of_weekly_travel = 0
                    time_of_single_travel = 0
                    time_of_daily_travel = 0
                    thats_your_restpoints.append(restpoint)  
                    route_list = [e for e in route if e not in rest_route]
                    break
                else: 
                    thats_your_restpoints.append('Invalid')
                    flag = False
                    break  
    return thats_your_restpoints

def get_time_by_step_back(roads_checked, rest_route):
    part_to_calculate_time = [e for e in rest_route if e not in roads_checked]
    time_to_rewind = 0
    for r in part_to_calculate_time:
        r_type = r['type']
        r_km_range = r['length']
        r_traffic_factor = r['trafficFactor']
        time_to_rewind += get_time_of_road_travel(r_type, r_km_range, r_traffic_factor)
    return time_to_rewind

def calculate_the_best_rest_point(roads_checked, restpoints_on_route):
    flag = False
    for road in reversed(roads_checked):
        road_end_point_id = road['endPointID']
        for r in restpoints_on_route:
            r_identity = r['identity']
            if road_end_point_id == r_identity:
                flag = True
                return r
        if flag:
            break

def return_the_rest_of_route(roads_checked, restpoint):
    route_to_restpoint = []
    for road in roads_checked:
        road_end_point_id = road['endPointID']
        if road_end_point_id != restpoint['identity']:
            route_to_restpoint.append(road)
        else:
            route_to_restpoint.append(road)
            break
    return route_to_restpoint

#ALLSHORTESTPATHS CUTTER
def fetch_indexes_in_chain(all_shortest_paths):
    indexes = []
    for i in range(1, len(all_shortest_paths)):
        if all_shortest_paths[i] == all_shortest_paths[0]:
            indexes.append(i)
    return indexes

def break_the_chain(all_shortest_paths):
    indexes = fetch_indexes_in_chain(all_shortest_paths)
    chain_to_analyse = all_shortest_paths
    list_of_routes = []
    if indexes != []:
        for i in indexes:
            path = chain_to_analyse[0 : i]
            list_of_routes.append(path)
            rest = chain_to_analyse[i : len(chain_to_analyse)]
            if len(path) == len(rest):
                list_of_routes.append(rest)
            else:
                chain_to_analyse = rest
    else:
        list_of_routes.append(chain_to_analyse)
    return list_of_routes

#OBSTACLES ON ROUTE
def get_cost_for_all_routes(routes, obstacles, impassable_obj, roads_connected_with_ra, impassable_ra):
    costs = []
    for r in routes:
        cost = get_cost_of_remove_obst_on_route(r, obstacles, impassable_obj, roads_connected_with_ra, impassable_ra)
        costs.append(cost)
    return costs

def get_cost_of_remove_obst_on_route(route, obstacles, impassable_obj, roads_connected_with_ra, impassable_ra):
    obst_on_route = get_obstacles_on_route(route, obstacles)
    ra_on_route = get_impassable_ra_on_route(route, roads_connected_with_ra, impassable_ra)
    cost_of_i_obj = get_cost_of_i_obj_on_route(obst_on_route, impassable_obj)
    cost_of_i_ra = get_cost_of_i_ra_on_route(ra_on_route)
    return cost_of_i_obj + cost_of_i_ra

def get_cost_of_i_obj_on_route(obst_on_route, impassable_obj):
    cost_of_travel = 0
    for o in obst_on_route:
        obst_id = o['obstacleID']
        for i in impassable_obj:
            i_obst_id = i['obstacleID']
            i_removal_cost = i['removalCost']
            if obst_id == i_obst_id:
                cost_of_travel += i_removal_cost
    return cost_of_travel

def get_cost_of_i_ra_on_route(impassable_ra):
    cost_of_travel = 0
    for ra in impassable_ra:
        ra_removal_cost = ra['removalCost']
        cost_of_travel += ra_removal_cost
    return cost_of_travel

def get_i_obj_on_all_routes(routes, obstacles, impassable_obj):
    i_objects = []
    for r in routes:
        i_objects_list = get_impassable_obj_on_route(r, obstacles, impassable_obj)
        i_objects.append(i_objects_list)
    return i_objects    

def get_impassable_obj_on_route(route, obstacles, impassable_obj):
    obst_on_route = get_obstacles_on_route(route, obstacles)
    cords_of_i_obj = []
    for o in obst_on_route:
        obst_id = o['obstacleID']
        obst_r_number = o['number']
        obst_name = o['name']
        obst_milestone = o['milestone']
        obst_lat = o['latitude']
        obst_lon = o['longitude']
        for i in impassable_obj: 
            i_obst_id = i['obstacleID'] 
            if obst_id == i_obst_id:
                impassable_obj_to_remove = {'identity' : obst_id, 'name' : obst_name, 'milestone' : obst_milestone, 'number' : obst_r_number, 'latitude' : obst_lat, 'longitude' : obst_lon}
                cords_of_i_obj.append(impassable_obj_to_remove)
    return cords_of_i_obj

def get_obstacles_on_route(route, obstacles):
    obstacles_on_route = []
    for r in route:
        r_identity = r['identity']
        for o in obstacles:
            o_identity = o['identity']
            if r_identity == o_identity:
                obstacles_on_route.append(o)
    return obstacles_on_route

#SAFETY
def get_weather_index_for_routes(weather_conditions, length):
    weather_index = 0
    for w in weather_conditions:
        w_weather_index = w['weatherIndex']
        weather_index += w_weather_index
    return round((weather_index / length), 4)

def get_safety_index_for_routes(traffic_factor, weather_conditions, length):
    safety_index = 0
    for w in weather_conditions:
        w_safety_index = w['safetyIndex']
        safety_index += w_safety_index
    return round(((safety_index * traffic_factor) / length), 4)

#ROUTES VALIDATION BASED ON OPERATOR PREFERENCES
def get_roads_after_limits(roads_to_calculate, max_cost, max_time_travel, obstacles, impassable_obj, roads_connected_with_ra, impassable_ra):
    your_routes = []
    for r in roads_to_calculate:
        if get_cost_of_remove_obst_on_route(r, obstacles, impassable_obj, roads_connected_with_ra, impassable_ra) <= max_cost and get_time_of_travel(r) <= max_time_travel:
            your_routes.append(r)
    return your_routes

#IMPASSABLE ROUNDABOUTS ON ROUTES
def get_i_ra_on_all_routes(routes, roads_connected_with_ra, impassable_ra):
    i_roundabouts = []
    for r in routes:
        i_roundabouts_list = get_impassable_ra_on_route(r, roads_connected_with_ra, impassable_ra)
        i_roundabouts.append(i_roundabouts_list)
    return i_roundabouts
  
def get_impassable_ra_on_route(route, roads_connected_with_ra, impassable_ra):
    ra_on_route = get_ra_on_route(route, roads_connected_with_ra)
    i_ra_on_route = []
    for ra in ra_on_route:
        ra_id = ra['obstacleID']
        ra_latitude = ra['latitude']
        ra_longitude = ra['longitude']
        ra_removal_cost = ra['removalCost']
        ra_name = ra['name']
        for i_ra in impassable_ra:
            i_ra_id = i_ra['obstacleID'] 
            if ra_id == i_ra_id:
                impassable_ra_to_remove = {'name' : ra_name, 'removalCost' : ra_removal_cost, 'latitude' : ra_latitude, 'longitude' : ra_longitude}
                i_ra_on_route.append(impassable_ra_to_remove) if impassable_ra_to_remove not in i_ra_on_route else i_ra_on_route
    return i_ra_on_route

def get_ra_on_route(route, roads_connected_with_ra):
    ra_on_route = []
    for r in route:
        r_identity = r['identity']
        for ro in roads_connected_with_ra:
            ro_identity = ro['identity']
            if r_identity == ro_identity:
                ra_on_route.append(ro)
    return ra_on_route

def get_ids_of_ra(ra):
    ids_of_ra = []
    for r in ra:
        r_id = r['obstacleID']
        ids_of_ra.append(r_id)
    return ids_of_ra