from ngsildclient import Entity

e = Entity("Vehicle", "A4567")
e.ctx.append(
    {
        "Vehicle": "http://example.org/Vehicle",
        "speed": "http://example.org/speed",
        "source": "http://example.org/hasSource",
    }
)
e.prop("speed", 55.0, unitcode="KMH").prop("source", "Speedometer", nested=True)
speed = e["speed"]*2 # obtain a list of 2 speed properties (duplicated from the one just created)
speed[0].datasetid = "Property:speedometerA4567-speed"
speed[1].datasetid = "Property:gpsBxyz123-speed"
speed[1].value = 54.5
speed[1]["source"].value = "GPS"
e["speed"] = speed
