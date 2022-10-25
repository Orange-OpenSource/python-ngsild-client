# [Orion-LD](https://github.com/FIWARE/context.Orion-LD)

## Orion-LD Context Broker

```console
$ docker compose up -d
```

```python
from ngsildclient import CLient

client = Client() # localhost, default port : 1026
```

## Orion-LD Context Broker w/TRoE enabled

```console
$ docker compose -f docker-compose-troe.yml up -d
```

```python
from ngsildclient import CLient

client = Client(port=8026, port_temporal=8027) # localhost, Orion LD port : 8026, Mintaka port : 8027
```