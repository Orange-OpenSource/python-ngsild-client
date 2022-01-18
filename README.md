# The ngsildclient library

## Overview

 **ngsildclient** is a Python library that helps building NGSI-LD entities and interacting with a NGSI-LD Context Broker.

 While the library primary purpose is to **ease and speed up the development of a NGSI Agent**, it's also **valuable for Data Modeling in the design stage** especially in interactive mode *with the help of autocompletion* - such as in Python console or in Jupyter notebook.

## Key Features

### Build NGSI-LD entities

The task of building a large NGSI-LD compliant entity is tedious, error-prone and results in a significant amount of code. 

By providing primitives to add properties and metadata in respect with the ETSI specification **ngsildclient** allows to build and manipulate NGSI-LD compliant entities without effort.

### Implement the NGSI-LD API

**ngsildclient** provides a NGSI-LD API Client implementation.

Acting as a Context Producer/Consumer **ngsildclient** is able to send/receive NGSI-LD entities to/from the Context Broker for creation and other operations.

As of v.01 it covers a subset of the API that consists of the ``/entities/{entityId}`` endpoint.

## Smart Building Demo

How to build the NGSI-LD [example](https://smart-data-models.github.io/dataModel.Building/Building/examples/example-normalized.jsonld) from the [Smart Data Models Initiative](https://smartdatamodels.org/), and ask the Context Broker to create it.

[![demo](https://asciinema.org/a/r328sRBCoKiDHuJHiBXNnQxqF.svg)](https://asciinema.org/a/r328sRBCoKiDHuJHiBXNnQxqF?autoplay=1&theme=solarized-dark&speed=3)


## Where to get it

The source code is currently hosted on GitHub at :
https://github.com/Orange-OpenSource/python-orion-client

Binary installer for the latest released version is available at the [Python
package index](https://pypi.org/project/ngsildclient).

```sh
pip install ngsildclient
```

## Installation

**ngsildclient** requires Python 3.9+.

One should use a virtual environment. For example with pyenv.

```sh
mkdir myfiwareproject && cd myfiwareproject
pyenv virtualenv 3.10.1 myfiwareproject
pyenv local
pip install ngsildclient
```

## Getting started

### Build your first NGSI-LD entity

```python
from datetime import datetime
from ngsildclient import Entity

# No context provided => defaults to NGSI-LD Core Context
entity = Entity("AirQualityObserved", "RZ:Obsv4567")

# Once we've created our entity by calling the Entity() constructor 
# We can add properties thanks to primitives

# tprop() sets a TemporalProperty
entity.tprop("dateObserved", datetime(2018, 8, 7, 12))

# gprop() sets a GeoProperty : Point, Polygon, ...
entity.gprop("location", (44, -8))

# prop() is used for other properties
entity.prop("PM10", 8).prop("NO2", 22, unitcode="GP", userdata={"reliability": 0.95})

# rel() sets a Relationship Property
entity.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")

entity.pprint()
```

The resulting JSON looks like this :

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
  ],
  "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
  "type": "AirQualityObserved",
  "dateObserved": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2018-08-07T12:00:00Z"
    }
  },
  "PM10": {
    "type": "Property",
    "value": 8
  },
  "NO2": {
    "type": "Property",
    "value": 22,
    "unitCode": "GP",
    "reliability": 0.95
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [
        -8,
        44
      ]
    }
  },
  "refPointOfInterest": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"
  }
}
```

Once you're satisfied with it, you can save it to a file to share it, for example with the [Smart Data Models Initiative](https://smartdatamodels.org/).

```python
entity.save("air_quality_sample.jsonld")
```

Or you can send it to the NGSI-LD Context Broker for creation.

### Interact with the NGSI-LD Orion broker

```python
from ngsildclient import Entity, SmartDataModels, Client

# This time we don't create our own entity but download a sample from the Smart Data Models Initiative
farm = Entity.load(SmartDataModels.SmartAgri.Agrifood.AgriFarm)

# We can visualize it : here we would like the simplified representation (aka KeyValues)
farm.pprint(kv=True)

# We could add/update properties using the prop primitives as we did previously
# For the sake of example we'll just update the phone number, using the dot notation facility
farm["contactPoint.value.telephone"] = "00349674538"

# Send it to the Context Broker for creation
# Here you need a Context Broker up and running
# You can find some ready-to-use docker-compose files in the brokers/ folder
# Without any arguments the client targets localhost and the default port
with Client() as client:
    client.create(farm)

# Later you'll be able to retrieve the entity from the broker and resend it for update
with Client() as client:
    # retrieve the entity by its id
    farm = client.retrieve("urn:ngsi-ld:AgriFarm:72d9fb43-53f8-4ec8-a33c-fa931360259a")
    # It would also work by passing the entity - in case it's still in memory
    # farm = client.retrieve(farm)
    farm["contactPoint.value.telephone"] = "00349674539"
    client.update(farm)
```

## License

[Apache 2.0](LICENSE)

## Documentation

Docstrings are widely used in the code.

For example.

```python
from ngsildclient import Entity

help(Entity)
```

For examples (from basic to more complex and realistic) you can have a look at the ``tests`` folder.

Especially the ``tests/test_entity.py`` file that builds basic entities.

And inside the ``tests/smartdatamodels`` folder that builds some sample entities from the Smart Data Models Initiative.

## Roadmap

- Add authentication
- Extend API coverage : add support for query, batch operations and subscriptions
- Add documentation
