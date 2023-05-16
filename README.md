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

```
{
  "name": "Drobin",
  "latitude": 52.737228,
  "longitude": 19.995445
}
```
</details>
<details>

<summary>Road</summary>
  
```
{
  "lat1": 52.149095,
  "lat2": 52.219148,
  "midLongitude": 20.15469410414446,
  "maxAxleLoad": 115.0,
  "numbers": [
    "92"
  ],
  "trafficFactor": 1.0262,
  "type": "GP",
  "midLatitude": 52.18413180707769,
  "lon1": 20.105352,
  "lon2": 20.204114,
  "kmRange": [
    410.068,
    420.628
  ],
  "width": 7000,
  "name": "Gr. Woj. - Sochaczew",
  "lines": 1,
  "direction": "TWO_WAY"
}
```
</details>
<details>

<summary>Obstacle</summary>
  
```
{
  "milestone": 430.48,
  "immovable": true,
  "city": "Kopiska",
  "latitude": 52.1192,
  "name": "Most",
  "url": "",
  "longitude": 20.507849
}
```
</details>
<details>

<summary>HeightObstruction</summary>
  
```
{
  "limit": 5000,
  "range": 0,
  "subtype": "OVERPASS",
  "profile": "LINE",
  "removalCost": 5000000
}
```
</details>
<details>

<summary>WidthObstruction</summary>
  
```
{
  "ranges": [
    500,
    1500
  ],
  "subtype": "OTHER",
  "limits": [
    4000,
    5000
  ],
  "symmetric": true,
  "removalCost": 5000000
}
```
</details>
<details>

<summary>WeightObstruction</summary>
  
```
{
  "limit": 0,
  "subtype": "BRIDGE",
  "mlc": 150,
  "removalCost": 5000000
}
```
</details>
<details>

<summary>CurvatureObstruction</summary>
  
```
{
  "outerRadius": 30000,
  "boundaryRadius": 0,
  "innerRadius": 23000,
  "outerLimit": 0,
  "removalCost": 5000000
}
```
</details>
<details>

<summary>ElevationObstruction</summary>
  
```
{
  "verticalCurveRadius": 200000,
  "removalCost": 5000000
}
```
</details>
<details>

<summary>Roundabout</summary>
  
```
{
  "outerDiameter": 21000,
  "verticalIsland": 8000,
  "outerLimit": 0,
  "innerDiameter": 11000,
  "open": false,
  "removalCost": 5000000
}
```
</details>
<details>

<summary>RestPoint</summary>
  
```
{
  "slotLength": 20000,
  "restpointType": "PRIVATE",
  "occupancy": 0.36,
  "hazardousSlots": 0,
  "lighting": true,
  "cctv": false,
  "security": false,
  "barriers": true,
  "milestone": 413.8,
  "slotWidth": 4000,
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
