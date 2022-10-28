from geojson import Polygon
from ngsildclient import Entity, PostalAddressBuilder

geometry = Polygon([[(100, 0), (101, 0), (101, 1), (100, 1), (100, 0)]])

e = Entity("Building", "building-a85e3da145c1")
e.ctx.append("https://raw.githubusercontent.com/smart-data-models/dataModel.Building/master/context.jsonld")
