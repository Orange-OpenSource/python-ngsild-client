from ngsildclient import Entity, MultAttrValue, mkprop

e = Entity("Vehicle", "A4567")
e.ctx.append(
    {
        "Vehicle": "http://example.org/Vehicle",
        "speed": "http://example.org/speed",
        "source": "http://example.org/hasSource",
    }
)
speed = MultAttrValue(unitcode="KMH") # KMH is the default unit code for all the speed attributes
speed.add(55.0, datasetid="Property:speedometerA4567-speed", userdata=mkprop("source", "Speedometer"))
speed.add(54.5, datasetid="Property:gpsBxyz123-speed", userdata=mkprop("source", "GPS"))
e.prop("speed", speed)
