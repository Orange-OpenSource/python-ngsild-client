from datetime import datetime
from ngsildclient import Entity, PostalAddressBuilder

obstime = datetime(2018, 9, 21, 12)  # Time of Observation

e = Entity("OffStreetParking", "porto-ParkingLot-23889")
e.ctx = ["https://raw.githubusercontent.com/smart-data-models/dataModel.Parking/master/context.jsonld"]
e.tprop("accessModified", obstime)
e.prop("address", PostalAddressBuilder().locality("Porto").country("Portugal").street("Rua de Fernandes Tomas").build())
e.prop("allowedVehicleType", ["car"])
e.prop("availableSpotNumber", 132, observedat=obstime)
e.prop("category", ["underground", "public", "feeCharged", "mediumTerm", "barrierAccess"])
e.prop("chargeType", ["temporaryPrice"])
e.prop("description", "Municipal car park located near the Trindade metro station and the Town Hall")
e.prop("extCategory", ["A"])
e.prop("fourWheelerSlots", {"availableSpotNumber": 25, "totalSpotNumber": 25, "occupiedSpotNumber": 0})
e.prop("layout", ["multiLevel"])
e.loc(41.150691773, -8.60961198807, precision=11)
e.prop("maximumParkingDuration", "PT8H")
e.prop(
    "municipalityInfo",
    {
        "district": "Bangalore Urban",
        "ulbName": "BMC",
        "cityId": "23",
        "wardId": "23",
        "stateName": "Karnataka",
        "cityName": "Bangalore",
        "zoneName": "South",
        "wardName": "Bangalore Urban",
        "zoneId": "2",
        "wardNum": 4,
    },
)
e.prop("name", "Parque de estacionamento Trindade")
e.tprop("observationDateTime", "2021-03-11T15:51:02Z").prop("occupancy", 0.68).tprop("occupancyModified", obstime)
e.prop("occupiedSpotNumber", 282).prop("parkingSiteID", "P2")
e.prop("requiredPermit", []).prop("totalSpotNumber", 414)
e.prop("twoWheelerSlots", {"availableSpotNumber": 20, "totalSpotNumber": 20, "occupiedSpotNumber": 0})
e.prop("unclassifiedSlots", {"availableSpotNumber": 0, "totalSpotNumber": 0, "occupiedSpotNumber": 0})
e.prop("vehicleEntranceCount", 28).prop("vehicleExitCount", 12)
