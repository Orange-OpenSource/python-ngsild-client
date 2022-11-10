Cookbook
========

How to develop NGSI-LD agents
-----------------------------

This chapter shows how to develop NGSI-LD Agents that implement the whole pipeline :

- Acquire some data
- Convert incoming data into NGSI-LD entities : here goes your business logic
- Send outgoing entities to the NGSI-LD broker

Various heterogeneous datasources have been selected to showcase the **ngsildclient** library at work.

All examples below use a NGSI-LD local instance.

To that end, some ready-to-use docker-compose files are available in the github repository under the folder `brokers <https://github.com/Orange-OpenSource/python-ngsild-client/tree/master/brokers>`_ .

Code samples are available in the github repository under the folder `cookbook/agents <https://github.com/Orange-OpenSource/python-ngsild-client/tree/master/cookbook/agents>`_.

Prefer synchronous agent if you need interactivity (i.e. inside Jupyter Notebooks), aim at simplicity and performance is not an issue.

Prefer asynchronous agent when interactivity is not required and seeking for performance, i.e. a real-time agent that collects data and sends entities to the broker at a high frequency rate.

Combine batch upserts and Asynchronous IO to achieve best performances.

.. note::
   | The ``build_entity()`` function creates entities from the incoming data.
   | It is a good place to enrich data, i.e. by requesting a database or an API.
   | As soon as it performs I/O you can benefit from making it ``async``.

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

Here is the sample JSON file `rooms.json <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/rooms.json>`_ used in the following examples.

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
| Here is the sample CSV file `rooms.csv <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/rooms.csv>`_ used in the following examples.

| The synchronous example relies on the Flask_ framework.
| The asynchronous example relies on the FastAPI_ framework.

| Flask_ is required to run the example below.

.. code-block:: bash
   :caption: command to run the Flask application

   flask --app tutorial40_api_server_flask_upload_csv run

.. code-block:: bash
   :caption: curl command to test against the Flask server

   curl -v -F "file=@rooms.csv" http://127.0.0.1:5000

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

.. code-block:: bash
   :caption: command to run the FastAPI application

   uvicorn tutorial41_api_server_fastapi_upload_csv_async:app

.. code-block:: bash
   :caption: curl command to test against the FastAPI server

   curl -v -F "file=@rooms.csv" http://127.0.0.1:8000

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
| Here is the sample JSON file `room.json <https://github.com/Orange-OpenSource/python-ngsild-client/blob/master/cookbook/agents/data/room.json>`_ used in the following examples.
| The synchronous example relies on the Flask_ framework.
| The asynchronous example relies on the FastAPI_ framework.

| Flask_ is required to run the example below.

.. code-block:: bash
   :caption: command to start the Flask server

   flask --app tutorial42_api_server_flask_rest_json run

.. code-block:: bash
   :caption: curl command to test against the Flask server

   curl -X POST -H "Content-Type: application/json" -d "@room.json" http://127.0.0.1:5000/rooms

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

.. code-block:: bash
   :caption: command to start the FastAPI server

   uvicorn tutorial43_api_server_fastapi_rest_json_async:app

.. code-block:: bash
   :caption: curl command to test against the FastAPI server

   curl -X POST -H "Content-Type: application/json" -d "@room.json" http://127.0.0.1:8000/rooms

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

This last example adds body validation, thanks to pydantic_.

.. code-block:: bash
   :caption: command to start the FastAPI server

   uvicorn tutorial44_api_server_fastapi_rest_json_async_with_validation:app

.. code-block::
   :caption: Asynchronous mode with body validation

   from fastapi import FastAPI
   from pydantic import BaseModel
   from fastapi.responses import JSONResponse
   from ngsildclient import Entity, AsyncClient, iso8601

   app = FastAPI()
   client = AsyncClient()

   class RoomObserved(BaseModel):
      id: str
      temperature: float
      pressure: int

   def build_entity(room: RoomObserved) -> Entity:
      e = Entity("RoomObserved", f"{room.id}:{iso8601.utcnow()}")
      e.obs()
      e.prop("temperature", room.temperature)
      e.prop("pressure", room.pressure)
      return e

   @app.post("/rooms")
   async def post_room(room: RoomObserved):
      entity = build_entity(room)
      await client.upsert(entity)
      return JSONResponse(
         status_code=201, content=entity.to_dict(), headers={"Content-Location": client.entities.to_broker_url(entity)}
      )         

