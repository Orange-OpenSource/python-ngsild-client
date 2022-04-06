Interact with the Broker
========================

This chapter explains how to use the NGSI-LD Client.

Connect to the broker
---------------------

Connect
~~~~~~~

| First we need a broker up and running.
| Then tell the client to point to the broker by providing its ip address and TCP port.

.. code-block::
    
   from ngsilclient import Client

   client = Client("my.broker.org", 8000)

| The Client constructor takes many optional arguments.
| **hostname** defaults to ``localhost``.
| **port** defaults to ``1026``.
| **tenant** is not set by default.
| Use HTTPS by setting the **secure** boolean argument to True.
| If the **overwrite** argument is set, the client will always upsert entities and will not complain about already existing entities.
| Authentication is not supported yet.
| For a complete list of arguments please refer to the doctrings.

| In case you don't have a broker you'll find some ready-to-use dockerized brokers in the **brokers** folder.
| Select one, cd into the directory and type in ``docker compose up -d``.

.. code-block::
   :caption: Connect to a local broker instance
    
   from ngsilclient import Client

   client = Client()

.. note::
   In interactive mode the Client displays additional information, probing the broker to guess the vendor and version.

Disconnect
~~~~~~~~~~

To free resources it's recommended to properly close the client at the end.

.. code-block::
   :caption: Disconnect from a local broker instance
    
   from ngsilclient import Client

   client = Client()
   print(client.is_connected())  # some processing
   client.close()


The with statement
~~~~~~~~~~~~~~~~~~

One could use the **with** statement. It will automatically close the client.

.. code-block::

   from ngsilclient import Client

   with Client() as client:
      print(client.is_connected())  # some processing

.. note::
   The **is_connected()** method sends a dummy but compliant request to the Context Broker then returns True
   if the broker answered.

Wrap API operations
-------------------

| The client wraps the following endpoints : **entities**, **entityOperations**, **types**, **jsonldContexts**, **subscriptions**.
| Operations for each endpoint are available using the proper submodule.
| i.e. **client.types** provides the **list()** method that corresponds to the operation "Retrieve Available Entity Types".
| Common operations such as operations on entities are directly available at the client level.

.. code-block::
   :caption: Retrieve available entity types

   from ngsilclient import Client

   with Client() as client:
      print(client.types.list())

.. table:: Submodule Mapping Table

   +---------------+------------------+
   | submodule     | NGSI-LD Resource |
   +===============+==================+
   | entities      | entities         |
   +---------------+------------------+
   | batch         | entityOperations |
   +---------------+------------------+
   | types         | types            |
   +---------------+------------------+
   | contexts      | jsonldContexts   |
   +---------------+------------------+
   | subscriptions | subscriptions    |
   +---------------+------------------+


Entities
~~~~~~~~

Entities operations handle **Entity** objects as defined in ``ngsildclient.model.entity``.

Create
^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   entity = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   with Client() as client:
      client.create(entity)

| If the entity already exists, a **NgsiAlreadyExistsError** exception is raised.
| You should either catch this exception or use an overwrite strategy.

You can enable the **overwrite** argument

.. code-block::

   client.create(entity, overwrite=True)

It's equivalent of the **upsert()** method.

If you prefer to skip creation you can enable the **skip** argument.

.. code-block::

   client.create(entity, skip=True)

You can enable an overwrite strategy at the client level globally for all operations.

.. code-block::
   :caption: at init time
   
   client = Client(overwrite=True)

Retrieve
^^^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   with Client() as client:
      entity = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
      entity.pprint()

.. note::
   The **get()** method accept both a NGSI-LD identifier and an entity object.

If the entity doesn't exist, a **NgsiResourceNotFoundError** exception is raised.

Delete
^^^^^^

.. code-block::

   from ngsilclient import Client

   with Client() as client:
      client.delete("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")

.. note::
   | The **delete()** method accept both a NGSI-LD identifier and an entity object.
   | **delete()** returns True if the entity has been successfully deleted.

Exists
^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   with Client() as client:
      if client.exists("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z"):
         print("found measure at 9AM")

.. note::
   | The **exists()** method accept both a NGSI-LD identifier and an entity object.
   | **delete()** returns True if the entity exists.

