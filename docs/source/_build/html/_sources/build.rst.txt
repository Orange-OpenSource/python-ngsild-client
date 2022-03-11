Build Entities
==============

Create an entity
----------------

| Let's start by creating an empty entity - without any properties *yet*.
| We'll add properties in a next step.

A NGSI-LD entity is characterized by :

- a unique and fully qualified identifier
- the type the entity belongs to
- a context

| Don't worry about the context for now. We'll speak about it later.

1. The preferred way
~~~~~~~~~~~~~~~~~~~~

Provide :

- the type the entity belongs to
- a fully qualified identifier

.. code-block::
    
   from ngsilclient import Entity

   entity = Entity("AirQualityObserved", "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z")

Let's display our newly created entity

.. code-block::

   entity.pprint()


.. code-block:: json-ld
   :caption: AirQualityObserved empty NGSI-LD Entity

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z",
      "type": "AirQualityObserved"
   }

*Note that the library has assigned a default context.*

To simplify the code we can omit the scheme and namespace identifier.

.. code-block::

   entity = Entity("AirQualityObserved", "AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z")

| By convention the identifier string is prefixed with the type.
| We can simplify once again to obtain the following line.

.. code-block::
  :emphasize-lines: 1

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")

1. Alternate way
~~~~~~~~~~~~~~~~

One could provide the qualified identifier and let the library infer the type.

.. code-block::

   entity = Entity("urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z")

Which can be written.

.. code-block::
   :emphasize-lines: 1

   entity = Entity("AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z")

Specify a context
-----------------

| One can provide the Entity constructor with a context.
| If no context is provided it defaults to the NGSI-LD Core Context.
| The context variable is an array of strings.

1. Using the context property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

   from ngsilclient import Entity

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.context.append("https://github.com/smart-data-models/dataModel.Environment/blob/master/context.jsonld")

2. Using the constructor
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

   from ngsilclient import Entity, CORE_CONTEXT

   ctx = [ "https://github.com/smart-data-models/dataModel.Environment/blob/master/context.jsonld", 
            CORE_CONTEXT ]
   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z", ctx=ctx)

Add properties
--------------

Here we talk about properties in the broad sense, including relationships.

Primitives
~~~~~~~~~~

| The Entity class provides primitives, whose purpose is to generate JSON content representing a property.
| The latter property is attached to the Entity instance.
| Four primitives are available : **prop()**, **gprop()**, **tprop()** and **rel()** that allow respectively to set a **Property**, **GeoProperty**, **Temporal Property** and **RelationShip**.

| For convenience these methods can be chained in order to shorten the code.
| Properties have at least a name and value and can optionally carry metadata and userdata.

+--------------------+------------+
| property           | primitive  |
+====================+============+
| Property           | prop()     |
+--------------------+------------+
| GeoProperty        | gprop()    |
+--------------------+------------+
| Temporal Property  | tprop()    |
+--------------------+------------+
| Relationship       | rel()      |
+--------------------+------------+

.. code-block::
  :caption: Example

   from ngsilclient import Entity

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.prop("CO", 500).prop("NO", 45).prop("NO2", 69)

.. code-block:: json-ld
   :caption: AirQualityObserved NGSI-LD Entity with some pollutant concentrations

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z",
      "type": "AirQualityObserved",
      "CO": {
         "type": "Property",
         "value": 500
      },
      "NO": {
         "type": "Property",
         "value": 45
      },
      "NO2": {
         "type": "Property",
         "value": 69
      }      
   }

Metadata
~~~~~~~~

| Metadata aka "properties of properties" are : **unitCode**, **datasetId** and **observedAt**.
| Primitives accept metadata as arguments.
| Which ones are available depend on which property you're building.
| For example **unitCode** is available for a Property but not for a GeoProperty.

Corresponding arguments in lower case.

+------------+------------+
| metadata   | argument   |
+============+============+
| unitCode   | unitcode   |
+------------+------------+
| datasetId  | datasetid  |
+------------+------------+
| observedAt | observedat |
+------------+------------+

unitCode
^^^^^^^^

.. code-block::
  :caption: SO2 concentration with its measurement unit code

   entity.prop("SO2", 11, unitcode="GP") # milligram per cubic metre (UNECE/CEFACT)

datasetId
^^^^^^^^^

