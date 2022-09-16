Cookbook
========

How to forge entities
---------------------

Some official entities from the Smart Data Models Initiative built with the library.

PointOfInterest
~~~~~~~~~~~~~~~

PointOfInterest_ on SmartDataModels repository.

.. code-block:: json-ld
   :caption: PointOfInterest NGSI-LD normalized example

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:PointOfInterest:PointOfInterest-A-Concha-123456",
      "type": "PointOfInterest",
      "name": {
         "type": "Property",
         "value": "Playa de a Concha"
      },
      "address": {
         "type": "Property",
         "value": {
            "addressLocality": "Vilagarcía de Arousa",
            "addressCountry": "ES"
         }
      },
      "category": {
         "type": "Property",
         "value": [
            113
         ]
      },
      "description": {
         "type": "Property",
         "value": "La Playa de A Concha se presenta como una continuacion de la Playa de Compostela, una de las mas frecuentadas de Vilagarcia."
      },
      "location": {
         "type": "GeoProperty",
         "value": {
            "type": "Point",
            "coordinates": [
            -8.76846,
            42.602145
            ]
         }
      },
      "source": {
         "type": "Property",
         "value": "http://www.tourspain.es"
      },
      "refSeeAlso": {
         "type": "Property",
         "value": [
            "urn:ngsi-ld:SeeAlso:Beach-A-Concha-123456"
         ]
      }
   }

.. code-block::
   :caption: PointOfInterest code snippet

   from ngsildclient import Entity, PostalAddressBuilder

   poi = Entity("PointOfInterest", "PointOfInterest-A-Concha-123456")
   poi.prop("name", "Playa de a Concha")
   poi.addr(PostalAddressBuilder().country("ES").locality("Vilagarcía de Arousa").build())
   poi.prop("category", [113])
   poi.prop("description", "La Playa de A Concha se presenta como una continuacion de la Playa de Compostela, una de las mas frecuentadas de Vilagarcia."
   poi.loc((42.60214472222222, -8.768460000000001))
   poi.prop("source", "http://www.tourspain.es")
   poi.prop("refSeeAlso", ["urn:ngsi-ld:SeeAlso:Beach-A-Concha-123456"])

How to develop NGSI-LD agents
-----------------------------

This chapter shows how to develop NGSI-LD Agents that implement the whole pipeline :

- Acquire some data
- Convert incoming data into NGSI-LD entities : here goes your business logic
- Send outgoing entities to the NGSI-LD broker

Various heterogeneous datasources have been selected to showcase the **ngsildclient** library at work.

Prefer synchronous agent if you need interactivity (i.e. inside Jupyter Notebooks), aim at simplicity and performance is not an issue.

Prefer asynchronous agent when interactivity is not required and seeking for performance, i.e. a real-time agent that collects data and sends entities to the broker at a high frequency rate.

Combine batch upserts and Asynchronous IO to achieve best performances.

Read in-memory tuples
~~~~~~~~~~~~~~~~~~~~~

In the examples below tuples are composed of 3 values :

- the room name *(string)*
- the temperature *(float, degrees Celsius)*
- the pressure *(integer, mmHg)*

.. code-block::
   :caption: Base mode

   from typing import Tuple
   from ngsildclient import Entity, Client

   def build_entity(room: Tuple) -> Entity:
      name, temp, pressure = room
      e = Entity("RoomObserved", name)
      e.prop("temperature", temp)
      e.prop("pressure", pressure)
      return e

   def main():
      client = Client()
      rooms = [("Room1", 23.1, 720), ("Room2", 21.8, 711)]
      for room in rooms:
         entity = build_entity(room)
         client.upsert(entity)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Batch variant
   
   from typing import Tuple
   from ngsildclient import Entity, Client

   def build_entity(room: Tuple) -> Entity:
      name, temp, pressure = room
      e = Entity("RoomObserved", name)
      e.prop("temperature", temp)
      e.prop("pressure", pressure)
      return e

   def main():
      client = Client()
      rooms = [("Room1", 23.1, 720), ("Room2", 21.8, 711)]
      entities = [build_entity(room) for room in rooms]
      client.upsert(entities)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   from typing import Tuple
   from ngsildclient import Entity, AsyncClient

   def build_entity(room: Tuple) -> Entity:
      name, temp, pressure = room
      e = Entity("RoomObserved", name)
      e.prop("temperature", temp)
      e.prop("pressure", pressure)
      return e

   async def main():
      client = AsyncClient()
      rooms = [("Room1", 23.1, 720), ("Room2", 21.8, 711)]
      for room in rooms:
         entity = build_entity(room)
         await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   from typing import Tuple
   from ngsildclient import Entity, AsyncClient

   def build_entity(room: Tuple) -> Entity:
      name, temp, pressure = room
      e = Entity("RoomObserved", name)
      e.prop("temperature", temp)
      e.prop("pressure", pressure)
      return e

   async def main():
      client = AsyncClient()
      rooms = [("Room1", 23.1, 720), ("Room2", 21.8, 711)]
      entities = [build_entity(room) for room in rooms]
      await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())

