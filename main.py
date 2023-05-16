from neo4j import GraphDatabase, unit_of_work
from vehicle import Vehicle
import validation, route_validation, weather
from math import ceil

server_ip = #YOUR NEO4J SERVER IP
uri = f"bolt://{server_ip}:7687"
driver = GraphDatabase.driver(uri, auth=(#YOUR LOGIN, #YOUR PASSWORD))

#NEO4j QUERIES
def find_all_roads(tx):
    roads = []
    result = tx.run("MATCH (r:Road) RETURN ID(r) as identity, r.type as type, r.numbers as number, r.name as name, r.maxAxleLoad as maxAxleLoad, r.lines as lines, "\
    "r.width as width, r.kmRange as kmRange, r.trafficFactor as trafficFactor, r.direction as direction, r.midLatitude as midLatitude, r.midLongitude as midLongitude, r.lat1 as lat1, r.lon1 as lon1, r.lat2 as lat2, r.lon2 as lon2 order by identity")
    for record in result:
        roads.append(record)
    return roads

def find_all_obstacles_on_roads(tx):
    obstacles = []
    result = tx.run("MATCH p=((n:Road)-[r:OBSTRUCTS]-(m:Obstacle)) RETURN ID(n) as identity, n.numbers as number, m.name as name, ID(m) as obstacleID, m.milestone as milestone, m.latitude as latitude, m.longitude as longitude order by identity")
    for record in result:
        obstacles.append(record)
    return obstacles

def find_roundabouts(tx):
    roundabouts = []
    result = tx.run("MATCH p=((n:Node)-[r:IS_ROUNDABOUT]-(m:Roundabout)) RETURN ID(n) as identity, n.name as name, ID(m) as obstacleID, m.outerDiameter as outerDiameter, "\
    "m.innerDiameter as innerDiameter, m.verticalIsland as verticalIsland, m.open as open, m.removalCost as removalCost, m.outerLimit as outerLimit")
    for record in result:
        roundabouts.append(record)
    return roundabouts

def find_roads_connected_with_ra(tx):
    roads_connected_with_ra = []
    result = tx.run("MATCH p=((r:Road)-[:EXIT]-(n:Roundabout)-[:IS_ROUNDABOUT]-(c:Node)) RETURN ID(r) as identity, ID(n) as obstacleID, n.removalCost as removalCost, c.latitude as latitude, c.longitude as longitude, c.name as name")
    for record in result:
        roads_connected_with_ra.append(record)
    return roads_connected_with_ra

def find_all_nodes(tx):
    nodes = []
    result = tx.run("MATCH (n:Node) RETURN ID(n) as identity, n.name as name")
    for record in result:
        nodes.append(record)
    return nodes

def find_all_subnodes(tx):
    subnodes = []
    result = tx.run("MATCH (n:Subnode) RETURN ID(n) as identity, n.subID as subID, n.name as name")
    for record in result:
        subnodes.append(record)
    return subnodes

def find_weight_obj_on_roads(tx):
    weight_obj_on_roads = []
    result = tx.run("MATCH p=((n:Road)-[x:OBSTRUCTS]-(o:Obstacle)-[r:HAS]-(w:WeightObstruction)) RETURN ID(n) as identity, n.name as name, ID(o) as obstacleID, w.mlc as mlc, w.removalCost as removalCost")
    for record in result:
        weight_obj_on_roads.append(record)
    return weight_obj_on_roads

def find_height_obj_on_roads(tx):
    height_obj_on_roads = []
    result = tx.run("MATCH p=((n:Road)-[x:OBSTRUCTS]-(o:Obstacle)-[r:HAS]-(h:HeightObstruction)) RETURN ID(n) as identity, n.name as name, ID(o) as obstacleID, n.width as width, h.limit as limit, h.range as range, h.removalCost as removalCost")
    for record in result:
        height_obj_on_roads.append(record)
    return height_obj_on_roads

def find_width_obj_on_roads(tx):
    width_obj_on_roads = []
    result = tx.run("MATCH p=((n:Road)-[x:OBSTRUCTS]-(o:Obstacle)-[r:HAS]-(w:WidthObstruction)) RETURN ID(n) as identity, n.name as name, ID(o) as obstacleID, n.width as roadWidth, w.limits as limits, "\
    "w.ranges as ranges, w.symmetric as symmetric, w.removalCost as removalCost")
    for record in result:
        width_obj_on_roads.append(record)
    return width_obj_on_roads

def find_curvature_obj_on_roads(tx):
    curva_obj_on_roads = []
    result = tx.run("MATCH p=((n:Road)-[x:OBSTRUCTS]-(o:Obstacle)-[r:HAS]-(c:CurvatureObstruction)) RETURN ID(n) as identity, n.name as name, ID(o) as obstacleID, c.boundaryRadius as boundaryRadius, "\
    "c.innerRadius as innerRadius, c.outerRadius as outerRadius, c.removalCost as removalCost, c.outerLimit as outerLimit")
    for record in result:
        curva_obj_on_roads.append(record)
    return curva_obj_on_roads

def find_elevation_obj_on_roads(tx):
    elevation_obj_on_roads = []
    result = tx.run("MATCH p=((n:Road)-[x:OBSTRUCTS]-(o:Obstacle)-[r:HAS]-(e:ElevationObstruction)) RETURN ID(n) as identity, n.name as name, ID(o) as obstacleID, e.verticalCurveRadius as elevationRadius, e.removalCost as removalCost")
    for record in result:
        elevation_obj_on_roads.append(record)
    return elevation_obj_on_roads

def find_restpoints(tx):
    restpoints = []
    result = tx.run("MATCH p=((n:Node)-[r:IS_RESTPOINT]-(m:RestPoint)) RETURN ID(n) as identity, n.latitude as latitude, n.longitude as longitude, n.name as name, ID(m) as restpointID, m.milestone as milestone, "\
    "m.roadNumber as number, m.restpointType as restpointType, m.occupancy as occupancy, m.generalSlots as generalSlots, m.slotLength as slotLength, m.slotWidth as slotWidth, "\
    "m.hazardousSlots as hazardousSlots, m.oversizeLength as oversizeLength, m.oversizeWidth as oversizeWidth, m.barriers as barriers, m.cctv as cctv, m.security as security, m.lighting as lighting")
    for record in result:
        restpoints.append(record)
    return restpoints

#THE SHORTEST PATHS QUERIES
    #SINGLE IN ROUTES GRAPH
@unit_of_work(timeout=1.0)
def find_subrels_of_shortest_path(tx, counter, omitted_roads, start_point_id, end_point_id):
    shortest_path_rels = []
    result = tx.run(f"MATCH p=shortestPath((n1:Subnode)-[*]->(n2:Subnode)) WHERE n1.subID = {start_point_id} AND n2.subID = {end_point_id} AND ALL (omittedRel in relationships(p) WHERE NOT omittedRel.subID in {omitted_roads}) AND LENGTH(p) > {counter} UNWIND relationships(p) as rel RETURN rel as rel, rel.subID as identity, ID(startNode(rel)) as startPoint, ID(endNode(rel)) as endPoint")
    for record in result:
        shortest_path_rels.append(record)
    return shortest_path_rels

    #MULTI IN ROUTES GRAPH
@unit_of_work(timeout=1.0)
def find_subrels_of_multi_path(tx, counter, omitted_roads, start_point_id, end_point_id):
    multi_path_rels = []
    result = tx.run(f"MATCH p=allShortestPaths((n1:Subnode)-[*]->(n2:Subnode)) WHERE n1.subID = {start_point_id} AND n2.subID = {end_point_id} AND ALL (omittedRel in relationships(p) WHERE NOT omittedRel.subID in {omitted_roads}) AND LENGTH(p) > {counter} UNWIND relationships(p) as rel RETURN rel as rel, rel.subID as identity, ID(startNode(rel)) as startPoint, ID(endNode(rel)) as endPoint")
    for record in result:
        multi_path_rels.append(record)
    return multi_path_rels

    #SUM OF SINGLE AND MULTI PATHS
def collect_multi_path_subrels(staff_to_omit, start_point_id, end_point_id):
    counter = 0 
    multi_path_rels_list = []
    while counter < 1:
        try:
            multi_path_rels = session.execute_read(find_subrels_of_multi_path, 0, staff_to_omit, start_point_id, end_point_id)
            sliced_chain = route_validation.break_the_chain(multi_path_rels)
            for r in sliced_chain:
                multi_path_rels_list.append(r)
            counter = len(sliced_chain[0])
        except:
            break
    return multi_path_rels_list
    
    #COLLECT TO RETURN ALL
def collect_rels_of_shortest_paths(staff_to_omit, start_point_id, end_point_id):
    counter = 0
    multi_shortest_paths_rels = collect_multi_path_subrels(staff_to_omit, start_point_id, end_point_id)
    single_shortest_paths_rels = []
    while counter < 120:
        try:
            shortest_path_rels = session.execute_read(find_subrels_of_shortest_path, counter, staff_to_omit, start_point_id, end_point_id)
            single_shortest_paths_rels.append(shortest_path_rels)
            counter = len(shortest_path_rels)
        except:
            break
    sum_path_rels = [e for e in single_shortest_paths_rels if e not in multi_shortest_paths_rels]
    return sum_path_rels

with driver.session() as session:

    def calculate(request_data):
        vehicle_input = Vehicle(request_data['vLength'], request_data['vWidth'], request_data['vWidthTop'], request_data['vWidthRangeStart'], request_data['vWidthRangeEnd'], request_data['vHeight'], request_data['vMlc'], request_data['vClerance'], request_data['vFirstAxle'], request_data['vLastAxle'], request_data['vTireWidth'], request_data['vSpacing'], request_data['vAngle'], request_data['vLoad'], request_data['vBolt'], request_data['vHazardous'], request_data['vValue'], request_data['vDrivers'], request_data['singleDriveTime'], request_data['dailyDriveTime'], request_data['weeklyDriveTime'])
        start_point_id = request_data['start']
        end_point_id = request_data['end']
        day_to_depart = request_data['daysToDepart']
        max_cost = request_data['maxCost']
        max_time_travel = request_data['maxTime']

        #NODES
        nodes = session.execute_read(find_all_nodes)
        subnodes = session.execute_read(find_all_subnodes)

        #ROADS
        roads = session.execute_read(find_all_roads)
        weight_obj_on_roads = session.execute_read(find_weight_obj_on_roads)
        height_obj_on_roads = session.execute_read(find_height_obj_on_roads)
        width_obj_on_roads = session.execute_read(find_width_obj_on_roads)
        curva_obj_on_roads = session.execute_read(find_curvature_obj_on_roads)
        elevation_obj_on_roads = session.execute_read(find_elevation_obj_on_roads)

        #OBSTACLES
        obstacles = session.execute_read(find_all_obstacles_on_roads)

        #ROUNDABOUTS
        roundabouts = session.execute_read(find_roundabouts)

        #ROADS CONNECTED WITH ROUNDABOUTS
        roads_connected_with_ra = session.execute_read(find_roads_connected_with_ra)

        #IMPASSABLE ROADS
        impassable_roads_by_trafficability = validation.get_impassable_roads_by_trafficability(vehicle_input, roads)
        impassable_obj_by_mlc = validation.get_impassable_obj_by_mlc(vehicle_input, weight_obj_on_roads)
        impassable_obj_by_height = validation.get_impassable_obj_by_height(vehicle_input, height_obj_on_roads)
        impassable_obj_by_width =  validation.get_impassable_obj_by_width(vehicle_input, width_obj_on_roads)
        impassable_obj_by_curva = validation.get_impassable_obj_by_curva(vehicle_input, curva_obj_on_roads)
        impassable_obj_by_elevation = validation.get_impassable_obj_by_elevation(vehicle_input, elevation_obj_on_roads)
        all_invalid_roads_ids = validation.get_invalid_roads(impassable_roads_by_trafficability, impassable_obj_by_mlc, impassable_obj_by_height, impassable_obj_by_width, impassable_obj_by_curva, impassable_obj_by_elevation)
        impassable_roads = validation.get_unique_ids_of_roads(all_invalid_roads_ids)

        #IMPASSABLE NODES (ROUNDABOUTS)
        impassable_nodes = validation.get_impassable_nodes(vehicle_input, roundabouts)

        #IDs OF IMPASSABLE ROADS (TRAFFICABILITY)
        i_road_by_trafficability_ids = validation.get_ids_of_roads_with_not_acceptable_load_and_width(impassable_roads_by_trafficability)

        #IMPASSABLE OBCJECTS
        impassable_obj = impassable_nodes + impassable_obj_by_mlc + impassable_obj_by_height + impassable_obj_by_width + impassable_obj_by_curva + impassable_obj_by_elevation

        #PARKINGS
        restpoints = session.execute_read(find_restpoints)

        #VALID PARKINGS
        valid_restpoints = validation.get_capable_restpoints(vehicle_input, restpoints)

        #OBJECTS TO OMIT
        staff_to_omit = validation.get_unique_ids_of_items(impassable_roads, impassable_nodes)

        #NODES NAME CHECKER
        start_point = validation.get_start_name(start_point_id, nodes)
        end_point = validation.get_end_name(end_point_id, nodes)

        #THE SHORTEST PATH WITHOUT REMOVE OBSTACLES
        all_shortest_path_rels = collect_rels_of_shortest_paths(staff_to_omit, start_point_id, end_point_id)
        valid_routes = route_validation.collect_valid_routes(all_shortest_path_rels)
        care_routes = validation.get_roads_to_calculate(roads, valid_routes, subnodes)
            
        #THE SHORETST PATH WITH REMOVE OBSTACLES
        paths_to_cal_cost = collect_rels_of_shortest_paths(i_road_by_trafficability_ids, start_point_id, end_point_id)
        valid_dont_care_routes = route_validation.collect_valid_routes(paths_to_cal_cost)
        dont_care_routes = validation.get_roads_to_calculate(roads, valid_dont_care_routes, subnodes)
        
        #EXTRACTING ROADS FROM ROUTE GRAPH RELS
        roads_to_calculate = validation.sum_routes(care_routes, dont_care_routes)

        #RETURNED ROUTES
        your_roads = route_validation.get_roads_after_limits(roads_to_calculate, max_cost, max_time_travel, obstacles, impassable_obj, roads_connected_with_ra, impassable_nodes)

        #TIME TRAVEL FOR ROUTES
        time_travel = route_validation.get_route_time_travel(your_roads)

        #COST OF TRAVEL FOR ROUTES
        cost = route_validation.get_cost_for_all_routes(your_roads, obstacles, impassable_obj, roads_connected_with_ra, impassable_nodes)

        #ROUTES LENGTH
        length = route_validation.get_length_of_shortest_paths(your_roads)

        #AVERAGE TRAFFIC FACTOR FOR ROUTES
        traffic_factor = route_validation.get_trafficpara_of_shortest_paths(your_roads)

        #PARKINGS FOR ROUTES
        restpoints_on_route = route_validation.show_all_stops_on_routes(valid_restpoints, your_roads, vehicle_input)

        #IMPASSABLE OBJECTS ON ROUTES
        i_obj_on_route = route_validation.get_i_obj_on_all_routes(your_roads, obstacles, impassable_obj)

        #WEATHER FOR ROUTES
        weather_conditions = weather.get_weather_conditions_for_routes(your_roads, day_to_depart)

        #IMPASSABLE ROUNDABOUTS ON ROUTES
        i_ra_on_routes = route_validation.get_i_ra_on_all_routes(your_roads, roads_connected_with_ra, impassable_nodes)

        def get_json():
            result = []
            for i in range(0, len(length)):
                if restpoints_on_route[i] != ['Invalid'] and "Invalid" not in restpoints_on_route[i]:
                    route = {'startPoint' : start_point, 'endPoint' : end_point, 'roadRows': your_roads[i], 'length' : length[i], 'trafficFactor' : traffic_factor[i], 'timeTravel' : time_travel[i], 'restpoints' : restpoints_on_route[i], 'impassableObjects' : i_obj_on_route[i], 'impassableRoundabouts' : i_ra_on_routes[i], 'cost' : cost[i], 'weather' : weather.get_only_bad_weather(weather_conditions[i]), 'weatherIndex' : route_validation.get_weather_index_for_routes(weather_conditions[i], length[i]), 'safetyIndex' : route_validation.get_safety_index_for_routes(traffic_factor[i], weather_conditions[i], length[i])}
                    result.append(route)
            return result
        result = get_json()
        return result

    calculate({'vLength' : 10000, 'vWidth' : 3000, 'vWidthTop' : 3000, 'vWidthRangeStart' : 0, 'vWidthRangeEnd' : 4000, 'vHeight' : 4000, 
           'vMlc' : 100, 'vClerance' : 500, 'vFirstAxle' : 15000, 'vLastAxle' : 23000, 'vTireWidth' : 300, 'vSpacing' : 2700, 'vAngle' : 45, 
           'vLoad' : 115, 'vBolt' : 5000, 'vHazardous' : False, 'vValue' : 40000, 'vDrivers' : 1, 'singleDriveTime' : 300, 'dailyDriveTime' : 500, 
           'weeklyDriveTime' : 3000, 'start' : 749, 'end' : 97, 'daysToDepart' : 3, 'maxCost' : 100000, 'maxTime' : 1000})

driver.close()