.. code-block::
  :caption: SO2 concentration with a datasetId

   entity.prop("SO2", 11, datasetid="dataset:01") # urn prefix omitted

observedAt
^^^^^^^^^^

.. code-block::
  :caption: SO2 concentration with the observation date

   from datetime import datetime, timezone

   entity.prop("SO2", 11, observedat=datetime(2016, 3, 15, 11, tzinfo=timezone.utc))

   # Alternatively one could pass directly an ISO8601 string
   # entity.prop("SO2", 11, observedat="2016-03-15T11:00:00Z")

| The library will always convert datetimes to UTC as expected by NGSI-LD.
| It's recommended to work with **aware** datetimes [1]_.

.. code-block::
  :caption: SO2 concentration with a CET observation date

   from datetime import datetime
   from zoneinfo import ZoneInfo

   CET = ZoneInfo("CET") # UTC+1
   entity.prop("SO2", 11, observedat=datetime(2016, 3, 15, 12, tzinfo=CET))

   # Alternatively one could pass directly an ISO8601 string
   # entity.prop("SO2", 11, observedat="2016-03-15T11:00:00Z")

| Often an observation date is the same that is used in the entity identifier to make it unique.
| And often the whole set of measures share the same observation date.
| The library caches the first datetime it encounters and allows to reuse it.

For the sake of example let's rewrite our entity.

.. code-block::
  :caption: Example

   from ngsildclient import Entity, Auto

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.prop("CO", 500, unitcode="GP", observedat=Auto)
   entity.prop("NO", 45, unitcode="GP", observedat=Auto)
   entity.prop("NO2", 69, unitcode="GP", observedat=Auto)
   entity.prop("SO2", 11, unitcode="GP", observedat=Auto)


.. code-block:: json-ld
   :caption: AirQualityObserved NGSI-LD Entity with all measures
   
   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z",
      "type": "AirQualityObserved",
      "CO": {
         "type": "Property",
         "value": 500,
         "unitCode": "GP",
         "observedAt": "2016-03-15T11:00:00Z"
      },
      "NO": {
         "type": "Property",
         "value": 45,
         "unitCode": "GP",
         "observedAt": "2016-03-15T11:00:00Z"
      },
      "NO2": {
         "type": "Property",
         "value": 69,
         "unitCode": "GP",
         "observedAt": "2016-03-15T11:00:00Z"
      },
      "SO2": {
         "type": "Property",
         "value": 11,
         "unitCode": "GP",
         "observedAt": "2016-03-15T11:00:00Z"
      }
   }

User data
~~~~~~~~~

| User data are additional custom metadata the user wants to be included in the property.
| You can use the **userdata** argument to provide your own dictionary.

| For example imagine you'd like to add to our AirQualityObserved entity a NOx measure with an accuracy indice.
| But you don't want to express this information as a property.
| *More on nested properties later*.

.. code-block::
  :caption: Example

   entity.prop("NOx", 119, userdata={"accuracy": 0.95})


.. code-block:: json-ld
   :caption: The NOx property with userdata
   
   "NOx": {
      "type": "Property",
      "value": 119,
      "accuracy": 0.95
   }

Property
~~~~~~~~

| We have already spoken of the Property in previous examples.
| That is a general Property that has a name and a value of any Python type that can be serialized to JSON.

.. code-block::
  :caption: A temperature property with a float value

   entity.prop("temperature", 22.5)

.. code-block::
  :caption: A description property with a List value

   entity.prop("description", [
      "https://example.org/concept/clay",
      "https://datamodel.org/example/clay"]
    }      

.. code-block::
  :caption: A description property with a string value

   entity.prop("description", "Corn farm")
    
| Considering strings, some characters are prohibited by the NGSI-LD broker.
| In this case you can set the escape argument to to escape the string.

.. code-block::
  :caption: A description property with a string value including forbidden characters

   entity.prop("description", "Corn farm (organic)", escape=True)

GeoProperty
~~~~~~~~~~~

| The GeoProperty as it name implies represents a geographic property.
| ngsildclient relies on the **geojson** library.
| As of now allowed *geojson* types are **Point**, **LineString**, **Polygon** and **MultiPoint**.

.. code-block::
  :caption: A simple GeoProperty

   from geojson import Point
   from ngsildclient import Entity

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.gprop("location", Point((-3.703790, 40.416775))) # Madrid