How to forge NGSI-LD entities
-----------------------------

| Some entities from the Smart Data Models Initiative built with the library.
| Code samples are available in the github repository under the folder `cookbook/entities <https://github.com/Orange-OpenSource/python-ngsild-client/tree/master/cookbook/entities>`_.

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
   poi.prop("description", "La Playa de A Concha se presenta como una continuacion de la Playa de Compostela, una de las mas frecuentadas de Vilagarcia.")
   poi.loc((42.60214472222222, -8.768460000000001))
   poi.prop("source", "http://www.tourspain.es")
   poi.prop("refSeeAlso", ["urn:ngsi-ld:SeeAlso:Beach-A-Concha-123456"])

Device
~~~~~~

Device_ on SmartDataModels repository.

.. code-block:: json-ld
   :caption: Device NGSI-LD normalized example

   {
      "@context": [
         "https://smartdatamodels.org/context.jsonld"
      ],
      "id": "urn:ngsi-ld:Device:device-9845A",
      "type": "Device",
      "category": {
         "type": "Property",
         "value": [
               "sensor"
         ]
      },
      "batteryLevel": {
         "type": "Property",
         "value": 0.75
      },
      "dateFirstUsed": {
         "type": "Property",
         "value": {
               "@type": "DateTime",
               "@value": "2014-09-11T11:00:00Z"
         }
      },
      "controlledAsset": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:wastecontainer-Osuna-100"
      },
      "serialNumber": {
         "type": "Property",
         "value": "9845A"
      },
      "ipAddress": {
         "type": "Property",
         "value": "192.14.56.78"
      },
      "mcc": {
         "type": "Property",
         "value": "214"
      },
      "mnc": {
         "type": "Property",
         "value": "07"
      },
      "rssi": {
         "type": "Property",
         "value": 0.86
      },
      "value": {
         "type": "Property",
         "value": "l%3D0.22%3Bt%3D21.2"
      },
      "refDeviceModel": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:DeviceModel:myDevice-wastecontainer-sensor-345"
      },
      "controlledProperty": {
         "type": "Property",
         "value": [
               "fillingLevel",
               "temperature"
         ]
      },
      "owner": {
         "type": "Property",
         "value": "http://person.org/leon"
      },
      "deviceState": {
         "type": "Property",
         "value": "ok"
      },
      "distance": {
         "type": "Property",
         "value": 20,
         "unitCode": "MTR"
      },
      "depth": {
         "type": "Property",
         "value": 3,
         "unitCode": "MTR"
      },
      "direction": {
         "type": "Property",
         "value": "Outlet"
      }
   }

.. code-block::
   :caption: Device code snippet

   from ngsildclient import Entity

    e = Entity(
        "Device",
        "Device:device-9845A",
        ctx=["https://smartdatamodels.org/context.jsonld"],
    )
    e.prop("category", ["sensor"])
    e.prop("batteryLevel", 0.75)
    e.tprop("dateFirstUsed", "2014-09-11T11:00:00Z")
    e.rel("controlledAsset", "wastecontainer-Osuna-100")
    e.prop("serialNumber", "9845A")
    e.prop("ipAddress", "192.14.56.78")
    e.prop("mcc", "214")
    e.prop("mnc", "07")
    e.prop("rssi", 0.86)
    e.prop("value", "l%3D0.22%3Bt%3D21.2")
    e.rel("refDeviceModel", "DeviceModel:myDevice-wastecontainer-sensor-345")
    e.prop("controlledProperty", ["fillingLevel", "temperature"])
    e.prop("owner", "http://person.org/leon")
    e.prop("deviceState", "ok")
    e.prop("distance", 20, unitcode="MTR")
    e.prop("depth", 3, unitcode="MTR")
    e.prop("direction", "Outlet")

