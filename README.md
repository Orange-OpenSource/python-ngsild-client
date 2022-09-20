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

 **ngsildclient** is a Python library that helps building NGSI-LD entities and allows to interact with a NGSI-LD Context Broker.

 The library primary purpose is to ease and **speed up the development of a NGSI Agent**.
 
 It also can be of interest *especially in a Jupyter notebook or in an interactive interpreter* :
 - to **design new DataModels**
 - to **explore and manipulate entities stored in a broker**
 - for **demos**, quick **proofs of concept** or **eductional purposes**

## Key Features

### Build NGSI-LD entities

The task of building a large NGSI-LD compliant entity is tedious, error-prone and results in a significant amount of code. 

**ngsildclient** provides primitives to build and manipulate NGSI-LD compliant entities without effort, in respect with the [ETSI specifications](https://www.etsi.org/committee/cim).

### Implement the NGSI-LD API

**ngsildclient** provides a NGSI-LD API Client implementation.

Acting as a Context Producer/Consumer **ngsildclient** is able to send/receive NGSI-LD entities to/from the Context Broker for creation and other operations.

The library wraps a large subset of the API endpoints and supports batch operations, queries, subscriptions.

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

## Getting started

The following code snippet builds a NGSI-LD entity related to a measure of air quality in Bordeaux then sends it to the Context Broker.

```python
from ngsildclient import Entity, Client

e = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
e.tprop("dateObserved").gprop("location", (44.84044, -0.5805))
e.prop("PM25", 12, unitcode="GP").prop("PM10", 18, unitcode="GP")
e.prop("NO2", 8, unitcode="GP").prop("O3", 83, unitcode="GP")
e.rel("refDevice", "Device:AirProbe42")
with Client() as client:
    client.upsert(e)
```

The corresponding JSON-LD [payload](https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/samples/gettingstarted.json) has been generated.

Already have a NGSI-LD entity available in JSON format ? Simply use `Entity.load()`.

## Asynchronous Client

Alternatively you can prefer the Asynchronous Client, typically when user interactivity is not needed and seeking for performance - i.e. writing a real-time NGSI-LD agent.


```python
from ngsildclient import AsyncClient

async with AsyncClient() as client:
    await client.upsert(e)
```

## Documentation

User guide is available on [Read the Docs](https://ngsildclient.readthedocs.io/en/latest/index.html).

Please refer to the [Cookbook](https://ngsildclient.readthedocs.io/en/latest/cookbook.html) chapter that provides many HOWTOs to :

- develop various NGSI-LD Agents collecting data from heterogeneous datasources
- forge official NGSI-LD Entities from the Smart Data Models initiative

## License

[Apache 2.0](LICENSE)
