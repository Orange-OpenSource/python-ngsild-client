ngsildclient documentation
==========================

Welcome to the **ngsildclient** documentation, where you can learn about ngsildclient and explore its features.

**ngsildclient** is a Python NGSI-LD client implementation.

| NGSI-LD_ has been standardized by the ETSI_ and is widely used in the Fiware_ ecosystem.
| **ngsildclient** is based on the NGSI-LD API ETSI Specification [ETSI_GS_CIM_009_V1.5.1]_.


Project Goals
-------------

The ngsildclient Python library has two main objectives.

1. :ref:`Build NGSI-LD compliant entities<Build Entities>`

   | The task of writing large NGSI-LD compliant entities using JSON is tedious, error-prone and results in a significant amount of code.
   | ngsilclient provides primitives to build and manipulate NGSI-LD entities without effort, in respect with the ETSI specifications_.

2. :ref:`Wrap the NGSI-LD API<Interact with the broker>`

   | As a Python NGSI-LD client it allows to interact with a broker by sending and retrieving NGSI-LD entities.
   | As of v0.1.6 it supports a subset of the API.

Four practical use cases
------------------------

ngsildclient can be useful in practice to :

- **model a domain-specific system**  
   it has many benefits in the exploration phase : 

   - use the interactive mode to quickly build entities *thanks to Python REPL (console)*
   - use Jupyter notebooks to share and discuss about modeling
   - load and extend example entities from the Smart Data Model Initiatives
  

- **demonstrate feasibility**
   quickly develop a Proof Of Concept by :
   
   - populating the broker with your entities
   - query the broker to test relationships
  

- **develop a full NGSI-LD Agent**
   putting all parts together the NGSI-LD Agent :

   - collects incoming domain-specific data
   - converts data to NGSI-LD compliant entities
   - feed the NGSI-LD broker
  

- **administrate the broker**
   allow admin tasks in interactive mode :

   - purge entities
   - list contexts

Installation
------------

ngsildclient requires Python 3.9 or above.

It's recommended to use a virtual environment.

.. code-block:: bash
   :emphasize-lines: 5

   mkdir myagent && cd myagent
   pyenv virtualenv 3.9.10 myagent
   pyenv local myagent

   pip install ngsildclient

Getting started
---------------

Create a first very basic NGSI-LD entity.

.. code-block::

   from datetime import datetime
   from ngsildclient import Entity

   entity = Entity("AirQualityObserved", "RZ:Obsv4567")
   entity.tprop("dateObserved", datetime(2018, 8, 7, 12))
   entity.gprop("location", (44, -8))
   entity.prop("PM10", 8).prop("NO2", 22, unitcode="GP", userdata={"reliability": 0.95})
   entity.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")

   entity.pprint() # have a look at your just created entity

| Send it to the Broker for creation.
| *It assumes you have a broker instance running locally.*

.. code-block::

   from ngsildclient import Client

   with Client() as client:
    client.create(entity)

.. toctree::
   :hidden:

   Home Page <self>
   Build Entities <build>
   Interact with the Broker <client>
   Annex <annex>
   License <license>
   API Reference <_autosummary/ngsildclient>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. [ETSI_GS_CIM_009_V1.5.1] ETSI Group `Specification <https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.05.01_60/gs_CIM009v010501p.pdf>`_
   Context Information Management (CIM)
   NGSI-LD API
   v1.5.1
   2021-11
.. _NGSI-LD: https://en.wikipedia.org/wiki/NGSI-LD
.. _ETSI: https://www.etsi.org/
.. _Fiware: https://www.fiware.org
.. _specifications: https://www.etsi.org/committee/cim