.. code-block:: json-ld
   :caption: A location geoproperty illustrated
   
   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z",
      "type": "AirQualityObserved",
      "location": {
         "type": "Property",
         "value": {
            "type": "Point",
            "coordinates": [
            -3.70379,
            40.416775
            ]
         }
      }
   }

| The Point is by far the most common geo type.
| ngsildclient accepts a tuple **(lat, lon)** to represent a Point, avoiding the need to invoke geojson for this simple case.

.. code-block::

   entity.gprop("location", (40.416775, -3.703790)) # Madrid

The **loc()** alias can be used to set this very common **location** GeoProperty.

.. code-block::

   entity.loc((40.416775, -3.703790)) # Madrid

Temporal Property
~~~~~~~~~~~~~~~~~

The Temporal Property accepts values of following types : **datetime**, **date** and **time**, or **ISO8601 string** representations of these latter.

.. code-block::
  :caption: Temporal Property illustrated

   from ngsildclient import Entity

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.tprop("dateObserved", "2016-03-15T11:00:00Z")

| In the above example the library has cached *at the entity creation time* the datetime that is part of the identifier.
| The **Auto** directive can be used to benefit from the cached datetime.

.. code-block::
  :caption: Temporal Property using the Auto keyword

   from ngsildclient import Entity, Auto

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.tprop("dateObserved", Auto)

The **obs()** alias can be used to set this very common **dateObserved** Temporal Property.

| The library will always convert datetimes to UTC as expected by NGSI-LD.
| It's recommended to work with **aware** datetimes [1]_.

.. code-block::

   entity.obs() # use a cached datetime if any, else current datetime

Relationship
~~~~~~~~~~~~

The Relationship Property points to one *or many* JSON-LD objects.

.. code-block::

   from ngsildclient import Entity

   entity = Entity("Vehicle", "A4567")
   entity.rel("isParked", "OffStreetParking:Downtown1", observedat="2017-07-29T12:00:04Z")

.. code-block:: json-ld
   :caption: Relationship illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Vehicle:A4567",
      "type": "Vehicle",
      "isParked": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:OffStreetParking:Downtown1",
         "observedAt": "2017-07-29T12:00:04Z"
      }
   }

Import the **Rel** Enum to access well-known relationship names, such as ``observedBy`` or ``hasPart``.

Implement nested properties
---------------------------

Sometimes properties are composed of properties.

Single level
~~~~~~~~~~~~

| You might want to add a nested property to provide information about the quality check status.
| Use the **NESTED** keyword or set the **nested** argument to True.
| The property will be nested into the latest added property.

.. code-block::

   from ngsildclient import Entity, NESTED

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.prop("NO2", 22, unitcode="GP").prop("qc", "checked", NESTED)

.. code-block:: json-ld
   :caption: Nested property illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z",
      "type": "AirQualityObserved",
      "NO2": {
         "type": "Property",
         "value": 22,
         "unitCode": "GP",
         "qc": {
            "type": "Property",
            "value": "checked"
         }
      }
   }

| Another nested example from the Guidelines for Modelling with NGSI-LD [ETSI_WP42]_.

.. code-block::

   from ngsildclient import Entity, NESTED, Rel

   room = Entity("Room", "01")
   room.prop("temperature", 17).rel(Rel.OBSERVED_BY, "Sensor:01", NESTED)

.. code-block:: json-ld
   :caption: Example from the ETSI White Paper

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Room:01",
      "type": "Room",
      "temperature": {
         "type": "Property",
         "value": 17,
         "observedBy": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:Sensor:01"
         }
      }
   }

Multilevel
~~~~~~~~~~

You can chain nested properties in order to obtain several nesting levels.

.. code-block::

   from ngsildclient import Entity, NESTED

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.prop("NO2", 22, unitcode="GP").prop("qc", "checked", NESTED).prop("status", "discarded", NESTED)

.. code-block:: json-ld
   :caption: Multilevel nested property illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z",
      "type": "AirQualityObserved",
      "NO2": {
         "type": "Property",
         "value": 22,
         "unitCode": "GP",
         "qc": {
            "type": "Property",
            "value": "checked",
            "status": {
               "type": "Property",
               "value": "discarded"
            }
         }
      }
   }