Upsert
^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   with Client() as client:
      entity = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
      entity["NO2.value"] += 1
      client.upsert(entity)

.. note::
   The **upsert()** method is not atomic as it combines a delete operation followed by a create operation.

Query Head
^^^^^^^^^^

   | The **query_head()** method retrieves the first 5 matching entities.
   | 

.. code-block::
   :caption: Retrieve the 5 first AirQualityObserved entities

   from ngsilclient import Client, Entity

   with Client() as client:
      entities = client.query_head(type="AirQualityObserved")

.. note::
   | The **query_head()** method takes an entity type, a query string, or both.
   | It takes a **num** optional argument to retrieve the first **num** entities (default is 5).
   | It retrieves up to **PAGINATION_LIMIT_MAX** results which depends on the broker implementation.
   

Query All
^^^^^^^^^

   The **query_all()** method returns a list of matching entities.

.. code-block::
   :caption: Print top ten NO2 worst levels

   from ngsilclient import Client, Entity

   with Client() as client:
      entities = client.query(type="AirQualityObserved", q="NO2>40")
      top10 = sorted(entities, reverse=True, key=lambda x: x["NO2.value"])[:10]
      print(top10)

.. note::
   | The **query_all()** method retrieves at once **ALL** the matching entities *by enabling pagination and sending behind the curtain as many requests as needed*.
   | Assume data hold in memory. Should not be an issue except for very large datasets.
   | **NgsiClientTooManyResultsError** is raised if more than 1 million entities (configurable thanks to the **max** argument).
   | Depending on your RAM you could confidently retrieve millions or even tens of millions entities.

Query Generator
^^^^^^^^^^^^^^^

   | The **query_generator()** method returns a generator of entities.
   | It relies on the Python generator mechanism and allows to retrieve entities on the fly *(without storing them)*.

.. code-block::
   :caption: Print all AirQualityObserved entities

   from ngsilclient import Client, Entity

   with Client() as client:
      for e in client.query_generator(type="AirQualityObserved"):
         e.pprint()

.. code-block::
   :caption: Print all NO2 values over 80 *(filtering on the client side)*

   from ngsilclient import Client, Entity

   with Client() as client:
      g = client.query_generator(type="AirQualityObserved")
      g = (e for e in g if e["NO2.value"] > 80)  # generator comprehension
      for e in g:
         e.pprint()

Low-Level Query
^^^^^^^^^^^^^^^

| Above query methods are advanced methods that handle pagination for you.
| If you want to handle pagination by yourself, you can use **client.entities.query()** that basically wraps the API endpoint and allows to specify the **offset** and **limit** arguments.

Count
^^^^^

   The **count()** method returns the number of matching entities.

.. code-block::
   :caption: Print number of values over threshold

   from ngsilclient import Client, Entity

   with Client() as client:
      exceed_threshold: int = client.county(type="AirQualityObserved", q="NO2>80")
      print(f"Values over threshold : {exceed_threshold}")

.. note::
   | **count()** has the same signature as the **query()** method.
   | Except it returns an integer.

Batch
~~~~~

Batch operations handle **Entity** list of objects as defined in ``ngsildclient.model.entity``.

Batch Create
^^^^^^^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   e1 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   e2 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T10:00:00Z").prop("NO2", 9)
   entities = [e1, e2]
   with Client() as client:
      client.batch.create(entities)

.. note::
   | **batch.create()** returns a tuple.
   | The 1st element is a boolean. True means creation has been successfull for all the entities.
   | If True the 2nd element is a list of identifiers.
   | If False the 2nd element is a dictionary with 2 entries, the ``success`` identifiers and the ``errors`` ones.

.. note::
   | The **MockerNgsi** class is very useful to mock and experiment with numerous entities.
   | One can duplicate an entity by using the **copy()** method or the **Entity.duplicate()** class method.

Batch Upsert
^^^^^^^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   e1 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   e2 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T10:00:00Z").prop("NO2", 9)
   entities = [e1, e2]
   with Client() as client:
      client.batch.upsert(entities)

.. note::
   | **batch.upsert()** returns a tuple.
   | The 1st element is a boolean. True means upsert has been successfull for all the entities.
   | The 2nd element is a dictionary with ``success`` and ``errors`` entries.
 
