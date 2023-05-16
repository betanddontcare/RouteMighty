from vehicle import Vehicle
import math
from route_validation import get_road_length

#TRAFFICABILITY VALIDATION
def get_impassable_roads_by_trafficability(vehicle_params, all_roads):
    impassable_roads_by_trafficability = []
    for r in all_roads:
        r_direction = r['direction']
        r_max_axle_load = r['maxAxleLoad']
        r_lines = r['lines']
        r_width = r['width']
        if not (is_valid_by_load(vehicle_params.load, r_max_axle_load) 
        and is_valid_by_trafficability(vehicle_params.width, vehicle_params.spacing, vehicle_params.width_tire, r_width, r_lines, r_direction)):
            impassable_roads_by_trafficability.append(r)
    return impassable_roads_by_trafficability

def is_valid_by_trafficability(v_width, v_spacing, v_tire, r_width, r_lines, r_direction):
    if r_lines == 1 and r_direction == 'TWO_WAY':
        return v_width - ((v_width - (2 * v_tire) - v_spacing) / 2) < int(r_width) / 2 + 500
    elif r_lines == 1 and r_direction == 'ONE_WAY':
        return v_spacing + (2 * v_tire) < int(r_width) + 500
    elif r_lines > 1 and r_direction == 'TWO_WAY':
        return v_width - ((v_width - (2 * v_tire) - v_spacing) / 2) < ((2 * (r_lines - 1)*int(r_width)) / r_lines) + 500
    else:
        return v_width - ((v_width - (2 * v_tire) - v_spacing) / 2) < (((r_lines - 1)*int(r_width)) / 4 * r_lines) + 500
    
def is_valid_by_load(v_load, r_load):
    return v_load <= r_load

def get_ids_of_roads_with_not_acceptable_load_and_width(roads):
    impassable_roads_ids = []
    for r in roads:
        r_id = r['identity']
        impassable_roads_ids.append(r_id)
    return impassable_roads_ids

#WEIGHT VALIDATION  
def get_impassable_obj_by_mlc(vehicle_params, weight_obj_on_roads):
    impassable_obj_by_mlc = []
    for r in weight_obj_on_roads:
        r_mlc = r['mlc']
        if not is_valid_by_mlc(vehicle_params.mlc, r_mlc):
            impassable_obj_by_mlc.append(r)
    return impassable_obj_by_mlc

def is_valid_by_mlc(v_mlc, o_mlc):
    return v_mlc <= o_mlc

#HEIGHT VALIDATION
def get_impassable_obj_by_height(vehicle_params, height_obj_on_roads):
    impassable_obj_by_height = []
    for r in height_obj_on_roads:
        r_limit = r['limit']
        r_range = r['range']
        r_width = r['width']
        if not is_valid_by_height(vehicle_params.height, vehicle_params.width_top, r_limit, r_range, r_width):
            impassable_obj_by_height.append(r)
    return impassable_obj_by_height

def is_valid_by_height(v_height, v_width_top, o_limit, o_range, o_width):
    if o_range == 0:
        return (v_height < o_limit)
    elif o_range > 0 and (o_limit - v_height) > math.tan(math.radians(o_range)) * o_width:
        return True
    else:
        return v_width_top < (o_limit - v_height) / math.tan(math.radians(o_range))

#WIDTH VALIDATION
def get_impassable_obj_by_width(vehicle_params, width_obj_on_roads):
    impassable_obj_by_width = []
    for r in width_obj_on_roads:
        r_limits = r['limits']
        r_ranges = r['ranges']
        r_symmetric = r['symmetric']
        road_width = r['roadWidth']
        if not is_valid_by_width(vehicle_params.width_tire, vehicle_params.width, vehicle_params.width_range_start, vehicle_params.width_range_end, vehicle_params.spacing, r_limits, calculate_o_min_interval(r_limits, r_ranges), road_width, r_symmetric):
            impassable_obj_by_width.append(r)
    return impassable_obj_by_width