Anchoring
~~~~~~~~~

| By default a property is added to the entity's root.
| When NESTED is set the property is nested into the latest added property.

| Sometimes you need to nest properties into a given and fixed property.
| Here comes the **anchor()** method that allows to set a property into which subsequent properties will be nested.
| Until the **unanchor()** method is called to return to the default behaviour.

.. code-block::

   from datetime import datetime
   from ngsildclient import Entity

   parking = Entity("OffStreetParking", "Downtown1")
   parking.prop("availableSpotNumber", 121, observedat=datetime(2017, 7, 29, 12, 5, 2).anchor()
   parking.prop("reliability", 0.7).rel("providedBy", "Camera:C1").unanchor()
   parking.prop("description", "Municipal car park located near the Trindade metro station and the Town Hall")

.. code-block:: json-ld
   :caption: Multilevel nested property illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:OffStreetParking:Downtown1",
      "type": "OffStreetParking",
      "availableSpotNumber": {
         "type": "Property",
         "value": 121,
         "observedAt": "2017-07-29T12:05:02Z",
         "reliability": {
            "type": "Property",
            "value": 0.7
         },
         "providedBy": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:Camera:C1"
         }
      },
      "description": {
         "type": "Property",
         "value": "Municipal car park located near the Trindade metro station and the Town Hall"
      }
   }

Update an entity
----------------

| An Entity instance is backed by a dictionary.
| In fact a NGSI-dedicated dictionary that extends the native Python dictionary.
| You use this dictionary each time you deal with a subpart of the Entity.

It provides obviously all the native dictionary staff but also :

- the **prop()**, **gprop()**, **tprop()** and **rel()** primitives quite equivalent to those provided by the Entity
- a dot notation to access fields, i.e. `room["temperature.value"]`

Let's consider the following example.

.. code-block:: json-ld

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Room:01",
      "type": "Room",
      "temperature": {
         "type": "Property",
         "value": 22.5,
         "observedBy": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:Sensor:01"
         }
      },
      "pressure": {
         "type": "Property",
         "value": 938.8
      }
   }

Update a member
~~~~~~~~~~~~~~~

| Entity members are ``id``, ``type`` and ``context``.
| The Entity class provides a Python property for each one.
| Members can be updated but cannot be removed.

.. code-block::

   from ngsildclient import Entity

   room.id = "urn:ngsi-ld:Room:02"

Update a value
~~~~~~~~~~~~~~~

.. code-block::

   from ngsildclient import Entity

   room["temperature.value"] += 0.2

Add metadata or userdata
~~~~~~~~~~~~~~~~~~~~~~~~

Use the same method.

.. code-block::

   from ngsildclient import Entity

   room["temperature.unitCode"] = "CEL"

Remove any part of the Entity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It applies to properties as well.

.. code-block::

   from ngsildclient import Entity

   del room["temperature.unitCode"]

Update a property
~~~~~~~~~~~~~~~~~

To update an Entity's property the easiest way is to override it.

.. code-block::

   from ngsildclient import Entity

   room.prop("pressure", 938.7, unitcode="A97")

Add a nested property
~~~~~~~~~~~~~~~~~~~~~

| We can add a nested property without rebuilding the upper property.
| Here we nest a qc property into the temperature property.

.. code-block::

   from ngsildclient import Entity

   room["temperature"].prop("qc", "checked")

Add a multilevel nested property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Here we nest a status property into a qc property, itself nested into the temperature property.
| Note that chaining the **prop()** automatically enables nesting.
| The **prop()** method used here does not belong to the Entity but to the NGSI-dedicated dictionary.

.. code-block::

   from ngsildclient import Entity

   room["temperature"].prop("qc", "checked").prop("status", "discarded")


Display an entity
-----------------

| The **to_json()** method returns the JSON payload as a string.
| By setting the **kv** argument to True, it returns the simplified representation aka **KeyValues** format.

| The **pprint()** method relies on **to_json()** in order to pretty-print the entity.
| It also takes a **kv** argument.

Import/Export
-------------

Dictionary
~~~~~~~~~~

Suppose we have this dictionary.

.. code-block::

   payload = {
      "type": "Room",
      "id": "urn:ngsi-ld:Room:01",
      "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
      "temperature": {"type": "Property", "value": 22.5}
   }

