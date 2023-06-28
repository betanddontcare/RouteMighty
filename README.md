![rm](https://github.com/betanddontcare/RouteMighty/assets/31188390/691ac948-e4a2-462f-92d7-9b659150a42a)

# RouteMighty 1.2.0
RouteMighty is a software application engine developed in Python for the efficient planning of routes for abnormal vehicles, such as those that are overweight or oversized.

This software based on a novel method developed in my PhD disseration titled: [Computer-aided method of transport planning process for abnormal vehicles](https://www.researchgate.net/publication/352283436_Metoda_komputerowego_wspomagania_procesu_planowania_przemieszczania_pojazdow_nienormatywnych) The dissertation was awarded by Polish Prime Minister as one of the best dissertaions in Poland (2021) :crown:.

![rm_arch](https://github.com/betanddontcare/RouteMighty/assets/31188390/5681e7e6-bbae-4432-a9f6-f9c5d188dc79)

# Requirements & Installation
In order to successfully run the tool you need to:

## Step 1: 

Install all the requirements before proceeding to next steps:

* Flask==2.3.2
* Flask-Cors==3.0.10
* neo4j==5.8.0
* requests==2.28.2

You should install all the python3 modules using the pip3 install *package_name* command.

(or alternatively using: sudo apt-get install python3-*package_name* conmmand)

## Step 2: 

Create the transportation network based on the structure presented in **Neo4j Graph Database** structure chapter using Neo4j. 

## Step 3: 

Host your graph database locally or in the cloud. Fill the IP address of your server in the ```main.py``` file (```server_ip``` variable). 

## Step 4: 

Assign your login and password to the ```GraphDatabase.driver()``` in ```main.py``` file.

## Step 5: 

Sign-up on [OpenWeather](https://openweathermap.org/) webservice and generate your API key for Daily Forecast 16 days service. Assign your API key to ```open_weather_api_key``` variable in ```weather.py```.

## Step 6: 

Configure the ```server.py``` file and host a Flask microservice. 

## Step 7: 

Send a ```POST``` query to the Flask. The request should be a JSON object consists of a following keys with parameters:

### Related to vehicle

![vehic](https://github.com/betanddontcare/RouteMighty/assets/31188390/514e4089-d2c5-469e-a86a-6dfc83db9412)


```vLength```	rigid lorry or semi-trailer length [in millimeters]

```vWidth```	maximum vehicle width [in millimeters]

```vWidthTop```	vehicle width at maximum height [in millimeters]

```vWidthRangeStart```	height from which the maximum width of the vehicle occurs [in millimeters]

```vWidthRangeEnd```	height up to which the maximum width of the vehicle occurs [in millimeters]

```vHeight```	vehicle height [in millimeters]

```vMlc```	MLC class value of the vehicle [MLC class]

```vClerance```	ground clearance [in millimeters]

```vFirstAxle```	distance between the front bumper and the first axle located behind the geometric centre of the vehicle in a rigid lorry (if the vehicle has more than 2 axles) or the front of the semi-trailer and its first axle [in millimeters]

```vLastAxle```	distance between the front bumper and the last axle on a rigid lorry or the front of the semi-trailer and its last axle [in millimeters]

```vTireWidth```	tire width [in millimeters]

```vSpacing```	wheelbase of a vehicle [in millimeters]

```vAngle```	maximum steering angle of the last axle of the vehicle [in degrees]

```vLoad```	the highest value of the axle load [in kilonewtons]

```vBolt```	distance between the front bumper and the first axle in a rigid lorry, or the distance between the front of the semi-trailer and the fifth wheel [in millimeters]

```vHazardous```	presence of dangerous goods [True/False]

### Related to operator preferences and information collected

```vValue```	cargo value [in dollars]

```vDrivers```	number of drivers in the crew 

```singleDriveTime```	maximum single driving time [in minutes]

```dailyDriveTime```	maximum daily driving time [in minutes]

```weeklyDriveTime```	maximum weekly driving time [in minutes]

```start```	id of the defined start node

```end```	id of the defined end node

```daysToDepart```	number of days until planned departure [0 - today, 1 - tomorrow, etc.]

```maxCost```	maximum amount declared by the carrier to cover the costs of disassembly/reconstruction of infrastructure elements [in dollars]

```maxTime```	maximum travel time [in minutes]

Example of correct JSON object needed to request:

```{'vLength' : 10000, 'vWidth' : 3000, 'vWidthTop' : 3000, 'vWidthRangeStart' : 0, 'vWidthRangeEnd' : 4000, 'vHeight' : 4000, 'vMlc' : 100, 'vClerance' : 500, 'vFirstAxle' : 15000, 'vLastAxle' : 23000, 'vTireWidth' : 300, 'vSpacing' : 2700, 'vAngle' : 45, 'vLoad' : 115, 'vBolt' : 5000, 'vHazardous' : False, 'vValue' : 40000, 'vDrivers' : 1, 'singleDriveTime' : 300, 'dailyDriveTime' : 500, 'weeklyDriveTime' : 3000, 'start' : 749, 'end' : 97, 'daysToDepart' : 3, 'maxCost' : 100000, 'maxTime' : 1000}```

## Step 8:

Use data from the response. 

The responded JSON object contains:

1. List of routes with parameters

Every route contains:

1. List of roads consisting of every route. There is an example of single element of this list:

```{'identity': 684, 'name': 'Dębe Wielkie - Mińsk Mazowiecki', 'type': 'GP', 'kmRange': [512.481, 515.2], 'length': 2.719, 'number': ['92'], 'trafficFactor': 1.0487, 'lat1': 52.200531, 'lon1': 21.491036, 'lat2': 52.19092, 'lon2': 21.5274, 'midLatitude': 52.195727, 'midLongitude': 21.50922, 'startPointID': 96, 'endPointID': 97}```

2. Additional parameters useful for assessment and for planning process improvement:

 ```length:``` Total length (in kilometers) of the route (eg. 83.917).
 
 ```trafficFactor:``` Total traffic factor reflects how much longer or shorter the time required to cover the distance between the starting point and ending point in relation to the historical average travel time (eg. 1.0262 - means that travel lasts 2,62% longer).
 
 ```timeTravel:``` Total driving time [in minutes] taking into consideration traffic factor (eg. 64).
 
 ```restpoints:``` List of valid respoints proposed by algorithm for stops or ```'Shorter'``` string if a stop is not needed.
 
 ```impassableObjects:``` List of impassable infrastructure object if the sum of removal cost is lower than a cost declared by the operator (eg. ```[{'identity': 1122, 'name': 'Oznakowanie pionowe', 'milestone': 209.8, 'number': ['50'], 'latitude': 52.150281, 'longitude': 21.504701}]```.
 
 ```impassableRoundabouts:``` List of impassable roundabouts if the sum of rebuilding is lower than a cost declared by the operator.
 
 ```cost:``` Total cost [in dollars] of dismantling/rebuilding infrastructure of the road (eg. 200).
 
 ```weather:``` List of roads where the weather is assessed as bad.
 
 ```weatherIndex:``` A weighted average taking into account the length of sections of individual roads and the amount of precipitation on them (eg. 0.2626).
 
 ```safetyIndex:```  A parameter taking into account both congestion and the amount of precipitation on the route (eg. 0.2868).

# Neo4j Graph Database structure
![neo4j_struct](https://github.com/betanddontcare/RouteMighty/assets/31188390/a5318089-d160-468b-9028-088fdedcd3fd)

## Node objects
<details>

<summary>Node</summary>

```name:``` Node name (eg. "5th Street/6th Street corner").
  
```latitude:``` Latitude coords (eg. 52.737228).
  
```longitude:``` Longitude coords (eg. 19.995445).
</details>
<details>

<summary>Road</summary>
  
```lat1:``` Latitude of starting node (eg. 52.149095).
  
```lat2:``` Latitude of ending node (eg. 52.219148).
  
```midLatitude:``` Latitude of the point located halfway between starting and ending nodes (eg. 52.18413180707769).
  
```lon1:``` Longitude of starting node (eg. 20.105352).
  
```lon2":``` Longitude of ending node (eg. 20.204114).
  
```midLongitude:```  Longitude of the point located halfway between starting and ending nodes (eg. 20.15469410414446).
  
```maxAxleLoad:``` Maximum axle load (in tonnes) acceptable on the road (eg. 115.0).
  
```numbers:``` List of road numbers (eg. ["92", "82"]).
  
```trafficFactor:``` Traffic factor reflects how much longer or shorter the time required to cover the distance between the nodes $v$ and $v'$ is in relation to the historical average travel time (eg. 1.0262). This data is relisable by Distance Matrix API service provided by Google Maps.
  
```type:```  Type of the road to calculate average speed: A - highway; S - expressway; GP fast traffic trunk road; G main road.
  
```kmRange:``` Boundary chainage of the road (eg. [410.068, 420.628].
  
```width:``` Width (in millimeters) of the road (eg. 7000).

```name:``` Name of the road (eg. "Gr. Woj. - Sochaczew").
  
```lines:``` Number of lines in single direction on the road (eg. 1).

```direction:``` Possible direction of travel: "TWO_WAY", "ONE_WAY".

</details>
<details>

<summary>Obstacle</summary>
  
```milestone:``` Chainage where the object occurs (eg. 430.48).
  
```immovable:``` Boolean. Possibility to remove the object: True/False.
  
```city:``` Name of the city where the object is located (eg. "Kopiska").
  
```latitude:``` Latitude of the object (eg. 52.1192).
  
```longitude:``` Longitude of the object (eg. 20.507849).
  
```name:``` Name of the object (eg. "St. Paul's Bridge").

</details>
<details>

<summary>HeightObstruction</summary>
  
```limit:``` Height limit (maximum value in millimeters) of the object (eg. 5000).
  
```range:``` Difference between the lowest and the highest point of the height limiting object: 0 - if the limiting object height is the same in every point over the road; >0 is the profile of the object is inclined relative to the road.
  
```subtype:``` Type of the object (eg. "OVERPASS").
  
```profile:``` Shape of the profile over the road. In this version there is only one type available: "LINE".
  
```removalCost:``` Cost of removing/rebuiling the object (eg. 50000).

</details>
<details>

<summary>WidthObstruction</summary>
  
```ranges:``` Height ranges on which particular width constraints occur (eg. [500, 1500]. This parameter is connected with ```limits```.
  
```limits:``` Width restriction values for individual height ranges calculated from the center of the roadway (eg. [4000, 5000]). In this version there is no possibility to reflect the non symmetric object, which is limiting the width from both sides in different ways.
  
These two above example variables means that the object has width limitation: 1. 4000 mm from the center of the road towards the shoulder to a height of 500 mm above the road; 2. 5000 mm from the center of the road towards the shoulder on the height between 500 mm and 1500 mm.

```subtype:``` Type of the object (eg. "TUNNEL").
 
```symmetric:``` Boolean. Is the object symmetric: True/False.
  
```removalCost:``` Cost of removing/rebuiling the object (eg. 50000).

</details>
<details>

<summary>WeightObstruction</summary>
  
```subtype:``` Type of the object (eg. "BRIDGE").
  
```mlc:``` Military Load Classification IAW NATO STANAG 2021 [Guide](https://www.osti.gov/servlets/purl/531084/) (eg. 150). In this version MLC was used in accordance of data availability. The method based on bridge MLC and vehicle MLC comparison.
  
```removalCost:``` Cost of removing/rebuiling the object (eg. 50000).

</details>
<details>

<summary>CurvatureObstruction</summary>

In this version the bend is described as an arc of a perfect circle.
  
```outerRadius:``` Outer radius (in millimeters) of the bend (eg. 30000).

```innerRadius:``` Inner radius (in millimeters) of the band (eg. 23000).
  
```boundaryRadius:``` The radius of the obstacle inside the bend (eg. 0 - if there is no such object).

```outerLimit:``` The radius of the obstacle outside the bend (eg. 31000 - if the object is located 1000 mm beyond the outer curb of the road).

```removalCost:``` Cost of removing/rebuiling the object (eg. 50000).

</details>
<details>

<summary>ElevationObstruction</summary>
  
```verticalCurveRadius:``` Vertical radius (in millimeters) of the curve (eg. 200000). In this version the curve is described as an arc of a perfect circle.
  
```removalCost:``` Cost of removing/rebuiling the object (eg. 50000).

</details>
<details>

<summary>Roundabout</summary>

In this version the roundabout is described as a perfect circle.
  
```outerRadius:``` Outer radius (in millimeters) of the roundabout (eg. 20000).
  
```innerRadius:``` Inner radius (in millimeters) of the roundabout (eg. 11000).
  
```verticalIsland:``` The radius of the central island inside the roundabout (eg. 8000).
  
```outerLimit:```  The radius of the obstacle outside the rounadabout (eg. 22000 - if the object is located 2000 mm beyond the outer curb of the roundabout).
  
```open:``` Boolean. Is it possible to drive straight through the roundabout : True/False.
  
```removalCost:``` Cost of removing/rebuiling the object (eg. 50000).

</details>
<details>

<summary>RestPoint</summary>
  
```slotLength:``` Length (in millimeters) of single slot for truck (eg. 20000).
  
```slotWidth:``` Width (in millimeters) of single slot for truck (eg. 4000).
  
```restpointType:``` Type of respoint (eg. "PRIVATE").
  
```occupancy:``` The average occupancy (in percent) of the parking (eg. 0.36). The data structure enables connection to the system that checks the load on parkings.
  
```hazardousSlots:``` Number of slots dedicated to truck with hazardous cargo (eg. 0 - if there is no slots).
  
```lighting:``` Boolean. Is there lighting in the parking : True/False.
  
```cctv:``` Boolean. Is there a monitoring system in the parking : True/False.
  
```security:``` Boolean. Is there a security guard in the parking : True/False.
  
```barriers:``` Boolean. Is there a security guard in the parking : True/False.
  
```milestone:``` Chainage where the parking occurs (eg. 413.8).
  
```oversizeWidth:``` The width of the parking area possible to use for abnormal vehicle (eg. 0 - if there is no additional operational space).
  
```oversizeLength:``` The length of the parking area possible to use for abnormal vehicle (eg. 0 - if there is no additional operational space).
  
```roadNumber:``` The number of road near which the parking occurs (eg. "S7")
  
```generalSlots:``` Number of slots dedicated to typical trucks (eg. 20).
 
 For more information please read my paper [Parking Lots Assignment Algorithm for Vehicles Requiring Specific Parking Conditions in Vehicle Routing Problem](https://ieeexplore.ieee.org/document/9628073)
  
</details>
<details>

<summary>Subnode</summary>
  
```subID:``` The id of ```Node``` to which ```Subnode``` refers (eg. 16).
  
```name:``` Subnode name - the same as ```Node``` (eg. "Ostrzykowizna")

</details>

## Relationships

```STARTS``` – reflects the possibility of moving from a given ```Node``` by ```Road```;

```ENDS``` - representing the possibility of reaching a ```Node``` by ```Road```;

```IS_ROUNDABOUT``` – specifying that ```Node``` object type represents a roundabout intersection;

```EXIT``` – representing the possibility of exiting the roundabout (node type interchange) onto the ```Road```;

```IS_LOCATED_ON``` – specifying that in the ```Node``` it is possible to reach the parking (```RestPoint```);

```OBSTRUCTS``` – specifying that the ```Obstacle``` is a restriction on the ```Road```;

```HAS``` – determining the existence of a constraint of a certain type for an ```Obstacle```;

```ROAD``` – which is the relational equivalent of the Road in the routes graph. This relation should consist parameter ```subID``` which refers to specific ```Road``` object (eg. 143).

# Validation functions explanation
## Height validation
![height_gh](https://github.com/betanddontcare/RouteMighty/assets/31188390/dbd91fb5-a4c0-4f24-bc40-3632cd13564f)

The necessity to remove the restriction may result from the height of the obstacle, and the analysis of the possibility of driving under it was carried out according to the following assumptions:

• the profile is a straight line parallel to the plane of the road or is inclined at the angle ```range```;

• when driving under the object, no part of the vehicle located at the ```vHeight``` may protrude beyond the outline of the road.

For the situation presented in Figure, three conditions of passage were distinguished:
1. when ```range = 0``` - the height of the vehicle ```vHeight``` must be less than the ```limit```:
```math
vHeight < limit
```
2. when ```range > 0``` and
```math
limit - vHeight > tan(range) * width
```
then the vehicle can take either side of the road,

3. when ```range > 0``` and 
```math
limit - vHeight < tan(range) * width
```
then the vehicle can pass under the object with as long as the condition is met:
```math
vWidthTop < \frac{limit - vHeight}{tan(range)}
```

## Curve validation
![curvegit](https://github.com/betanddontcare/RouteMighty/assets/31188390/f491a21f-c5eb-4cf1-b871-e977cb3f4c3a)

The presence of the limiting object may generate the need to drive through a horizontal curve (bend). For such a variant it was assumed that:

• the inside and outside profile of the bend is part of a circle;

• the sum of the distance from the last axle to the fifth wheel, the distance between the inner edges of the wheels on a single axle and twice the tire width does not exceed twice the outer radius of the turn;

• the limiting object always has a height resulting in potential contact with the maneuvering vehicle.

Analyzing Figure, 4 possible scenarios can be distinguished, occurring when:
1. ```outerLimit = 0``` and ```boundaryRadius = 0``` - in this situation the vehicle moves in such a way that the right wheel of the last axle of the semi-trailer/vehicle moves as close as possible to the outer edge of the turn in order to minimize the turning angle this axis:
```math
vAngle \geq 90^{\circ} - cos^{-1} (\frac{\frac{vLastAxle - vBolt}{2}}{outerRadius - vTireWidth - \frac{vSpacing}{2}})
```

2. ```outerLimit > 0``` and ```boundaryRadius = 0``` - in this situation, point A (rear right corner of the semi-trailer/vehicle) moves with maximum proximity to the limiting object lying on a circle with radius ```outerLimit``` and for this condition the steering angle is checked, which must be smaller than the last axle's declared by the manufacturer:

 ```math
vAngle \geq tan^{-1} (\frac{\frac{vLastAxle - vBolt}{2}}{\sqrt{outerLimit^2 - (vLength - vLastAxle + \frac{vLastAxle - vBolt}{2})^2 - \frac{vWidth}{2}}})
```

In addition, the distance of the left wheel of the axle lying directly behind the apparent non-steering axle of the semi-trailer/vehicle from the inner curb of the turn is checked:

```math
innerRadius + vTireWidth + \frac{vSpacing}{2} < \sqrt{(\sqrt{outerLimit^2 - (vLength - vLastAxle + \frac{vLastAxle - vBolt}{2})^2} - \frac{vWidth}{2})^2 + (vFirstAxle - vBolt - \frac{vLastAxle - vBolt}{2})^2}
```

3. ```outerLimit = 0``` and ```boundaryRadius > 0``` - in this situation the vehicle moves in such a way that the right wheel of the last axle of the semi-trailer/vehicle moves as close as possible to the outer edge of the turn in order to minimize the turning angle this axis and it is a condition analogous to the condition described by formula from point 1. Moreover, point B (the point of closest approach to the center of the turn) cannot exceed the limit determined by the radius ```boundaryRadius```:

```math
boundaryRadius < \sqrt{(outerRadius - vTireWidth - \frac{vSpacing}{2})^2 - (\frac{vLastAxle - vBolt}{2})^2} - \frac{vWidth}{2}
```

4. ```outerLimit > 0``` and ```boundaryRadius > 0``` - in this situation, point A (rear right corner of the semi-trailer/vehicle) moves with maximum proximity to the limiting object lying on a circle with radius ```outerLimit``` and for this condition the turning angle is checked - the condition is analogous to the condition described in formula from point 1. In addition, for such a scenario, it should be checked whether point B will not be within the zone defined by the radius ```boundaryRadius```:

```math
vWidth + boundaryRadius < \sqrt{outerLimit^2 - (vLength - vLastAxle + \frac{vLastAxle - vBolt}{2})^2}
```

and the condition described by second formula from point 2.

## Roundabout validation
![ra](https://github.com/betanddontcare/RouteMighty/assets/31188390/47b149c6-deb1-4f58-b204-d49e51fef6e7)

The analysis of the possibility of driving through the roundabout will be based on the following assumptions:
• the sum of the distance from the last axle to the fifth wheel, the distance between the inner edges of the wheels on a single axle and twice the tire width does not exceed the outer diameter of the roundabout;

• if an external limiting object exists, then its radius is greater than the distance between the apparent non-steering axle and the rear edge of the vehicle/semi-trailer;

• if there is a limiting object on the roundabout, then regardless of the chosen direction of travel (turn right, drive straight ahead, etc.) and the actual location of this object, it is assumed that it will be at the height of the maneuvering vehicle (it will make contact or the vehicle will move at a safe distance from this object);

• the limiting object always has a height resulting in potential contact with the maneuvering vehicle;

• limiting objects located near the roundabout do not hinder both entry and exit to/from the roundabout.

The developed model distinguishes 5 possible scenarios for which the fulfillment of particular conditions will affect the cost of driving through the roundabout. These scenarios occur when:
1. ```outerLimit = 0``` and ```verticalIsland = 0``` - in this situation, the vehicle moves in such a way that the right wheel of the last axle of the semi-trailer/vehicle moves as close as possible to the outer edge of the roundabout in order to minimize the steering angle of this axis:

```math
vAngle \geq 90^{\circ} - cos^{-1} (\frac{\frac{vLastAxle - vBolt}{2}}{outerRadius - vTireWidth - \frac{vSpacing}{2}})
```

2. ```outerLimit > 0``` and ```verticalIsland = 0``` – in this situation, point A (rear right corner of the semi-trailer/vehicle) moves with maximum proximity to the limiting object lying on a circle with radius ```outerLimit``` and for this condition the turning angle, which must be smaller than the turning angle of the last axle declared by the manufacturer:

 ```math
vAngle \geq tan^{-1} (\frac{\frac{vLastAxle - vBolt}{2}}{\sqrt{outerLimit^2 - (vLength - vLastAxle + \frac{vLastAxle - vBolt}{2})^2 - \frac{vWidth}{2}}})
```

In addition, the distance of the left wheel of the axle lying directly behind the apparent non-steering axle of the semi-trailer/vehicle from the inner curb of the roundabout is checked:

```math
innerRadius + vTireWidth + \frac{vSpacing}{2} < \sqrt{(\sqrt{outerLimit^2 - (vLength - vLastAxle + \frac{vLastAxle - vBolt}{2})^2} - \frac{vWidth}{2})^2 + (vFirstAxle - vBolt - \frac{vLastAxle - vBolt}{2})^2}
```

3. ```outerLimit = 0``` and ```verticalIsland > 0``` - in this situation, the vehicle moves in such a way that the right wheel of the last axle of the semi-trailer/vehicle moves as close as possible to the outer edge of the roundabout in order to minimize the turning angle of this axis and this is a condition analogous to the condition described by formula from point 1. What's more, point B (the point of closest approach to the center of the roundabout/horizontal curve) cannot exceed the border determined by the radius ```verticalIsland```:

```math
verticalIsland < \sqrt{(outerRadius - vTireWidth - \frac{vSpacing}{2})^2 - (\frac{vLastAxle - vBolt}{2})^2} - \frac{vWidth}{2}
```

4. ```outerLimit > 0``` and ```verticalIsland > 0``` – in this situation, point A (rear right corner of the semi-trailer/vehicle) moves with maximum proximity to the limiting object lying on a circle with radius ```outerLimit``` and for this condition the turning angle - a condition analogous to the condition described in formula from point 1. In addition, for such a scenario, it should be checked whether point B will not be within the zone defined by the radius ```verticalisland```:

```math
vWidth + verticalIsland < \sqrt{outerLimit^2 - (vLength - vLastAxle + \frac{vLastAxle - vBolt}{2})^2}
```

and the condition described by second formula from point 2.
5. ```open = 1``` - in this situation, due to the properties of the roundabout, it is possible to drive straight ahead or in any other direction without having to check other conditions.

## Width validation
![wth_merg](https://github.com/betanddontcare/RouteMighty/assets/31188390/9bd9f9ef-5575-4306-b4e1-7a11a49571ba)

The travel restriction may also be related to the width of the vehicle. The possibility of driving through the structure limiting the horizontal clearance was considered according to the following assumptions:
1. the maximum width of the vehicle and the maximum limitation of the horizontal clearance occur only in one height range;
2. when passing through an object limiting the horizontal clearance, the vehicle moves in the center of the road axis - in the case of symmetry of the object, and otherwise:
   
• if 

```math
limits < \frac{width}{2}
```

then it moves maximally close to the limiting object,

• if 

```math
limits > \frac{width}{2}
```

then it moves maximally close to the edge of the roadway lying on the opposite side of the limiting object whose distance from the center of the roadway is ```limits```.

The variant in which there is no symmetry and where on both sides above the road surface there are objects limiting the extreme horizontal has been omitted in the work.
in the case of both symmetry and lack of symmetry of the structure, the horizontal clearance may be limited from the ground level (outside the road outline) and at a certain height (above the road surface).

Analyzing Figure, four situations can be distinguished:
1. when ```symmetric = 1``` and

```math
min(limits) > \frac{width}{2}
```

this limitation occurs from the ground level outside the road outline, where the passage condition is specified in following way:

```math
vWidth < 2min(limits)
```

2. when ```symmetric = 1``` and

```math
min(limits) < \frac{width}{2}
```

the restriction is over the road. If 

```math
min(limits) < \frac{width}{2}
```

then in such a situation it should be checked whether for the height range at which the maximum width of the vehicle occurs there will be contact with the object. Otherwise, the vehicle can pass unrestricted.

3. when ```symmetric = 0``` and

```math
min(limits) < \frac{width}{2}
```

then the restriction is above the road surface on one side. The vehicle can pass through the facility unhindered if the following condition is met:

```math
\frac{vWidth}{2} - min(limits) + \frac{vSpacing}{2} + vTireWidth < \frac{width}{2}
```

Otherwise, check condition from point 2.

4. when ```symmetric = 0``` and

```math
min(limits) > \frac{width}{2}
```

then the restriction occurs on both sides of the road from the ground level. The condition of keeping the vehicle wheels in the road zone is presented below:

```math
\frac{vWidth}{2} + \frac{vSpacing}{2} + vTireWidth < \frac{3width}{2}
```

In addition, the condition of no contact with the limiting object whose distance from the center of the roadway is ```limits``` must also be met:

```math
vWidth - width < min(limits)
```

## Elevation validation
![elevat](https://github.com/betanddontcare/RouteMighty/assets/31188390/8336deda-78ac-466c-809e-13932b1a31a8)