Read in-memory dataclasses instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the examples below a Room object is composed of 3 attributes :

- the room name *(string)*
- the temperature *(float, degrees Celsius)*
- the pressure *(integer, mmHg)*

.. code-block::
   :caption: Base mode

   from dataclasses import dataclass
   from ngsildclient import Entity, Client

   @dataclass
   class Room:
      name: str
      temperature: float
      pressure: int

   def build_entity(room: Room) -> Entity:
      e = Entity("RoomObserved", room.name)
      e.prop("temperature", room.temperature)
      e.prop("pressure", room.pressure)
      return e

   def main():
      client = Client()
      rooms = [Room("Room1", 23.1, 720), Room("Room2", 21.8, 711)]
      for room in rooms:
         entity = build_entity(room)
         client.upsert(entity)

   if __name__ == "__main__":
      main()


.. code-block::
   :caption: Batch variant
   
   from dataclasses import dataclass
   from ngsildclient import Entity, Client

   @dataclass
   class Room:
      name: str
      temperature: float
      pressure: int

   def build_entity(room: Room) -> Entity:
      e = Entity("RoomObserved", room.name)
      e.prop("temperature", room.temperature)
      e.prop("pressure", room.pressure)
      return e

   def main():
      client = Client()
      rooms = [Room("Room1", 23.1, 720), Room("Room2", 21.8, 711)]
      entities = [build_entity(room) for room in rooms]
      client.upsert(entities)

   if __name__ == "__main__":
      main()


.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   from dataclasses import dataclass
   from ngsildclient import Entity, AsyncClient

   @dataclass
   class Room:
      name: str
      temperature: float
      pressure: int

   def build_entity(room: Room) -> Entity:
      e = Entity("RoomObserved", room.name)
      e.prop("temperature", room.temperature)
      e.prop("pressure", room.pressure)
      return e

   async def main():
      client = AsyncClient()
      rooms = [Room("Room1", 23.1, 720), Room("Room2", 21.8, 711)]
      for room in rooms:
         entity = build_entity(room)
         await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   from dataclasses import dataclass
   from ngsildclient import Entity, AsyncClient

   @dataclass
   class Room:
      name: str
      temperature: float
      pressure: int

   def build_entity(room: Room) -> Entity:
      e = Entity("RoomObserved", room.name)
      e.prop("temperature", room.temperature)
      e.prop("pressure", room.pressure)
      return e

   async def main():
      client = AsyncClient()
      rooms = [Room("Room1", 23.1, 720), Room("Room2", 21.8, 711)]
      entities = [build_entity(room) for room in rooms]
      await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())

Read in-memory dictionaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the examples below dictionaries are composed of 3 entries :

- the room name *(string)*
- the temperature *(float, degrees Celsius)*
- the pressure *(integer, mmHg)*

.. code-block::
   :caption: Base mode

   from ngsildclient import Entity, Client

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", room["name"])
      e.prop("temperature", room["temp"])
      e.prop("pressure", room["pressure"])
      return e

   def main():
      client = Client()
      rooms = [{"name": "Room1", "temp": 23.1, "pressure": 720}, {"name": "Room2", "temp": 21.8, "pressure": 711}]
      for room in rooms:
         entity = build_entity(room)
         client.upsert(entity)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Batch variant
   
   from ngsildclient import Entity, Client

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", room["name"])
      e.prop("temperature", room["temp"])
      e.prop("pressure", room["pressure"])
      return e

   def main():
      client = Client()
      rooms = [{"name": "Room1", "temp": 23.1, "pressure": 720}, {"name": "Room2", "temp": 21.8, "pressure": 711}]
      entities = [build_entity(room) for room in rooms]
      client.upsert(entities)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   from ngsildclient import Entity, AsyncClient

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", room["name"])
      e.prop("temperature", room["temp"])
      e.prop("pressure", room["pressure"])
      return e

   async def main():
      client = AsyncClient()
      rooms = [{"name": "Room1", "temp": 23.1, "pressure": 720}, {"name": "Room2", "temp": 21.8, "pressure": 711}]
      for room in rooms:
         entity = build_entity(room)
         await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   from ngsildclient import Entity, AsyncClient

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", room["name"])
      e.prop("temperature", room["temp"])
      e.prop("pressure", room["pressure"])
      return e

   async def main():
      client = AsyncClient()
      rooms = [{"name": "Room1", "temp": 23.1, "pressure": 720}, {"name": "Room2", "temp": 21.8, "pressure": 711}]
      entities = [build_entity(room) for room in rooms]
      await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())      

