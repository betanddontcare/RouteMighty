![rm](https://github.com/betanddontcare/RouteMighty/assets/31188390/af0f6a33-c0a6-4066-9ac9-3eda41aed941)

# RouteMighty 1.2.0
RouteMighty is a software application engine developed in Python for the efficient planning of routes for abnormal vehicles, such as those that are overweight or oversized.

![rm_arch](https://github.com/betanddontcare/RouteMighty/assets/31188390/5681e7e6-bbae-4432-a9f6-f9c5d188dc79)

# Requirements & Installation
Step 1: Install all the requirements before proceeding to next steps:

Example: Python >= 3.11.3

You should install all the python3 modules using the pip3 install *package_name* command.

(or alternatively using: sudo apt-get install python3-*package_name* conmmand)

Step 2: 

In order to successfully run the tool you need to:

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

For more information please read my paper [Parking Lots Assignment Algorithm for Vehicles Requiring Specific Parking Conditions in Vehicle Routing Problem](https://ieeexplore.ieee.org/document/9628073)
  
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
  
  
  "oversizeWidth": 0,
  "roadNumber": "S7",
  "generalSlots": 20,
  "oversizeLength": 0
}
```
</details>
<details>

<summary>Subnode</summary>
  
```
{
  "subID": 16,
  "name": "Ostrzykowizna"
}
```
</details>

## Relationships

# Validation functions