Batch Update
^^^^^^^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   e1 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   e2 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T10:00:00Z").prop("NO2", 9)
   entities = [e1, e2]
   with Client() as client:
      client.batch.update(entities)

.. note::
   | **batch.update()** returns a tuple.
   | The 1st element is a boolean. True means update has been successfull for all the entities.
   | The 2nd element is a dictionary with ``success`` and ``errors`` entries.

Batch Delete
^^^^^^^^^^^^

.. code-block::

   from ngsilclient import Client, Entity

   with Client() as client:
      entities = client.query(type="AirQualityObserved")
      client.batch.delete(entities)

.. note::
   | **batch.delete()** returns a tuple.
   | The 1st element is a boolean. True means update has been successfull for all the entities.
   | The 2nd element is a dictionary with ``success`` and ``errors`` entries.

Exception handling
------------------

| The client at creation time and in subsequent methods calls may raise exceptions.
| It is a good idea to catch them to get proper information about errors that occured.

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~

.. raw:: html
   :file: exceptions_hierarchy_ascii_scheme.html
   :encoding: ascii

| All exceptions raised by the library inherit from the **NgsiError** exception.
| **NgsiContextBrokerError** are augmented exceptions that provide accurate information thanks to ProblemDetails implemented by the NGSI-LD API operations [2]_.
| Not all exceptions are represented here. Please refer to docstrings for the full list.

Mapping to NGSI-LD API errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------------+-----------------------------------------------------------+
| Exception                      | Error Type                                                |
+================================+===========================================================+
| NgsiInvalidRequestError        | https://uri.etsi.org/ngsi-ld/errors/InvalidRequest        |
+--------------------------------+-----------------------------------------------------------+
| NgsiBadRequestDataError        | https://uri.etsi.org/ngsi-ld/errors/BadRequestData        |
+--------------------------------+-----------------------------------------------------------+
| NgsiAlreadyExistsError         | https://uri.etsi.org/ngsi-ld/errors/AlreadyExists         |
+--------------------------------+-----------------------------------------------------------+
| NgsiOperationNotSupportedError | https://uri.etsi.org/ngsi-ld/errors/OperationNotSupported |
+--------------------------------+-----------------------------------------------------------+
| NgsiResourceNotFoundError      | https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound      |
+--------------------------------+-----------------------------------------------------------+
| NgsiInternalError              | https://uri.etsi.org/ngsi-ld/errors/InternalError         |
+--------------------------------+-----------------------------------------------------------+
| NgsiTooComplexQueryError       | https://uri.etsi.org/ngsi-ld/errors/TooComplexQuery       |
+--------------------------------+-----------------------------------------------------------+
| NgsiTooManyResultsError        | https://uri.etsi.org/ngsi-ld/errors/TooManyResults        |
+--------------------------------+-----------------------------------------------------------+
| NgsiLdContextNotAvailableError | https://uri.etsi.org/ngsi-ld/errors/LdContextNotAvailable |
+--------------------------------+-----------------------------------------------------------+
| NgsiNoMultiTenantSupportError  | https://uri.etsi.org/ngsi-ld/errors/NoMultiTenantSupport  |
+--------------------------------+-----------------------------------------------------------+
| NgsiNonexistentTenantError     | https://uri.etsi.org/ngsi-ld/errors/NonexistentTenant     |
+--------------------------------+-----------------------------------------------------------+

Nominal vs Unattended exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Nominal exceptions are part of the NGSI-LD expected functional worflow.
| For example an exception is raised when trying to create an entity that already exists.
| In this case one would notify the user, silenlty ignore the error or implement custom logic.
| Unattended exceptions means errors have occured and should be caught.

.. code-block::
   :caption: Create a new entity

   from ngsildclient import Entity, Client, NgsiAlreadyExistsError, NgsiContextBrokerError, NgsiError

   try:
      entity = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
      client.create(entity)
   except NgsiAlreadyExistsError:
      pass  # silently ignore
   except NgsiContextBrokerError as e:
         print(e.problemdetails)
   except NgsiError as e:
         print(e)

.. note::
   The library provides advanced methods to tackle intricacies of entity creation, such as an ``upsert()`` method.


.. [2] IETF RFC 7807: Problem Details for HTTP APIs