| You can create an entity from this dictionary.
| Note that ``id``, ``type`` and ``@context`` are mandatory.
| If missing an exception will be raised.

.. code-block::

   from ngsildclient import Entity

   room = Entity.from_dict(payload)

The opposite operation converts your entity to a dictionary.

.. code-block::

   from ngsildclient import Entity

   payload = room.to_dict()

File
~~~~

Import and Export from/to a file is a very useful feature that allows :

- backup : just restore an entity you've previously saved
- testing : store an expected result for further comparison
- sharing : elaborate with others about modeling
- experimenting : load an example from the `Smart Data Models Initiative`_ and play around
- contributing : propose a NGSI-LD example to the Smart Data Models Initiative

We can load a local file.

.. code-block::

   from ngsildclient import Entity, SmartDataModels

   room = Entity.load("/tmp/room1.jsonld")

And save an entity to a file.

.. code-block::

   from ngsildclient import Entity, SmartDataModels

   room.save("/tmp/room2.jsonld")

We can load a remote file through HTTP.

.. code-block::

   from ngsildclient import Entity

   battery = Entity.load("https://github.com/smart-data-models/dataModel.Battery/raw/master/Battery/examples/example-normalized.jsonld")

For convenience some datamodel example URLs of the `Smart Data Models Initiative`_ are made available.

.. code-block::

   from ngsildclient import Entity, SmartDataModels

   beach = Entity.load(SmartDataModels.SmartCities.PointOfInterest.Beach)


Utils
-----

ISO8601
~~~~~~~

In NGSI-LD entities dates, times and datetimes are represented as ISO8601 strings.

The **iso8601** module provides you with functions to convert from Python types to ISO8601 :

- **from_date()**
- **from_time()**
- **from_datetime()**
- **utcnow()** to get the current datetime

Note that this is not needed for the **tprop()** primitive and **observedat** argument that accepts Python date types, *calling these functions for you*.

.. code-block::
   :caption: ISO8601 Example

   from datetime import datetime
   from ngsildclient import iso8601, TZ_CET

   dt = datetime(2022, 3, 10, 17, 49, tzinfo=TZ_CET)
   iso8601.from_datetime(dt) # '2022-03-10T16:49:00Z'

Short UUID
~~~~~~~~~~

A UUID may be useful in some cases to create a unique Entity identifier.

But a long dash-separated string is not always suitable.
The short UUID string will be 22 characters long, base64-encoded, with padding characters removed.
The encoding uses the urlsafe alphabet with a slightly difference.
The dash character (often used as a NGSI field separator) is replaced by the tilde character.

.. code-block::

   from ngsildclient import Entity, shortuuid

   dt = datetime(2022, 3, 10, 17, 49, tzinfo=TZ_CET)
   crop = Entity("AgriCrop", shortuuid())

.. code-block:: json-ld
   :caption: short UUID illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AgriCrop:ldoRJQMZSaaKoWn9g_JR~g",
      "type": "AgriCrop"
   }

Helpers
-------

Helper functions can help building complex data structures frequently used in NGSI-LD entities.

Using helper functions :

- enforces a well-constructed consistent structure
- guides you through the different options thanks to IDE autocompletion

The code may look quite long at first sight but is mainly generated by the IDE.

PostalAddress
~~~~~~~~~~~~~

PostalAddress_ as defined by `Schema.org`_.

.. code-block::

   from ngsildclient import Entity, PostalAddressBuilder

   entity = Entity("WeatherObserved", "Spain-Valladolid-2016-11-30T07:00:00.00Z")
   entity.prop("address",
      PostalAddressBuilder()
      .street("C/ La Pereda 14")
      .locality("Santander")
      .region("Cantabria")
      .country("Spain")
      .build())

.. code-block:: json-ld
   :caption: PostalAddress illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:WeatherObserved:Spain-Valladolid-2016-11-30T07:00:00.00Z",
      "type": "WeatherObserved",
      "address": {
         "type": "Property",
         "value": {
            "streetAddress": "C/ La Pereda 14",
            "addressLocality": "Santander",
            "addressRegion": "Cantabria",
            "addressCountry": "Spain"
         }
      }
   }

OpeningHours
~~~~~~~~~~~~