def is_valid_by_width(v_tire_width, v_width, v_max_width_range_start, v_max_width_range_end, v_spacing, o_limit, o_min_value_interval, road_width, o_symmetric):
    min_o_width = min(o_limit)
    if (o_symmetric == True) and (min_o_width > road_width / 2):
        return v_width < 2 * min_o_width
    elif (o_symmetric == True) and (min_o_width < road_width / 2):
        return (max(0, min(v_max_width_range_end, o_min_value_interval[1]) - max(v_max_width_range_start, o_min_value_interval[0])) == 0)
    elif (o_symmetric == False) and (min_o_width < road_width / 2):
        if ((v_width / 2) - min_o_width + (v_spacing / 2) + v_tire_width) < road_width / 2:
            return True
        else:
            return (max(0, min(v_max_width_range_end, o_min_value_interval[1]) - max(v_max_width_range_start, o_min_value_interval[0])) == 0)
    else:
        return (((v_width / 2) - road_width + (v_spacing / 2) + v_tire_width) < road_width / 2) and (v_width - road_width < min_o_width)

def calculate_o_min_interval(o_limit, o_range):
    o_min_value_interval = []
    min_o_width = min(o_limit)
    min_o_range = o_range[o_limit.index(min_o_width)]
    if o_range.index(min_o_range) == 0:
        o_min_value_interval = [0, min_o_range]
    else:
        o_min_value_interval = [o_range[o_range.index(min_o_range) - 1], o_range[o_range.index(min_o_range)] + o_range[o_range.index(min_o_range) - 1]]
    return o_min_value_interval

#SHARP BEND VALIDATION
def get_impassable_obj_by_curva(vehicle_params, curva_obj_on_roads):
    impassable_obj_by_curva = []
    for r in curva_obj_on_roads:
        r_boundary_rad = r['boundaryRadius']
        r_inner_rad = r['innerRadius']
        r_outer_rad = r['outerRadius']
        r_outer_limit = r['outerLimit']
        if not is_valid_by_curva(vehicle_params.length, vehicle_params.width, vehicle_params.first_axle, vehicle_params.last_axle, vehicle_params.width_tire, vehicle_params.angle, vehicle_params.spacing, vehicle_params.bolt, r_inner_rad, r_outer_rad, r_boundary_rad, r_outer_limit):
            impassable_obj_by_curva.append(r)
    return impassable_obj_by_curva