Read in-memory pandas dataframes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| pandas_ is required to run below examples.
| The `DataFrame sample`_ is taken from the pandas documentation.

.. code-block::
   :caption: Base mode

   import pandas as pd
   from ngsildclient import Entity, Client, iso8601

   def build_entity(specimen: tuple) -> Entity:
      e = Entity("SpecimenObserved", f"{specimen[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("specimenName", specimen[0])
      e.prop("legs", specimen[1])
      e.prop("wings", specimen[2])
      e.prop("amountObserved", specimen[3])
      return e

   def main():
      client = Client()
      df = pd.DataFrame(
         {"num_legs": [2, 4, 8, 0], "num_wings": [2, 0, 0, 0], "num_specimen_seen": [10, 2, 1, 8]},
         index=["falcon", "dog", "spider", "fish"],
      )
      for specimen in df.itertuples():
         entity = build_entity(specimen)
         client.upsert(entity)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Batch variant
   
   import pandas as pd
   from ngsildclient import Entity, Client, iso8601

   def build_entity(specimen: tuple) -> Entity:
      e = Entity("SpecimenObserved", f"{specimen[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("specimenName", specimen[0])
      e.prop("legs", specimen[1])
      e.prop("wings", specimen[2])
      e.prop("amountObserved", specimen[3])
      return e

   def main():
      client = Client()
      df = pd.DataFrame(
         {"num_legs": [2, 4, 8, 0], "num_wings": [2, 0, 0, 0], "num_specimen_seen": [10, 2, 1, 8]},
         index=["falcon", "dog", "spider", "fish"],
      )
      entities = [build_entity(specimen) for specimen in df.itertuples()]
      client.upsert(entities)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   import pandas as pd
   from ngsildclient import Entity, AsyncClient, iso8601

   def build_entity(specimen: tuple) -> Entity:
      e = Entity("SpecimenObserved", f"{specimen[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("specimenName", specimen[0])
      e.prop("legs", specimen[1])
      e.prop("wings", specimen[2])
      e.prop("amountObserved", specimen[3])
      return e

   async def main():
      client = AsyncClient()
      df = pd.DataFrame(
         {"num_legs": [2, 4, 8, 0], "num_wings": [2, 0, 0, 0], "num_specimen_seen": [10, 2, 1, 8]},
         index=["falcon", "dog", "spider", "fish"],
      )
      for specimen in df.itertuples():
         entity = build_entity(specimen)
         await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   import pandas as pd
   from ngsildclient import Entity, AsyncClient, iso8601

   def build_entity(specimen: tuple) -> Entity:
      e = Entity("SpecimenObserved", f"{specimen[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("specimenName", specimen[0])
      e.prop("legs", specimen[1])
      e.prop("wings", specimen[2])
      e.prop("amountObserved", specimen[3])
      return e

   async def main():
      client = AsyncClient()
      df = pd.DataFrame(
         {"num_legs": [2, 4, 8, 0], "num_wings": [2, 0, 0, 0], "num_specimen_seen": [10, 2, 1, 8]},
         index=["falcon", "dog", "spider", "fish"],
      )
      entities = [build_entity(specimen) for specimen in df.itertuples()]
      await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())

Read CSV files
~~~~~~~~~~~~~~

Here is the `sample CSV file <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/rooms.csv>`_ used in the following examples.

Each line is composed of 3 values, delimited by the semicolon character :

- the room name *(string)*
- the temperature *(float, degrees Celsius)*
- the pressure *(integer, mmHg)*


.. code-block::
   :caption: Base mode

   from ngsildclient import Entity, Client, iso8601

   def build_entity(csvline: str) -> Entity:
      room = csvline.rstrip().split(";")
      e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", float(room[1]))
      e.prop("pressure", int(room[2]))
      return e

   def main():
      client = Client()
      with open("rooms.csv") as f:
         for csvline in f:
               entity = build_entity(csvline)
               client.upsert(entity)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Batch variant
   
   from ngsildclient import Entity, Client, iso8601

   def build_entity(csvline: str) -> Entity:
      room = csvline.rstrip().split(";")
      e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", float(room[1]))
      e.prop("pressure", int(room[2]))
      return e

   def main():
      client = Client()
      with open("rooms.csv") as f:
         csvlines = f.readlines()
         entities = [build_entity(csvline) for csvline in csvlines]
         client.upsert(entities)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   import aiofiles
   from ngsildclient import Entity, AsyncClient, iso8601

   def build_entity(csvline: str) -> Entity:
      room = csvline.rstrip().split(";")
      e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", float(room[1]))
      e.prop("pressure", int(room[2]))
      return e

   async def main():
      client = AsyncClient()
      async with aiofiles.open("rooms.csv", "r") as f:
         async for csvline in f:
               entity = build_entity(csvline)
               await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   import aiofiles
   from ngsildclient import Entity, AsyncClient, iso8601

   def build_entity(csvline: str) -> Entity:
      room = csvline.rstrip().split(";")
      e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", float(room[1]))
      e.prop("pressure", int(room[2]))
      return e

   async def main():
      client = AsyncClient()
      async with aiofiles.open("rooms.csv", "r") as f:
         csvlines = await f.readlines()
         entities = [build_entity(csvline) for csvline in csvlines]
         await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())      

Read JSON files
~~~~~~~~~~~~~~~

Here is the `sample JSON file <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/rooms.json>`_ used in the following examples.

The upper `rooms` JSON array contains JSON objects, each one composed of 3 values :

- the room name *(string)*
- the temperature *(float, degrees Celsius)*
- the pressure *(integer, mmHg)*
  
.. code-block::
   :caption: Base mode

   import json
   from ngsildclient import Entity, Client, iso8601

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", room["temperature"])
      e.prop("pressure", room["pressure"])
      return e

   def main():
      client = Client()
      with open("rooms.json") as f:
         payload: dict = json.load(f)
         for room in payload["rooms"]:
               entity = build_entity(room)
               client.upsert(entity)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Batch variant
   
   import json
   from ngsildclient import Entity, Client, iso8601

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", room["temperature"])
      e.prop("pressure", room["pressure"])
      return e

   def main():
      client = Client()
      with open("rooms.json") as f:
         payload: dict = json.load(f)
         rooms = payload["rooms"]
         entities = [build_entity(room) for room in rooms]
         client.upsert(entities)

   if __name__ == "__main__":
      main()

.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   import aiofiles
   import json
   from ngsildclient import Entity, AsyncClient, iso8601

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", room["temperature"])
      e.prop("pressure", room["pressure"])
      return e

   async def main():
      client = AsyncClient()
      async with aiofiles.open("rooms.json") as f:
         content = await f.read()
         payload: dict = json.loads(content)
      for room in payload["rooms"]:
         entity = build_entity(room)
         await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   import json
   from ngsildclient import Entity, AsyncClient, iso8601

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", room["temperature"])
      e.prop("pressure", room["pressure"])
      return e

   async def main():
      client = AsyncClient()
      with open("rooms.json") as f:
         payload: dict = json.load(f)
         rooms = payload["rooms"]
         entities = [build_entity(room) for room in rooms]
         await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())

Request an API
~~~~~~~~~~~~~~

| Examples below use the CoinGecko_ API that delivers crypto data.
| Here a public endpoint is requested that sends back information about companies that hold bitcoins and their amount.
| Outgoing NGSI-LD entities are created using a custom DataModel named BitcoinCapitalization.
| Fore the sake of the anecdote Tesla got dropped off the list in 2022, after it has sold 75% of its bitcoin holdings.
| The synchronous examples are based on the requests_ library.
| The asynchronous examples are based on the httpx_ library.

| requests_ is required to run the example below.

.. code-block::
   :caption: Base mode

   import requests
   from ngsildclient import Entity, Client, iso8601, Auto

   COINGECKO_BTC_CAP_ENDPOINT = "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin"
   DATA_PROVIDER = "CoinGecko API"

   def build_entity(company: dict) -> Entity:
      market, symbol = [x.strip() for x in company["symbol"].split(":")]
      e = Entity("BitcoinCapitalization", f"{market}:{symbol}:{iso8601.utcnow()}")
      e.obs()
      e.prop("dataProvider", DATA_PROVIDER)
      e.prop("companyName", company["name"])
      e.prop("stockMarket", market)
      e.prop("stockSymbol", symbol)
      e.prop("country", company["country"])
      e.prop("totalHoldings", company["total_holdings"], unitcode="BTC", observedat=Auto)
      e.prop("totalValue", company["total_current_value_usd"], unitcode="USD", observedat=Auto)
      return e

   def main():
      client = Client()
      r = requests.get(COINGECKO_BTC_CAP_ENDPOINT)
      r.raise_for_status()
      companies = r.json()["companies"]
      for company in companies:
         entity = build_entity(company)
         client.upsert(entity)

   if __name__ == "__main__":
      main()

| requests_ is required to run the example below.

.. code-block::
   :caption: Batch variant
   
   import requests
   from ngsildclient import Entity, Client, iso8601, Auto

   COINGECKO_BTC_CAP_ENDPOINT = "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin"
   DATA_PROVIDER = "CoinGecko API"

   def build_entity(company: dict) -> Entity:
      market, symbol = [x.strip() for x in company["symbol"].split(":")]
      e = Entity("BitcoinCapitalization", f"{market}:{symbol}:{iso8601.utcnow()}")
      e.obs()
      e.prop("dataProvider", DATA_PROVIDER)
      e.prop("companyName", company["name"])
      e.prop("stockMarket", market)
      e.prop("stockSymbol", symbol)
      e.prop("country", company["country"])
      e.prop("totalHoldings", company["total_holdings"], unitcode="BTC", observedat=Auto)
      e.prop("totalValue", company["total_current_value_usd"], unitcode="USD", observedat=Auto)
      return e

   def main():
      client = Client()
      r = requests.get(COINGECKO_BTC_CAP_ENDPOINT)
      r.raise_for_status()
      companies = r.json()["companies"]
      entities = [build_entity(c) for c in companies]
      client.upsert(entities)

   if __name__ == "__main__":
      main()

| httpx_ is required to run the example below.

.. code-block::
   :caption: Asynchronous variant
   
   import asyncio
   import httpx
   from ngsildclient import Entity, AsyncClient, iso8601, Auto

   COINGECKO_BTC_CAP_ENDPOINT = "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin"
   DATA_PROVIDER = "CoinGecko API"

   def build_entity(company: dict) -> Entity:
      market, symbol = [x.strip() for x in company["symbol"].split(":")]
      e = Entity("BitcoinCapitalization", f"{market}:{symbol}:{iso8601.utcnow()}")
      e.obs()
      e.prop("dataProvider", DATA_PROVIDER)
      e.prop("companyName", company["name"])
      e.prop("stockMarket", market)
      e.prop("stockSymbol", symbol)
      e.prop("country", company["country"])
      e.prop("totalHoldings", company["total_holdings"], unitcode="BTC", observedat=Auto)
      e.prop("totalValue", company["total_current_value_usd"], unitcode="USD", observedat=Auto)
      return e

   async def main():
      client = AsyncClient()
      r = httpx.get(COINGECKO_BTC_CAP_ENDPOINT)
      r.raise_for_status()
      companies = r.json()["companies"]
      for company in companies:
         entity = build_entity(company)
         await client.upsert(entity)

   if __name__ == "__main__":
      asyncio.run(main())

| httpx_ is required to run the example below.

.. code-block::
   :caption: Asynchronous batch variant
   
   import asyncio
   import httpx
   from ngsildclient import Entity, AsyncClient, iso8601, Auto

   COINGECKO_BTC_CAP_ENDPOINT = "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin"
   DATA_PROVIDER = "CoinGecko API"

   def build_entity(company: dict) -> Entity:
      market, symbol = [x.strip() for x in company["symbol"].split(":")]
      e = Entity("BitcoinCapitalization", f"{market}:{symbol}:{iso8601.utcnow()}")
      e.obs()
      e.prop("dataProvider", DATA_PROVIDER)
      e.prop("companyName", company["name"])
      e.prop("stockMarket", market)
      e.prop("stockSymbol", symbol)
      e.prop("country", company["country"])
      e.prop("totalHoldings", company["total_holdings"], unitcode="BTC", observedat=Auto)
      e.prop("totalValue", company["total_current_value_usd"], unitcode="USD", observedat=Auto)
      return e

   async def main():
      client = AsyncClient()
      r = httpx.get(COINGECKO_BTC_CAP_ENDPOINT)
      r.raise_for_status()
      companies = r.json()["companies"]
      entities = [build_entity(c) for c in companies]
      await client.upsert(entities)

   if __name__ == "__main__":
      asyncio.run(main())      

HTTP server
~~~~~~~~~~~

| Sometimes NGSI-LD agents act as daemons.
| Here in fact it's an HTTP server that **waits for CSV files to be uploaded**.
| When triggered it consumes the CSV file and produces NGSI-LD entities.
| Here is the `sample CSV file <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/rooms.csv>`_ used in the following examples.
| The synchronous example relies on the Flask_ framework.
| The asynchronous example relies on the FastAPI_ framework.

| Flask_ is required to run the example below.

.. code-block::
   :caption: Synchronous mode

   import io
   from flask import Flask, request, Response
   from ngsildclient import Entity, Client, iso8601

   app = Flask(__name__)
   client = Client()

   def build_entity(csvline: str) -> Entity:
      room = csvline.rstrip().split(";")
      e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", float(room[1]))
      e.prop("pressure", int(room[2]))
      return e

   @app.route("/", methods=["POST"])
   def upload_file():
      file = request.files["file"]
      csvlines = io.TextIOWrapper(file).readlines()
      entities = [build_entity(csvline) for csvline in csvlines]
      client.upsert(entities)
      return Response("CSV file processed", status=200)

| FastAPI_ is required to run the example below.

.. code-block::
   :caption: Asynchronous mode

   import io
   from fastapi import FastAPI, UploadFile
   from ngsildclient import Entity, AsyncClient, iso8601

   app = FastAPI()
   client = AsyncClient()

   def build_entity(csvline: str) -> Entity:
      room = csvline.rstrip().split(";")
      e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", float(room[1]))
      e.prop("pressure", int(room[2]))
      return e

   @app.post("/")
   async def upload_file(file: UploadFile):
      file = file.file._file
      csvlines = io.TextIOWrapper(file).readlines()
      entities = [build_entity(csvline) for csvline in csvlines]
      await client.upsert(entities)
      return "CSV file processed"

HTTP REST server
~~~~~~~~~~~~~~~~

| Sometimes NGSI-LD agents act as daemons.
| Here in fact it's an HTTP REST server that **exposes a dedicated endpoint** which **accepts a JSON payload**.
| This endpoint is named ``/rooms`` and the expected payload is a JSON object describing a room.
| When triggered it processes the JSON payload and produces NGSI-LD entities.
| Here is the `sample JSON file <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/room.json>`_ used in the following examples.
| The synchronous example relies on the Flask_ framework.
| The asynchronous example relies on the FastAPI_ framework.

| Flask_ is required to run the example below.

.. code-block::
   :caption: Synchronous mode

   from flask import Flask, request, jsonify
   from ngsildclient import Entity, Client, iso8601

   app = Flask(__name__)
   client = Client()

   def build_entity(room: dict) -> Entity:
      e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", room["temperature"])
      e.prop("pressure", room["pressure"])
      return e

   @app.route("/rooms", methods=["POST"])
   def post_room():
      content_type = request.headers.get("Content-Type")
      if content_type != "application/json":
         return
      entity = build_entity(request.json)
      client.upsert(entity)
      resp = jsonify(entity.to_dict())
      resp.headers = {"Content-Location": client.entities.to_broker_url(entity)}
      resp.status_code = 201
      return resp

| FastAPI_ is required to run the example below.

.. code-block::
   :caption: Asynchronous mode

      from fastapi import FastAPI, Request
      from fastapi.responses import JSONResponse
      from ngsildclient import Entity, AsyncClient, iso8601

      app = FastAPI()
      client = AsyncClient()

      def build_entity(room: dict) -> Entity:
         e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
         e.obs()
         e.prop("temperature", room["temperature"])
         e.prop("pressure", room["pressure"])
         return e

      @app.post("/rooms")
      async def post_room(request: Request):
         payload = await request.json()
         entity = build_entity(payload)
         await client.upsert(entity)
         return JSONResponse(status_code=201, content=entity.to_dict(), headers={"Content-Location": client.entities.to_broker_url(entity)})         

.. _PointOfInterest: https://github.com/smart-data-models/dataModel.PointOfInterest
.. _pandas : https://pypi.org/project/pandas/
.. _DataFrame sample : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html
.. _CoinGecko : https://www.coingecko.com/
.. _Flask : https://flask.palletsprojects.com
.. _FastAPI : https://fastapi.tiangolo.com/
.. _requests : https://requests.readthedocs.io/en/latest/
.. _httpx : https://www.python-httpx.org/
