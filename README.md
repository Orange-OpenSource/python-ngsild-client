# The ngsildclient library

[![NGSI-LD badge](https://img.shields.io/badge/NGSI-LD-red.svg)](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.02.01_60/gs_CIM009v010201p.pdf)
[![SOF support badge](https://nexus.lab.fiware.org/repository/raw/public/badges/stackoverflow/fiware.svg)](http://stackoverflow.com/questions/tagged/fiware)
<br>
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Read the Docs](https://img.shields.io/readthedocs/ngsildclient)](https://ngsildclient.readthedocs.io/en/latest/index.html)
<br>
[![deploy status](https://github.com/Orange-OpenSource/python-ngsild-client/workflows/CI/badge.svg)](https://github.com/Orange-OpenSource/python-ngsild-client/actions)
[![PyPI](https://img.shields.io/pypi/v/ngsildclient.svg)](https://pypi.org/project/ngsildclient/)
[![Python version](https://img.shields.io/pypi/pyversions/ngsildclient)](https://pypi.org/project/ngsildclient/)


## Overview

 **ngsildclient** is a Python library dedicated to NGSI-LD.
 
 It combines :

 - a toolbox to create and modify NGSI-LD entities effortlessly
 - a NGSI-LD API client to interact with a Context Broker

## Features

### Build NGSI-LD entities

ngsildclient aims at :

- programatically generate NGSI-LD entities
- load entities from JSON-LD payloads

Four primitives are provided `prop()`, `gprop()`, `tprop()`, `rel()` to build respectively a Property, GeoProperty, TemporalProperty and Relationship.

An Entity is backed by a Python dictionary that stores the JSON-LD payload.
The library operates the mapping between the Entity's attributes and their JSON-LD counterpart, allowing to easily manipulate NGSI-LD value and metadata directly in Python.

### Features list

- primitives to build properties and relationships (chainable)
- benefit from uri naming convention, omit scheme and entity's type, e.g. `parking = Entity("OffStreetParking", "Downtown1")`
- support dot-notation facility, e.g. `reliability = parking["availableSpotNumber.reliability"]`
- easily manipulate a property's value, e.g. `reliability.value = 0.8`
- easily manipulate a property's metadata, e.g. `reliability.datasetid = "dataset1"`
- support nesting
- support multi-attribute
- load/save to file
- load from HTTP
- load well-known sample entities, e.g.  `parking = Entity.load(SmartDataModels.SmartCities.Parking.OffStreetParking)`
- provide helpers to ease building some structures, e.g. PostalAddress
- pretty-print entity and properties

### Interact with the Context Broker

Two clients are provided, `Client` and `AsyncClient` respectively for synchronous and asynchronous modes.

Prefer the synchronous one when working in interactive mode, for example to explore and visualize context data in a Jupyter notebook.
Prefer the async one if you're looking for performance, for example to develop a real-time NGSI-LD Agent with a high data-acquisition frequency rate.

### Features list

 - synchronous and asynchronous clients
 - support batch operations
 - support pagination : transparently handle pagination (sending as many requests as needed under the hood)
 - support auto-batch : transparently divide into many batch requests if needed
 - support queries and alternate (POST) queries
 - support temporal queries
 - support pandas dataframe as a temporal query result
 - support subscriptions
 - find subscription conflicts
 - SubscriptionBuilder to help build subscriptions
 - auto-detect broker vendor and version
 - support follow relationships (chainable), e.g. `camera = parking.follow("availableSpotNumber.providedBy")`

## Getting started

### Create our first parking Entity

The following code snippet builds the `OffstreetParking` sample entity from the ETSI documentation.

```python
from datetime import datetime
from ngsildclient import Entity

PARKING_CONTEXT = "https://raw.githubusercontent.com/smart-data-models/dataModel.Parking/master/context.jsonld"

e = Entity("OffStreetParking", "Downtown1")
e.ctx.append(PARKING_CONTEXT)
e.prop("name", "Downtown One")
e.prop("availableSpotNumber", 121, observedat=datetime(2022, 10, 25, 8)).anchor()
e.prop("reliability", 0.7).rel("providedBy", "Camera:C1").unanchor()
e.prop("totalSpotNumber", 200).loc(41.2, -8.5)
```

Let's print the JSON-LD payload.

```python
e.pprint()
```

The result is available [here](https://raw.githubusercontent.com/Orange-OpenSource/python-ngsild-client/master/parking_sample.jsonld).<br>


### Persist our parking in the Context Broker

The following example assumes that an Orion-LD context broker is running on localhost.<br>
A docker-compose config [file](https://raw.githubusercontent.com/Orange-OpenSource/python-ngsild-client/master/brokers/orionld/docker-compose-troe.yml) file is provided for that purpose.

```python
from ngsildclient import Client

client = Client(port=8026, port_temporal=8027)
client.create(e)
```

### Increase our parking occupancy as the day goes on

Each hour ten more parkings spots are occupied, until 8 p.m.

```python
from datetime import timedelta

prop = e["availableSpotNumber"]
for _ in range(12):
    prop.observedat += timedelta(hours=1)
    prop.value -= 10
    client.update(e)
```

### Retrieve our parking

Get back our parking from the broker and display its `availableSpotNumber` property.<br>

```python
parking = client.get("OffStreetParking:Downtown1", ctx=PARKING_CONTEXT)
parking["availableSpotNumber"].pprint()
```

Only one available parking spot remains at 8 p.m.

```json
{
    "type": "Property",
    "value": 1,
    "observedAt": "2022-10-25T20:00:00Z",
    "reliability": {
        "type": "Property",
        "value": 0.7
    },
    "providedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Camera:C1"
    }
}
```

### Request the Temporal Representation of our parking

For convenience we retrieve it as a pandas dataframe.

*If you don't have pandas installed, just omit the `as_dataframe` argument and get JSON instead.*

```python
df = client.temporal.get(e, ctx=PARKING_CONTEXT, as_dataframe=True)
```

Let's display the three last rows.

```python
df.tail(3)
```

|    | OffStreetParking   | observed                  |   availableSpotNumber |
|---:|:-------------------|:--------------------------|----------------------:|
| 10 | Downtown1          | 2022-10-25 18:00:00+00:00 |                    21 |
| 11 | Downtown1          | 2022-10-25 19:00:00+00:00 |                    11 |
| 12 | Downtown1          | 2022-10-25 20:00:00+00:00 |                     1 |

### Let's throw in a more realistic parking management system

Let us move from our first example to the more realistic parking example provided by the Smart Data Models Program.

```python
from ngsildclient import SmartDataModels

parking = Entity.load(SmartDataModels.SmartCities.Parking.OffStreetParking)
```

Once loaded we can manipulate our new parking the same way we've done until now.<br>
For the moment just see how it is occupied.

```python
n_total = parking["totalSpotNumber"].value
n_occupied = parking["occupiedSpotNumber"].value
n_avail= parking["availableSpotNumber"].value
print(n_total, n_occupied, n_avail)
```

This parking has 414 parking slots. 282 are occupied. 132 are available.<br>
In order to complete our parking system we would like to add 414 spots to our datamodel.<br>
Let's create a reference parking spot to be used as a template.

```python
spot = Entity("ParkingSpot", "OffStreetParking:porto-ParkingLot-23889:000")
spot.prop("status", "free")
spot.rel("refParkingSite", parking)
```

Let's clone this spot 414 times, assign a disctinct id to each one and occupy the 282 first spots.<br>
This is a simplistic strategy but enough to keep the parking system consistent.

```python
spots = spot * n_total
for i, spot in enumerate(spots):
    spot.id = f"{spot.id[:-3]}{i+1:03}"
    if i < n_occupied:
        spot["status"].value = "occupied"
```

We now establish the relationship between the parking and its spots by adding a new attribute to the parking.<br>
Having a mutual relationship is not necessarily needed. It depends on how we want to navigate in our datamodel. <br>
Let's do it for the sake of example.

```python
from ngsildclient import MultAttrValue

mrel = MultAttrValue()
for spot in spots:
    mrel.add(spot, datasetid=f"Dataset:{spot.id[-26:]}")
parking.rel("refParkingSpot", mrel)
```

To sum up we have obtained 415 entities : 1 parking and 414 spots.<br>
Make a single list of these parts and save it into a file.

```python
datamodel = sum(([parking], spots), [])  # flatten lists
Entity.save_batch(datamodel, "parking_system.jsonld")
```
The result is available [here](https://raw.githubusercontent.com/Orange-OpenSource/python-ngsild-client/master/parking_system.jsonld).<br>
Time now to populate our parking system in the broker.

```python
client.upsert(datamodel)
```

Check everything is fine by asking the broker for the number of occupied spots.<br>
Eventually close the client.

```python
client.count("ParkingSpot", q='refParkingSite=="urn:ngsi-ld:OffStreetParking:porto-ParkingLot-23889";status=="occupied"')  # 282
client.close()
```

## Where to get it

The source code is currently hosted on GitHub at :
https://github.com/Orange-OpenSource/python-ngsild-client

Binary installer for the latest released version is available at the [Python
package index](https://pypi.org/project/ngsildclient).

## Installation

**ngsildclient** requires Python 3.9+.

```sh
pip install ngsildclient
```

## Documentation

User guide is available on [Read the Docs](https://ngsildclient.readthedocs.io/en/latest/index.html).

Refer to the [Cookbook](https://ngsildclient.readthedocs.io/en/latest/cookbook.html) chapter that provides many HOWTOs to :

- develop various NGSI-LD Agents collecting data from heterogeneous datasources
- forge NGSI-LD sample entities from the Smart Data Models initiative

## License

[Apache 2.0](LICENSE)