.. code-block:: json-ld
   :caption: DeviceModel NGSI-LD normalized example

   {
      "@context": [
         "https://smartdatamodels.org/context.jsonld",
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:DeviceModel:myDevice-wastecontainer-sensor-345",
      "type": "DeviceModel",
      "category": {
         "type": "Property",
         "value": [
               "sensor"
         ]
      },
      "function": {
         "type": "Property",
         "value": [
               "sensing"
         ]
      },
      "modelName": {
         "type": "Property",
         "value": "S4Container 345"
      },
      "name": {
         "type": "Property",
         "value": "myDevice Sensor for Containers 345"
      },
      "brandName": {
         "type": "Property",
         "value": "myDevice"
      },
      "manufacturerName": {
         "type": "Property",
         "value": "myDevice Inc."
      },
      "controlledProperty": {
         "type": "Property",
         "value": [
               "fillingLevel",
               "temperature"
         ]
      }
   }

.. code-block::
   :caption: DeviceModel code snippet

   from ngsildclient import Entity

    e = Entity(
        "DeviceModel",
        "DeviceModel:myDevice-wastecontainer-sensor-345",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("category", ["sensor"])
    e.prop("function", ["sensing"])
    e.prop("modelName", "S4Container 345")
    e.prop("name", "myDevice Sensor for Containers 345")
    e.prop("brandName", "myDevice")
    e.prop("manufacturerName", "myDevice Inc.")
    e.prop("controlledProperty", ["fillingLevel", "temperature"])    

SmartAgri
~~~~~~~~~

SmartAgrifood_ on SmartDataModels repository.

.. code-block:: json-ld
   :caption: AgriCrop NGSI-LD normalized example

   {
      "@context": [
         "https://smartdatamodels.org/context.jsonld",
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AgriCrop:df72dc57-1eb9-42a3-88a9-8647ecc954b4",
      "type": "AgriCrop",
      "name": {
         "type": "Property",
         "value": "Wheat"
      },
      "alternateName": {
         "type": "Property",
         "value": "Triticum aestivum"
      },
      "description": {
         "type": "Property",
         "value": "Spring wheat"
      },
      "agroVocConcept": {
         "type": "Property",
         "value": "http://aims.fao.org/aos/agrovoc/c_7951"
      },
      "wateringFrequency": {
         "type": "Property",
         "value": "daily"
      },
      "harvestingInterval": {
         "type": "Property",
         "value": [
               {
                  "dateRange": "-03-21/-04-01",
                  "description": "Best Season"
               },
               {
                  "dateRange": "-04-02/-04-15",
                  "description": "Season OK"
               }
         ]
      },
      "hasAgriFertiliser": {
         "type": "Property",
         "value": [
               "urn:ngsi-ld:AgriFertiliser:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
               "urn:ngsi-ld:AgriFertiliser:380973c8-4d3b-4723-a899-0c0c5cc63e7e"
         ]
      },
      "hasAgriPest": {
         "type": "Property",
         "value": [
               "urn:ngsi-ld:AgriPest:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
               "urn:ngsi-ld:AgriPest:380973c8-4d3b-4723-a899-0c0c5cc63e7e"
         ]
      },
      "hasAgriSoil": {
         "type": "Property",
         "value": [
               "urn:ngsi-ld:AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
               "urn:ngsi-ld:AgriSoil:e8a8389a-edf5-4345-8d2c-b98ac1ce8e2a"
         ]
      },
      "plantingFrom": {
         "type": "Property",
         "value": [
               {
                  "dateRange": "-09-28/-10-12",
                  "description": "Best Season"
               },
               {
                  "dateRange": "-10-11/-10-18",
                  "description": "Season OK"
               }
         ]
      },
      "relatedSource": {
         "type": "Property",
         "value": [
               {
                  "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
                  "applicationEntityId": "app:weat"
               }
         ]
      },
      "seeAlso": {
         "type": "Property",
         "value": [
               "https://example.org/concept/wheat",
               "https://datamodel.org/example/wheat"
         ]
      }
   }

.. code-block::
   :caption: AgriCrop code snippet

   from ngsildclient import Entity

    e = Entity(
        "AgriCrop",
        "AgriCrop:df72dc57-1eb9-42a3-88a9-8647ecc954b4",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("name", "Wheat")
    e.prop("alternateName", "Triticum aestivum")
    e.prop("description", "Spring wheat")
    e.prop("agroVocConcept", "http://aims.fao.org/aos/agrovoc/c_7951")
    e.prop("wateringFrequency", "daily")
    e.prop(
        "harvestingInterval",
        [
            {"dateRange": "-03-21/-04-01", "description": "Best Season"},
            {"dateRange": "-04-02/-04-15", "description": "Season OK"},
        ],
    )
    e.prop(
        "hasAgriFertiliser",
        [
            "urn:ngsi-ld:AgriFertiliser:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
            "urn:ngsi-ld:AgriFertiliser:380973c8-4d3b-4723-a899-0c0c5cc63e7e",
        ],
    )
    e.prop(
        "hasAgriPest",
        [
            "urn:ngsi-ld:AgriPest:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
            "urn:ngsi-ld:AgriPest:380973c8-4d3b-4723-a899-0c0c5cc63e7e",
        ],
    )
    e.prop(
        "hasAgriSoil",
        [
            "urn:ngsi-ld:AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
            "urn:ngsi-ld:AgriSoil:e8a8389a-edf5-4345-8d2c-b98ac1ce8e2a",
        ],
    )
    e.prop(
        "plantingFrom",
        [
            {"dateRange": "-09-28/-10-12", "description": "Best Season"},
            {"dateRange": "-10-11/-10-18", "description": "Season OK"},
        ],
    )
    e.prop(
        "relatedSource",
        [
            {
                "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
                "applicationEntityId": "app:weat",
            }
        ],
    )
    e.prop(
        "seeAlso",
        ["https://example.org/concept/wheat", "https://datamodel.org/example/wheat"],
    )

.. code-block:: json-ld
   :caption: AgriSoil NGSI-LD normalized example

   {
      "@context": [
         "https://smartdatamodels.org/context.jsonld",
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
      "type": "AgriSoil",
      "name": {
         "type": "Property",
         "value": "Clay"
      },
      "alternateName": {
         "type": "Property",
         "value": "Heavy soil"
      },
      "description": {
         "type": "Property",
         "value": "Fine grained, poor draining soil. Particle size less than 0.002mm"
      },
      "agroVocConcept": {
         "type": "Property",
         "value": "http://aims.fao.org/aos/agrovoc/c_7951"
      },
      "hasAgriProductType": {
         "type": "Property",
         "value": [
               "urn:ngsi-ld:AgriProductType:ea54eedf-d5a7-4e44-bddd-50e9935237c0",
               "urn:ngsi-ld:AgriProductType:275b4c08-5e52-4bb7-8523-74ce5d0007de"
         ]
      },
      "relatedSource": {
         "type": "Property",
         "value": [
               {
                  "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
                  "applicationEntityId": "app:clay"
               }
         ]
      },
      "seeAlso": {
         "type": "Property",
         "value": [
               "https://example.org/concept/clay",
               "https://datamodel.org/example/clay"
         ]
      }
   }

.. code-block::
   :caption: AgriSoil code snippet

   from ngsildclient import Entity

    e = Entity(
        "AgriSoil",
        "AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("name", "Clay")
    e.prop("alternateName", "Heavy soil")
    e.prop(
        "description",
        "Fine grained, poor draining soil. Particle size less than 0.002mm",
    )
    e.prop("agroVocConcept", "http://aims.fao.org/aos/agrovoc/c_7951")
    e.prop(
        "hasAgriProductType",
        [
            "urn:ngsi-ld:AgriProductType:ea54eedf-d5a7-4e44-bddd-50e9935237c0",
            "urn:ngsi-ld:AgriProductType:275b4c08-5e52-4bb7-8523-74ce5d0007de",
        ],
    )
    e.prop(
        "relatedSource",
        [
            {
                "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
                "applicationEntityId": "app:clay",
            }
        ],
    )
    e.prop(
        "seeAlso",
        ["https://example.org/concept/clay", "https://datamodel.org/example/clay"],
    )

SmartCities
~~~~~~~~~~~

SmartCities_ on SmartDataModels repository.

.. code-block:: json-ld
   :caption: Building NGSI-LD normalized example

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Building:building-a85e3da145c1",
      "type": "Building",
      "address": {
         "type": "Property",
         "value": {
               "streetAddress": "25 Walbrook",
               "addressLocality": "London",
               "postalCode": "EC4N 8AF"
         }
      },
      "category": {
         "type": "Property",
         "value": [
               "office"
         ]
      },
      "containedInPlace": {
         "type": "GeoProperty",
         "value": {
               "type": "Polygon",
               "coordinates": [
                  [
                     [
                           100,
                           0
                     ],
                     [
                           101,
                           0
                     ],
                     [
                           101,
                           1
                     ],
                     [
                           100,
                           1
                     ],
                     [
                           100,
                           0
                     ]
                  ]
               ]
         }
      },
      "dataProvider": {
         "type": "Property",
         "value": "OperatorA"
      },
      "description": {
         "type": "Property",
         "value": "Office block"
      },
      "floorsAboveGround": {
         "type": "Property",
         "value": 7
      },
      "floorsBelowGround": {
         "type": "Property",
         "value": 0
      },
      "location": {
         "type": "GeoProperty",
         "value": {
               "type": "Polygon",
               "coordinates": [
                  [
                     [
                           100,
                           0
                     ],
                     [
                           101,
                           0
                     ],
                     [
                           101,
                           1
                     ],
                     [
                           100,
                           1
                     ],
                     [
                           100,
                           0
                     ]
                  ]
               ]
         }
      },
      "mapUrl": {
         "type": "Property",
         "value": "http://www.example.com"
      },
      "occupier": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:Person:9830f692-7677-11e6-838b-4f9fb3dc5a4f"
      },
      "openingHours": {
         "type": "Property",
         "value": [
               {
                  "opens": "10:00",
                  "closes": "19:00",
                  "dayOfWeek": "Monday"
               },
               {
                  "opens": "10:00",
                  "closes": "19:00",
                  "dayOfWeek": "Tuesday"
               },
               {
                  "opens": "10:00",
                  "closes": "22:00",
                  "dayOfWeek": "Saturday"
               },
               {
                  "opens": "10:00",
                  "closes": "21:00",
                  "dayOfWeek": "Sunday"
               }
         ]
      },
      "owner": [
         {
               "type": "Relationship",
               "object": "urn:ngsi-ld:cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84"
         },
         {
               "type": "Relationship",
               "object": "urn:ngsi-ld:1be9cd61-ef59-421f-a326-4b6c84411ad4"
         }
      ],
      "source": {
         "type": "Property",
         "value": "http://www.example.com"
      }
   }

.. code-block::
   :caption: Building code snippet

   from datetime import time
   from geojson import Polygon
   from ngsildclient import Entity, PostalAddressBuilder, OpeningHoursBuilder

    polygon = Polygon([[(100, 0), (101, 0), (101, 1), (100, 1), (100, 0)]])
    e = Entity("Building", "building-a85e3da145c1")
    e.addr(PostalAddressBuilder().locality("London").postalcode("EC4N 8AF").street("25 Walbrook").build())
    e.prop("category", ["office"])
    e.gprop("containedInPlace", polygon)
    e.prop("dataProvider", "OperatorA").prop("description", "Office block")
    e.prop("floorsAboveGround", 7).prop("floorsBelowGround", 0)
    e.loc(polygon)
    e.prop("mapUrl", "http://www.example.com")
    e.rel("occupier", "Person:9830f692-7677-11e6-838b-4f9fb3dc5a4f")
    e.prop(
        "openingHours",
        OpeningHoursBuilder()
        .monday(time(10), time(19))
        .tuesday(time(10), time(19))
        .saturday(time(10), time(22))
        .sunday(time(10), time(21))
        .build(),
    )
    e.rel(
        "owner",
        [
            "cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84",
            "1be9cd61-ef59-421f-a326-4b6c84411ad4",
        ],
    )
    e.prop("source", "http://www.example.com")

.. code-block:: json-ld
   :caption: UrbanMobility NGSI-LD normalized example

   {
      "@context": [
         "https://smart-data-models.github.io/data-models/context.jsonld",
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:PublicTransportStop:santander:busStop:463",
      "type": "PublicTransportStop",
      "dateModified": {
         "type": "Property",
         "value": {
               "@type": "DateTime",
               "@value": "2018-09-25T08:32:26Z"
         }
      },
      "source": {
         "type": "Property",
         "value": "https://api.smartsantander.eu/"
      },
      "dataProvider": {
         "type": "Property",
         "value": "http://www.smartsantander.eu/"
      },
      "entityVersion": {
         "type": "Property",
         "value": "2.0"
      },
      "address": {
         "type": "Property",
         "value": {
               "streetAddress": "C/ La Pereda 14",
               "addressLocality": "Santander",
               "addressRegion": "Cantabria",
               "addressCountry": "Spain"
         }
      },
      "location": {
         "type": "GeoProperty",
         "value": {
               "type": "Point",
               "coordinates": [
                  -3.804648,
                  43.478053
               ]
         }
      },
      "stopCode": {
         "type": "Property",
         "value": "la_pereda_463"
      },
      "shortStopCode": {
         "type": "Property",
         "value": "463"
      },
      "name": {
         "type": "Property",
         "value": "La Pereda 14"
      },
      "wheelchairAccessible": {
         "type": "Property",
         "value": 0
      },
      "transportationType": {
         "type": "Property",
         "value": [
               3
         ]
      },
      "refPublicTransportRoute": {
         "type": "Property",
         "value": [
               "urn:ngsi-ld:PublicTransportRoute:santander:transport:busLine:N3",
               "urn:ngsi-ld:PublicTransportRoute:santander:transport:busLine:N4"
         ]
      },
      "peopleCount": {
         "type": "Property",
         "value": 0
      },
      "refPeopleCountDevice": {
         "type": "Property",
         "value": "urn:ngsi-ld:PorpleCountDecice:santander:463"
      },
      "openingHoursSpecification": {
         "type": "Property",
         "value": [
               {
                  "opens": "00:01",
                  "closes": "23:59",
                  "dayOfWeek": "Monday"
               },
               {
                  "opens": "00:01",
                  "closes": "23:59",
                  "dayOfWeek": "Tuesday"
               },
               {
                  "opens": "00:01",
                  "closes": "23:59",
                  "dayOfWeek": "Wednesday"
               },
               {
                  "opens": "00:01",
                  "closes": "23:59",
                  "dayOfWeek": "Thursday"
               },
               {
                  "opens": "00:01",
                  "closes": "23:59",
                  "dayOfWeek": "Friday"
               }
         ]
      }
   }

.. code-block::
   :caption: UrbanMobility code snippet

   from datetime import datetime
   from dateutil.tz import UTC
   from ngsildclient import Entity, PostalAddressBuilder, OpeningHoursBuilder
   from ngsildclient.utils.urn import Urn

    e = Entity(
        "PublicTransportStop",
        "PublicTransportStop:santander:busStop:463",
        ctx=[
            "https://smart-data-models.github.io/data-models/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.tprop("dateModified", datetime(2018, 9, 25, 8, 32, 26, tzinfo=UTC))
    e.prop("source", "https://api.smartsantander.eu/")
    e.prop("dataProvider", "http://www.smartsantander.eu/")
    e.prop("entityVersion", "2.0")
    builder = PostalAddressBuilder()
    address = builder.street("C/ La Pereda 14").locality("Santander").region("Cantabria").country("Spain").build()
    e.prop("address", address)
    e.gprop("location", (43.478053126, -3.804648385))
    e.prop("stopCode", "la_pereda_463")
    e.prop("shortStopCode", "463")
    e.prop("name", "La Pereda 14")
    e.prop("wheelchairAccessible", 0)
    e.prop("transportationType", [3])
    e.prop(
        "refPublicTransportRoute",
        [
            "urn:ngsi-ld:PublicTransportRoute:santander:transport:busLine:N3",
            "urn:ngsi-ld:PublicTransportRoute:santander:transport:busLine:N4",
        ],
    )
    e.prop("peopleCount", 0)
    e.prop("refPeopleCountDevice", Urn.prefix("PorpleCountDecice:santander:463"))
    builder = OpeningHoursBuilder()
    openinghours = builder.businessdays("00:01", "23:59").build()
    e.prop("openingHoursSpecification", openinghours)

.. code-block:: json-ld
   :caption: Weather NGSI-LD normalized example

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Building:building-a85e3da145c1",
      "type": "Building",
      "address": {
         "type": "Property",
         "value": {
               "streetAddress": "25 Walbrook",
               "addressLocality": "London",
               "postalCode": "EC4N 8AF"
         }
      },
      "category": {
         "type": "Property",
         "value": [
               "office"
         ]
      },
      "containedInPlace": {
         "type": "GeoProperty",
         "value": {
               "type": "Polygon",
               "coordinates": [
                  [
                     [
                           100,
                           0
                     ],
                     [
                           101,
                           0
                     ],
                     [
                           101,
                           1
                     ],
                     [
                           100,
                           1
                     ],
                     [
                           100,
                           0
                     ]
                  ]
               ]
         }
      },
      "dataProvider": {
         "type": "Property",
         "value": "OperatorA"
      },
      "description": {
         "type": "Property",
         "value": "Office block"
      },
      "floorsAboveGround": {
         "type": "Property",
         "value": 7
      },
      "floorsBelowGround": {
         "type": "Property",
         "value": 0
      },
      "location": {
         "type": "GeoProperty",
         "value": {
               "type": "Polygon",
               "coordinates": [
                  [
                     [
                           100,
                           0
                     ],
                     [
                           101,
                           0
                     ],
                     [
                           101,
                           1
                     ],
                     [
                           100,
                           1
                     ],
                     [
                           100,
                           0
                     ]
                  ]
               ]
         }
      },
      "mapUrl": {
         "type": "Property",
         "value": "http://www.example.com"
      },
      "occupier": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:Person:9830f692-7677-11e6-838b-4f9fb3dc5a4f"
      },
      "openingHours": {
         "type": "Property",
         "value": [
               {
                  "opens": "10:00",
                  "closes": "19:00",
                  "dayOfWeek": "Monday"
               },
               {
                  "opens": "10:00",
                  "closes": "19:00",
                  "dayOfWeek": "Tuesday"
               },
               {
                  "opens": "10:00",
                  "closes": "22:00",
                  "dayOfWeek": "Saturday"
               },
               {
                  "opens": "10:00",
                  "closes": "21:00",
                  "dayOfWeek": "Sunday"
               }
         ]
      },
      "owner": [
         {
               "type": "Relationship",
               "object": "urn:ngsi-ld:cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84"
         },
         {
               "type": "Relationship",
               "object": "urn:ngsi-ld:1be9cd61-ef59-421f-a326-4b6c84411ad4"
         }
      ],
      "source": {
         "type": "Property",
         "value": "http://www.example.com"
      }
   }

.. code-block::
   :caption: Weather code snippet

   from ngsildclient import Entity, PostalAddressBuilder

    e = Entity(
        "WeatherObserved",
        "WeatherObserved:Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00.00Z",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.tprop("dateObserved", "2016-11-30T07:00:00Z")
    e.prop("illuminance", 1000)
    e.prop("temperature", 3.3)
    e.prop("precipitation", 0)
    e.prop("atmosphericPressure", 938.9)
    e.prop("pressureTendency", 0.5)
    e.rel("refDevice", "Device:device-0A3478")
    e.prop("source", "http://www.aemet.es")
    e.prop("dataProvider", "http://www.smartsantander.eu/")
    e.prop("windSpeed", 2)
    e.gprop("location", (41.640833333, -4.754444444))
    e.prop("stationName", "Valladolid")
    builder = PostalAddressBuilder()
    address = (
        builder.street("C/ La Pereda 14")
        .locality("Santander")
        .region("Cantabria")
        .country("Spain")
        .build()
    )
    e.prop("address", address)
    builder = PostalAddressBuilder()
    address = builder.locality("Valladolid").country("ES").build()
    e.prop("address", address).prop("stationCode", 2422).prop("dataProvider", "TEF")
    e.prop("windDirection", -45).prop("relativeHumidity", 1)
    e.prop("streamGauge", 50).prop("snowHeight", 20).prop("uvIndexMax", 1.0)

SmartWater
~~~~~~~~~~

SmartWater_ on SmartDataModels repository.

.. code-block:: json-ld
   :caption: Pipe NGSI-LD normalized example

   {
      "@context": [
         "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:Pipe:74azsty-70d4l-4da9-b7d0-3340ef655nnb",
      "type": "Pipe",
      "bulkCoeff": {
         "type": "Property",
         "value": 72.4549,
         "unitCode": "E91"
      },
      "description": {
         "type": "Property",
         "value": "Free Text"
      },
      "diameter": {
         "type": "Property",
         "value": 203,
         "unitCode": "MMT"
      },
      "endsAt": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:Reservoir:1863179e-3768-4480-9167-ff21f870dd19"
      },
      "flow": {
         "type": "Property",
         "value": 20,
         "unitCode": "G51",
         "observedBy": {
               "type": "Relationship",
               "object": "urn:ngsi-ld:Device:device-9845A"
         }
      },
      "inititalStatus": {
         "type": "Property",
         "value": "OPEN"
      },
      "length": {
         "type": "Property",
         "value": 52.9,
         "unitCode": "MTR"
      },
      "minorLoss": {
         "type": "Property",
         "value": 72.4549,
         "unitCode": "C62"
      },
      "quality": {
         "type": "Property",
         "value": 0.5,
         "unitCode": "F27",
         "observedBy": {
               "type": "Relationship",
               "object": "urn:ngsi-ld:Device:device-9845A"
         }
      },
      "roughness": {
         "type": "Property",
         "value": 72.4549,
         "unitCode": "C62"
      },
      "startsAt": {
         "type": "Relationship",
         "object": "urn:ngsi-ld:Junction:63fe7d79-0d4c-4da9-b7d0-3340efa0656a"
      },
      "status": {
         "type": "Property",
         "value": "OPEN"
      },
      "tag": {
         "type": "Property",
         "value": "DMA1"
      },
      "velocity": {
         "type": "Property",
         "value": 2,
         "unitCode": "MTS",
         "observedBy": {
               "type": "Relationship",
               "object": "urn:ngsi-ld:Device:device-9845A"
         }
      },
      "vertices": {
         "type": "GeoProperty",
         "value": {
               "type": "MultiPoint",
               "coordinates": [
                  [
                     [
                           24.40623,
                           60.17966
                     ],
                     [
                           24.50623,
                           60.27966
                     ]
                  ]
               ]
         }
      },
      "wallCoeff": {
         "type": "Property",
         "value": 72.4549,
         "unitCode": "RRC"
      }
   }

.. code-block::
   :caption: Pipe code snippet

   from geojson import MultiPoint
   from ngsildclient import Entity, NESTED, Rel

    device = "Device:device-9845A"
    e = Entity("Pipe", "74azsty-70d4l-4da9-b7d0-3340ef655nnb")
    e.prop("bulkCoeff", 72.4549, unitcode="E91")
    e.prop("description", "Free Text")
    e.prop("diameter", 203, unitcode="MMT")
    e.rel("endsAt", "Reservoir:1863179e-3768-4480-9167-ff21f870dd19")
    e.prop("flow", 20, unitcode="G51").rel(Rel.OBSERVED_BY, device, NESTED)
    e.prop("inititalStatus", "OPEN").prop("length", 52.9, unitcode="MTR")
    e.prop("minorLoss", 72.4549, unitcode="C62")
    e.prop("quality", 0.5, unitcode="F27").rel(Rel.OBSERVED_BY, device, NESTED)
    e.prop("roughness", 72.4549, unitcode="C62")
    e.rel("startsAt", "Junction:63fe7d79-0d4c-4da9-b7d0-3340efa0656a")
    e.prop("status", "OPEN").prop("tag", "DMA1")
    e.prop("velocity", 2, unitcode="MTS").rel(Rel.OBSERVED_BY, device, NESTED)
    e.gprop("vertices", MultiPoint([[(24.40623, 60.17966), (24.50623, 60.27966)]]))
    e.prop("wallCoeff", 72.4549, unitcode="RRC")

.. _pandas : https://pypi.org/project/pandas/
.. _DataFrame sample : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html
.. _CoinGecko : https://www.coingecko.com/
.. _Flask : https://flask.palletsprojects.com
.. _FastAPI : https://fastapi.tiangolo.com/
.. _requests : https://requests.readthedocs.io/en/latest/
.. _httpx : https://www.python-httpx.org/
.. _pydantic : https://github.com/pydantic/pydantic
.. _PointOfInterest: https://github.com/smart-data-models/dataModel.PointOfInterest
.. _Device: https://github.com/smart-data-models/dataModel.Device
.. _SmartAgrifood: https://github.com/smart-data-models/dataModel.Agrifood
.. _SmartCities: https://github.com/smart-data-models/SmartCities
.. _SmartWater: https://github.com/smart-data-models/SmartWater
