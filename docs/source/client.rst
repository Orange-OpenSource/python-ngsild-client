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
   :emphasize-lines: 3
    
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
   :emphasize-lines: 3
    
   from ngsilclient import Client

   client = Client()

.. note::
   In interactive mode the Client displays additional information, probing the broker to guess the vendor and version.

Disconnect
~~~~~~~~~~

To free resources it's recommended to properly close the client at the end.

.. code-block::
   :caption: Disconnect from a local broker instance
   :emphasize-lines: 5
    
   from ngsilclient import Client

   client = Client()
   print(client.is_connected())  # some processing
   client.close()


The with statement
~~~~~~~~~~~~~~~~~~

One could use the **with** statement. It will automatically close the client.

.. code-block::
   :emphasize-lines: 3

   from ngsilclient import Client

   with Client() as client:
      print(client.is_connected())  # some processing

.. note::
   The **is_connected()** method sends a dummy but compliant request to the Context Broker then returns True
   if the broker answered.

Use the API
-----------

| The client wraps the following endpoints : **entities**, **entityOperations**, **types**, **jsonldContexts**, **subscriptions**.
| Operations for each endpoint are available using the proper submodule.
| i.e. **client.types** provides the **list()** method that corresponds to the operation "Retrieve Available Entity Types".

.. note::
   For convenience common operations such as operations on entities are provided by the Client class.

.. code-block::
   :caption: Retrieve available entity types
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      print(client.list_types())

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


Handle Entities
~~~~~~~~~~~~~~~

Entities operations handle **Entity** objects as defined in ``ngsildclient.model.entity``.

Create a single entity
^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 5

   from ngsilclient import Client, Entity

   entity = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   with Client() as client:
      client.create(entity)

| If the entity already exists a **NgsiAlreadyExistsError** exception is raised.
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

Create a batch of entities
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 7

   from ngsilclient import Client, Entity

   e1 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   e2 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T10:00:00Z").prop("NO2", 9)
   entities = [e1, e2]
   with Client() as client:
      client.create(entities)

.. note::
   | **batch.create()** returns a tuple.
   | The 1st element is a boolean. True means creation has been successfull for all the entities.
   | If True the 2nd element is a list of identifiers.
   | If False the 2nd element is a dictionary with 2 entries, the ``success`` identifiers and the ``errors`` ones.

.. note::
   | The **MockerNgsi** class is very useful to mock and experiment with numerous entities.
   | One can duplicate an entity by using the **copy()** method or the **Entity.duplicate()** class method.

Retrieve a single entity
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      entity = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
      entity.pprint()

.. note::
   The **get()** method accept both a NGSI-LD identifier and an entity object.

If the entity doesn't exist, a **NgsiResourceNotFoundError** exception is raised.

.. note::
   The corresponding batch methods to retrieve a list of entities are known as **query** methods and prefixed with ``query_``.

Check whether an entity exists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      if client.exists("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z"):
         print("found measure at 9AM")

.. note::
   | The **exists()** method accept both a NGSI-LD identifier and an entity object.
   | There's no equivalent in batch mode.

Upsert a single entity
^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 5

   from ngsilclient import Client, Entity

   with Client() as client:
      entity = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
      client.upsert(entity)

.. note::
   The **upsert()** method is not atomic as *- for an existing entity -* it combines a delete operation followed by a create operation.

Upsert a batch of entities
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 7

   from ngsilclient import Client, Entity

   e1 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T09:00:00Z").prop("NO2", 8)
   e2 = Entity("AirQualityObserved", "Bordeaux-AirProbe42-2022-03-24T10:00:00Z").prop("NO2", 9)
   entities = [e1, e2]
   with Client() as client:
      client.upsert(entities)

.. note::
   | **batch.upsert()** returns a tuple.
   | The 1st element is a boolean. True means upsert has been successfull for all the entities.
   | The 2nd element is a dictionary with ``success`` and ``errors`` entries.

Update a single entity
^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 6

   from ngsilclient import Client, Entity

   with Client() as client:
      entity = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
      entity["NO2.value"] += 1
      client.update(entity)

Update a batch of entities
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 9

   from ngsilclient import Client, Entity

   e1 = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
   e2 = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T10:00:00Z")
   entities = [e1, e2]
   for e in entities:
      e["NO2.value"] += 1
   with Client() as client:
      client.update(entities)

.. note::
   | **batch.update()** returns a tuple.
   | The 1st element is a boolean. True means update has been successfull for all the entities.
   | The 2nd element is a dictionary with ``success`` and ``errors`` entries.

Query Head
^^^^^^^^^^

| The **query_head()** method is useful to **preview** a query execution.
| By default it retrieves the first 5 matching entities.

.. code-block::
   :caption: Retrieve the 5 first AirQualityObserved entities
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      entities = client.query_head(type="AirQualityObserved")

.. note::
   | The **query_head()** method takes an entity type, a query string, or both.
   | It takes a **num** optional argument to retrieve the first **num** entities. *Default is 5*.
   | It retrieves up to **PAGINATION_LIMIT_MAX** results that is currently a constant set to 100.
   

Query All
^^^^^^^^^

The **query_all()** method returns a list of matching entities.

.. code-block::
   :caption: Print top ten NO2 worst levels
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      entities = client.query_all(type="AirQualityObserved", q="NO2>40")
      top10 = sorted(entities, reverse=True, key=lambda x: x["NO2.value"])[:10]
      print(top10)

