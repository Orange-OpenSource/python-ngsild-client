Get started
===========

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