OpeningHoursSpecification_ as defined by `Schema.org`_.

.. code-block::

   from ngsildclient import Entity, OpeningHours

   openinghours = OpeningHoursBuilder()
      .businessdays("10:00", "17:30")
      .saturday("10:00", "14:00")
      .build()
   library = Entity("Library", "Ireland-Shannon-PublicLibrary")
   library.prop("openingHours", openinghours)

.. code-block:: json-ld
   :caption: OpeningHours illustrated

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Library:Ireland-Shannon-PublicLibrary",
      "type": "Library",
      "openingHours": {
         "type": "Property",
         "value": [
            {
               "opens": "10:00",
               "closes": "17:30",
               "dayOfWeek": "Monday"
            },
            {
               "opens": "10:00",
               "closes": "17:30",
               "dayOfWeek": "Tuesday"
            },
            {
               "opens": "10:00",
               "closes": "17:30",
               "dayOfWeek": "Wednesday"
            },
            {
               "opens": "10:00",
               "closes": "17:30",
               "dayOfWeek": "Thursday"
            },
            {
               "opens": "10:00",
               "closes": "17:30",
               "dayOfWeek": "Friday"
            },
            {
               "opens": "10:00",
               "closes": "14:00",
               "dayOfWeek": "Saturday"
            }
         ]
      }
      }

This is only a basic implementation but still useful. As of now it does not support break times.

Mocking
-------

For testing purpose you may need a lot of entities but don't have them.

Here comes **MockerNgsi**. In the following example it generates from a given entity 100 new mocked entities.

.. code-block::

   from ngsildclient import Entity, MockerNgsi

   entity = Entity("AirQualityObserved", "Madrid-28079004-2016-03-15T11:00:00Z")
   entity.prop("NO2", 22, unitcode="GP")

   # generate 100 mocked entities
   mocker = MockerNgsi()
   mocked_entities = mocker.mock(entity, 100)

Have a look at the first mocked entity in the list.

.. code-block:: json-ld
   :caption: Mocking illustrated
   :emphasize-lines: 5, 12-15

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z:Mocked:a_m7D8qkQBCIjlTnkY7J~g",
      "type": "AirQualityObserved",
      "NO2": {
         "type": "Property",
         "value": 22,
         "unitCode": "GP"
      },
      "mocked": {
         "type": "Property",
         "value": true
      }
   }

The ``id`` has been suffixed with a unique mock-identifier. A ``mocked`` property has been added.
This is the default behaviour of the **MockerNgsi** class.

It's up to you to implement your custom mocking logic by providing your own ``f_mock_id`` and ``f_mock_payload`` functions.

.. code-block::

   import random

   def randomize_NO2(entity: Entity):
      entity.prop("mocked", True)
      entity["NO2.value"] += random.uniform(-3.0, 3.0)

   # generate 100 mocked entities
   mocker = MockerNgsi(f_mock_payload=randomize_NO2)
   mocked_entities = mocker.mock(entity, 100)

.. code-block:: json-ld
   :caption: Custom mocking logic illustrated
   :emphasize-lines: 9

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AirQualityObserved:Madrid-28079004-2016-03-15T11:00:00Z:Mocked:uIzmaZfVT3ulIcR8UY8cXg",
      "type": "AirQualityObserved",
      "NO2": {
         "type": "Property",
         "value": 22.830140401969413,
         "unitCode": "GP"
      },
      "mocked": {
         "type": "Property",
         "value": true
      }
   }

For further information look at the **MockerNgsi** class documentation.


.. [1] Note that all NGSI-LD datetimes are UTC. The library will always convert datetimes to UTC, either naive or aware.
   The downside of not specifying the timezone is that the result depends on your local environment therefore code execution is not reproducible.
   Behaviour may change if your code is run in a different place/timezone.

.. [ETSI_WP42] Guidelines for Modelling with NGSI-LD `ETSI WhitePaper <https://www.etsi.org/images/files/ETSIWhitePapers/etsi_wp_42_NGSI_LD.pdf>`_
.. _Smart Data Models Initiative: https://smartdatamodels.org/
.. _Schema.org: https://schema.org
.. _PostalAddress: https://schema.org/PostalAddress
.. _OpeningHoursSpecification: https://schema.org/OpeningHoursSpecification