.. note::
   | The **query_all()** method retrieves at once **ALL** the matching entities *by enabling pagination and sending behind the curtain as many requests as needed*.
   | **NgsiClientTooManyResultsError** is raised if more than 1 million entities (configurable thanks to the **max** argument).

.. warning:: 
   | Assume the whole dataset fits in memory.
   | It should not be an issue except for very large datasets.

Query Generator
^^^^^^^^^^^^^^^

| The **query_generator()** method returns a generator of entities.
| It relies on the Python generator mechanism and allows to retrieve entities on the fly *(without storing them)*.

.. code-block::
   :caption: Print all AirQualityObserved entities
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      for e in client.query_generator(type="AirQualityObserved"):
         e.pprint()

.. code-block::
   :caption: Print all NO2 values over 80 *(filtering on the client side)*
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      g = client.query_generator(type="AirQualityObserved")
      g = (e for e in g if e["NO2.value"] > 80)  # generator comprehension
      for e in g:
         e.pprint()

.. note::
   | The **query_generator()** method takes an entity type, a query string, or both.
   | By default it **yields** entities one by one.
   | When the **batch** boolean argument is set it **yields** batch of entities.
   | Batch size is currently defined by the constant **PAGINATION_LIMIT_MAX**.

Low-Level Query
^^^^^^^^^^^^^^^

| Above query methods are advanced methods that handle pagination for you.
| If you want to handle pagination by yourself, you can use **client.entities.query()** that basically wraps the API endpoint and allows to specify the **offset** and **limit** arguments.

Count
^^^^^

The **count()** method returns the number of matching entities.

.. code-block::
   :caption: Print number of values over threshold
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      exceed_threshold: int = client.count(type="AirQualityObserved", q="NO2>80")
      print(f"Values over threshold : {exceed_threshold}")

.. note::
   | **count()** has the same signature as the **query()** method.
   | Except it returns an integer.

Delete a single entity
^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      client.delete("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")

.. note::
   | The **delete()** method accept both a NGSI-LD identifier and an entity object.
   | **delete()** returns True if the entity has been successfully deleted.

Delete a batch of entities
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 6

   from ngsilclient import Client, Entity

   with Client() as client:
      e1 = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T09:00:00Z")
      e2 = client.get("urn:ngsi-ld:AirQualityObserved:Bordeaux-AirProbe42-2022-03-24T10:00:00Z")
      entities = [e1, e2]  
      client.delete(entities)

.. note::
   | **batch.delete()** returns a tuple.
   | The 1st element is a boolean. True means update has been successfull for all the entities.
   | The 2nd element is a dictionary with ``success`` and ``errors`` entries. 

Conditional Delete
^^^^^^^^^^^^^^^^^^

.. code-block::
   :caption: Remove outliers
   :emphasize-lines: 4

   from ngsilclient import Client, Entity

   with Client() as client:
      client.delete_where(type="AirQualityObserved", q="NO2<0|NO2>1000")

Drop all entities of the same type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      client.drop("AirQualityObserved")

Purge all entities
^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      client.purge()

.. caution::
   **purge()** removes **ALL** entities.

Flush all
^^^^^^^^^

Remove all entities and all contexts *except the Core context*.

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      client.flush_all()

.. caution::
   No confirmation is asked.

List types
^^^^^^^^^^

List available entity types.

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      client.list_types()


Handle Contexts
~~~~~~~~~~~~~~~

List contexts
^^^^^^^^^^^^^

.. code-block::
   :caption: Display stored contexts
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      contexts = client.contexts.list()
      print(contexts)

It returns a list of strings. Each string heads to a context URI.

.. note::
   There should be at least one entry : the default Core context.

Retrieve a context
^^^^^^^^^^^^^^^^^^

.. code-block::
   :caption: Display the content of the default core context
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      ctx_core = client.contexts.get("https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld")
      print(ctx_core)

Delete a context
^^^^^^^^^^^^^^^^^^

.. code-block::
   :caption: Remove the Device context
   :emphasize-lines: 5

   from ngsilclient import Client

   ctx_device = "https://github.com/smart-data-models/dataModel.Device/raw/aba14f18bb6e5f7ee1bd2f3b866d23c7ad630ad8/context.jsonld"
   with Client() as client:
      client.contexts.delete(ctx_device)

Delete any context matching a substring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :caption: Remove the Device context and other contexts containing the word ``device``
   :emphasize-lines: 4

   from ngsilclient import Client

   with Client() as client:
      client.contexts.delete("device")

.. note::
   Matching is case insensitive.

Cleanup contexts
^^^^^^^^^^^^^^^^

Remove all contexts except the default core context.

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client, CORE_CONTEXT

   with Client() as client:
      client.contexts.cleanup()

Add a context
^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 5

   from ngsilclient import Client

   ctx_nimp = {"@context": {"nimp": "https://nimp.org/nimp"}}
   with Client() as client:
      client.contexts.add(ctx_nimp)

.. note::
   Raise a **ValueError** exception if input dictionary does not contain a ``@context`` key.

Check whether a context exists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::
   :emphasize-lines: 4

   from ngsilclient import Client, CORE_CONTEXT

   with Client() as client:
      if not client.contexts.exists(CORE_CONTEXT):
         print("Missing default context !!")

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