def is_valid_by_curva(v_length, v_width, v_first_axle, v_last_axle, v_tire_width, v_angle, v_spacing, v_bolt, r_inner_rad, r_outer_rad, r_boundary_rad, r_outer_limit):
    if (v_last_axle - v_bolt + v_spacing + 2 * v_tire_width) < 2 * r_outer_rad:
        if r_boundary_rad == 0 and r_outer_limit == 0:
            return (v_angle >= 90 - math.degrees(math.acos(((v_last_axle - v_bolt) / 2) / (r_outer_rad - v_tire_width - (v_spacing / 2)))))
        elif r_boundary_rad == 0 and r_outer_limit > 0:
            if (r_outer_limit > v_length - v_last_axle + (v_last_axle - v_bolt) / 2):
                return ((v_angle >= math.degrees(math.atan(((v_last_axle - v_bolt) / 2) / (math.sqrt(pow(r_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2))))) and ((r_outer_rad + v_tire_width + (v_spacing / 2)) < math.sqrt(pow((math.sqrt(pow(r_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2)), 2) + pow((v_first_axle - v_bolt -((v_last_axle - v_bolt) / 2)), 2))))
            else:
                return False
        elif r_boundary_rad > 0 and r_outer_limit == 0:
            return ((r_boundary_rad < math.sqrt(pow((r_outer_rad - v_tire_width - (v_spacing / 2)), 2) - pow(((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2)) and (v_angle >= 90 - math.degrees(math.acos(((v_last_axle - v_bolt) / 2) / (r_outer_rad - v_tire_width - (v_spacing / 2))))))
        else:
            if (r_outer_limit > v_length - v_last_axle + (v_last_axle - v_bolt) / 2):
                return ((v_width + r_boundary_rad < math.sqrt(pow(r_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2))) and (v_angle >= math.degrees(math.atan(((v_last_axle - v_bolt) / 2) / (math.sqrt(pow(r_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2))))) and (r_inner_rad + v_tire_width + (v_spacing / 2) < math.sqrt(pow(math.sqrt(pow(r_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2), 2) + pow((v_first_axle - v_bolt -((v_last_axle - v_bolt) / 2)), 2))))
            else:
                return False
    else:
        return False

#HILLS PASSABILITY
def get_impassable_obj_by_elevation(vehicle_params, elevation_obj_on_roads):
    impassable_obj_by_elevation = []
    for r in elevation_obj_on_roads:
        r_elevation_rad = r['elevationRadius']
        if not is_valid_by_elevation(vehicle_params.clerance, vehicle_params.last_axle, r_elevation_rad):
            impassable_obj_by_elevation.append(r)
    return impassable_obj_by_elevation

def is_valid_by_elevation(v_clearance, v_distance, r_elevation_rad):
    return v_clearance > pow(v_distance / 2, 2) / (2 * r_elevation_rad)

#ROUNDABOUT VALIDATION
def get_impassable_nodes(vehicle_params, roundabouts):
    impassable_nodes = []
    for ra in roundabouts:
        ra_outer_radius = ra['outerRadius']
        ra_inner_radius = ra['innerRadius']
        ra_vertical_island = ra['verticalIsland']
        ra_outer_limit = ra['outerLimit']
        ra_open = ra['open']
        if not is_valid_by_roundabout_size(vehicle_params.length, vehicle_params.width, vehicle_params.first_axle, vehicle_params.last_axle, vehicle_params.width_tire, vehicle_params.angle, vehicle_params.spacing, vehicle_params.bolt, ra_outer_radius, ra_inner_radius, ra_open, ra_vertical_island, ra_outer_limit):
            impassable_nodes.append(ra)
    return impassable_nodes

def is_valid_by_roundabout_size(v_length, v_width, v_first_axle, v_last_axle, v_tire_width, v_angle, v_spacing, v_bolt, ra_outer_radius, ra_inner_radius, ra_open, ra_island, ra_outer_limit):
    if ra_open == "True":
        return True
    else:
        if (v_last_axle - v_bolt + v_spacing + 2 * v_tire_width) < 2 * ra_outer_radius:
            if ra_island == 0 and ra_outer_limit == 0:
                return (v_angle >= 90 - math.degrees(math.acos(((v_last_axle - v_bolt) / 2) / (ra_outer_radius - v_tire_width - (v_spacing / 2)))))
            elif ra_island == 0 and ra_outer_limit > 0:
                if (ra_outer_limit > v_length - v_last_axle + (v_last_axle - v_bolt) / 2):
                    return ((v_angle >= math.degrees(math.atan(((v_last_axle - v_bolt) / 2) / (math.sqrt(pow(ra_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2))))) and ((ra_inner_radius + v_tire_width + (v_spacing / 2)) < math.sqrt(pow((math.sqrt(pow(ra_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2)), 2) + pow((v_first_axle - v_bolt -((v_last_axle - v_bolt) / 2)), 2))))
                else:
                    return False
            elif ra_island > 0 and ra_outer_limit == 0:
                return ((ra_island < math.sqrt(pow((ra_outer_radius - v_tire_width - (v_spacing / 2)), 2) - pow(((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2)) and (v_angle >= 90 - math.degrees(math.acos(((v_last_axle - v_bolt) / 2) / (ra_outer_radius - v_tire_width - (v_spacing / 2))))))
            else:
                if (ra_outer_limit > v_length - v_last_axle + (v_last_axle - v_bolt) / 2):
                    return ((v_width + ra_island < math.sqrt(pow(ra_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2)) and (v_angle >= math.degrees(math.atan(((v_last_axle - v_bolt) / 2) / (math.sqrt(pow(ra_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2))))) and (ra_inner_radius + v_tire_width + (v_spacing / 2) < math.sqrt(pow(math.sqrt(pow(ra_outer_limit, 2) - pow(v_length - v_last_axle + ((v_last_axle - v_bolt) / 2), 2)) - (v_width / 2), 2) + pow((v_first_axle - v_bolt -((v_last_axle - v_bolt) / 2)), 2))))
                else:
                    return False
        else:
            return False

#PARKINGS VALIDATION
def get_capable_restpoints(vehicle_params, restpoints):
    capable_restpoints = []
    for r in restpoints:
        r_occupancy = r['occupancy']
        r_slot_length = r['slotLength']
        r_slot_width = r['slotWidth']
        r_slot_hazardous = r['hazardousSlots']
        r_oversize_length = r['oversizeLength']
        r_oversize_witdh = r['oversizeWidth']
        r_security = r['security']
        r_cctv = r['cctv']
        r_barriers = r['barriers']
        r_lighting = r['lighting']
        if is_not_occupied(r_occupancy) and is_enough_space(r_slot_length, r_slot_width, r_oversize_length, r_oversize_witdh, vehicle_params.length, vehicle_params.width) and is_ok_for_hazardous(r_slot_hazardous, vehicle_params.hazardous) and is_enough_safe(r_security, r_barriers, r_cctv, r_lighting, vehicle_params.value):
            capable_restpoints.append(r)
    return capable_restpoints

def is_not_occupied(occupancy):
    return occupancy <= 0.85

def is_enough_space(slot_length, slot_width, space_length, space_width, v_length, v_width):
    if ((v_length <= slot_length) and (v_width <= slot_width)) or ((v_length <= space_length) and (v_width <= space_width)):
        return True
    else:
        return False

def is_enough_safe(security, barriers, cctv, lighting, v_value):
    if v_value == "true":
        if (((security == True) or (cctv == True)) and ((barriers == True) or (lighting == True))) or ((security == True) and (cctv == True)):
            return True
    else:
        return False

def is_ok_for_hazardous(slots_hazardous, v_hazardous):
    if v_hazardous == "true":
        return slots_hazardous > 0
    else:
        return True

#SUPPORTING FUNCTIONS

def get_unique_ids_of_items(invalid_roads, invalid_nodes):
    ids_of_ra = []
    for ra in invalid_nodes:
        ra_identity = ra['identity']
        ids_of_ra.append(ra_identity)
    return ids_of_ra + invalid_roads

def get_unique_ids_of_roads(invalid_roads):
    unify_ids = []
    sorted_ids = sorted(invalid_roads)
    for i in range(0, len(sorted_ids)):
        if sorted_ids[i] != sorted_ids[i - 1]:
            unify_ids.append(sorted_ids[i])
    return unify_ids

def get_invalid_roads(roads_by_trafficability, roads_by_mlc, roads_by_height, roads_by_width, roads_by_curva, roads_by_elevation):
    list_of_lists = roads_by_trafficability + roads_by_mlc + roads_by_height + roads_by_width + roads_by_curva + roads_by_elevation
    list_of_ids = []
    for i in list_of_lists:
        i_identity = i['identity']
        list_of_ids.append(i_identity)
    return list_of_ids

def get_roads_to_calculate(roads, rels, subnodes):
    roads_to_calculate = []
    for r in rels:
        roads_from_route = get_roads_json_to_cal(roads, r, subnodes)
        roads_to_calculate.append(roads_from_route)
    return roads_to_calculate

def get_roads_json_to_cal(roads, rel, subnodes):
    roads_from_route = []
    for r in rel:
        r_sub_id = r['identity']
        r_startpoint_id = get_sub_id(r['startPoint'], subnodes)
        r_endpoint_id = get_sub_id(r['endPoint'], subnodes)
        for ro in roads:
            ro_name = ro['name']
            ro_length = get_road_length(ro['kmRange'])
            ro_kmRange = ro['kmRange']
            ro_number = ro['number']
            ro_identity = ro['identity']
            ro_traffic_factor = get_correct_traffic_factor(ro['trafficFactor'])
            ro_type = ro['type']
            ro_lat1 = ro['lat1']
            ro_lon1 = ro['lon1']
            ro_lat2 = ro['lat2']
            ro_lon2 = ro['lon2']
            ro_mid_latitude = ro['midLatitude']
            ro_mid_longitude = ro['midLongitude']
            if r_sub_id == ro_identity:
                json_route = {'identity' : ro_identity, 'name' : ro_name, 'type' : ro_type, 'kmRange' : ro_kmRange, 'length' : ro_length, 'number' : ro_number, 'trafficFactor' : ro_traffic_factor, 'lat1' : ro_lat1, 'lon1' : ro_lon1, 'lat2' : ro_lat2, 'lon2' : ro_lon2, 'midLatitude' : round(ro_mid_latitude, 6), 'midLongitude' : round(ro_mid_longitude, 6), 'startPointID' : r_startpoint_id, 'endPointID' : r_endpoint_id}
                roads_from_route.append(json_route)
    return roads_from_route

def get_sub_id(subnode_id, subnodes):
    for s in subnodes:
        s_id = s['identity']
        s_real_node_id = s['subID']
        if subnode_id == s_id:
            return s_real_node_id

def get_correct_traffic_factor(traffic_factor):
    if traffic_factor >= 1:
        return traffic_factor
    else:
        return 1
    
def sum_routes(care_routes, dont_care_routes):
    sum_routes = care_routes + [e for e in dont_care_routes if e not in care_routes]
    return sum_routes

def get_start_name(start_point_id, nodes):
    for n in nodes:
        n_identity = n['identity']
        n_name = n['name']
        if start_point_id == n_identity:
            return n_name

def get_end_name(end_point_id, nodes):
    for n in nodes:
        n_identity = n['identity']
        n_name = n['name']
        if end_point_id == n_identity:
            return n_name
