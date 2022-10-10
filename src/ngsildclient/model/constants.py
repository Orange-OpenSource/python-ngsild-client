#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

"""This module contains constants used in the model package.
"""

from __future__ import annotations

from enum import Enum
from typing import Union, Sequence, TYPE_CHECKING
from datetime import datetime, date, time, timezone
from zoneinfo import ZoneInfo
from geojson import Point, LineString, Polygon

from ..utils.sentinel import Sentinel

if TYPE_CHECKING:
    import ngsildclient.model.entity as entity
    EntityOrId = Union[str, entity.Entity]
    OneOrManyEntities = Union[entity.Entity, Sequence[entity.Entity]]

NgsiLocation = Union[tuple[int, int], Point]
"""A user type : either a tuple of two ints (lat, lon) or a GeoJson Point.
"""

NgsiGeometry = Union[NgsiLocation, LineString, Polygon]
"""A user type : Valid Geometries types for a NGSI-LD GeoProperty.
"""

NgsiDate = Union[str, datetime, date, time]
"""A user type : Valid Date types for a NGSI-LD TemporalProperty.
"""

CORE_CONTEXT = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
"""The default NGSI-LD Core Context. Automatically set at entity creation time if no context is provided.
"""

META_ATTR_CONTEXT = "@context"
META_ATTR_UNITCODE = "unitCode"
META_ATTR_OBSERVED_AT = "observedAt"
META_ATTR_DATASET_ID = "datasetId"

NESTED = True

TZ_UTC = timezone.utc
TZ_WET = ZoneInfo("WET")  # UTC+1 i.e. Europe/Lisbon
TZ_CET = ZoneInfo("CET")  # UTC+2 i.e. Europe/Paris
TZ_FET = ZoneInfo("Europe/Minsk")  # UTC+3


class Auto(Sentinel):
    pass


class Rel(Enum):
    HAS_PART = "hasPart"
    HAS_DIRECT_PART = "hasDirectPart"
    IS_CONTAINED_IN = "isContainedIn"
    OBSERVED_BY = "observedBy"
    PROVIDED_BY = "providedBy"


class GeometryMetaAttr(Enum):
    LOCATION = "location"
    OBSERVATION_SPACE = "observationSpace"
    OPERATION_SPACE = "operationSpace"


class AttrType(Enum):
    PROP = "Property"
    TEMPORAL = "Property"  # Temporal Property
    GEO = "GeoProperty"
    REL = "Relationship"


class GeometryType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"


class TemporalType(Enum):
    DATETIME = "DateTime"
    DATE = "Date"
    TIME = "Time"


SMARTDATAMODELS_BASEURL = "https://smart-data-models.github.io"  # Github Pages


class SmartDataModels:
    class SmartAgri:
        class Agrifood:
            AgriApp = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriApp/examples/example-normalized.jsonld"
            AgriCrop = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriCrop/examples/example-normalized.jsonld"
            AgriFarm = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriFarm/examples/example-normalized.jsonld"
            AgriGreenhouse = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriGreenhouse/examples/example-normalized.jsonld"
            AgriParcel = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriParcel/examples/example-normalized.jsonld"
            AgriParcelOperation = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriParcelOperation/examples/example-normalized.jsonld"
            AgriParcelRecord = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriParcelRecord/examples/example-normalized.jsonld"
            AgriPest = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriPest/examples/example-normalized.jsonld"
            AgriProductType = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriProductType/examples/example-normalized.jsonld"
            AgriSoil = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/AgriSoil/examples/example-normalized.jsonld"
            Animal = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/Animal/examples/example-normalized.jsonld"
            Compartment = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/Compartment/examples/example-normalized.jsonld"
            Pen = f"{SMARTDATAMODELS_BASEURL}/dataModel.Agrifood/Pen/examples/example-normalized.jsonld"

        class Aquaculture:
            BreedingOperation = f"{SMARTDATAMODELS_BASEURL}/dataModel.Aquaculture/BreedingOperation/examples/example-normalized.jsonld"
            FishContainment = f"{SMARTDATAMODELS_BASEURL}/dataModel.Aquaculture/FishContainment/examples/example-normalized.jsonld"

        class Weather:
            SeaConditions = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/SeaConditions/examples/example-normalized.jsonld"
            WeatherAlert = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/WeatherAlert/examples/example-normalized.jsonld"
            WeatherForecast = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/WeatherForecast/examples/example-normalized.jsonld"
            WeatherObserved = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/WeatherObserved/examples/example-normalized.jsonld"

    class SmartCities:
        class Building:
            Building = f"{SMARTDATAMODELS_BASEURL}/dataModel.Building/Building/examples/example-normalized.jsonld"
            BuildingOperation = f"{SMARTDATAMODELS_BASEURL}/dataModel.Building/BuildingOperation/examples/example-normalized.jsonld"
            VibrationsObserved = f"{SMARTDATAMODELS_BASEURL}/dataModel.Building/VibrationsObserved/examples/example-normalized.jsonld"

        class Parking:
            OffStreetParking = f"{SMARTDATAMODELS_BASEURL}/dataModel.Parking/OffStreetParking/examples/example-normalized.jsonld"
            OnStreetParking = f"{SMARTDATAMODELS_BASEURL}/dataModel.Parking/OnStreetParking/examples/example-normalized.jsonld"
            ParkingAccess = f"{SMARTDATAMODELS_BASEURL}/dataModel.Parking/ParkingAccess/examples/example-normalized.jsonld"
            ParkingGroup = f"{SMARTDATAMODELS_BASEURL}/dataModel.Parking/ParkingGroup/examples/example-normalized.jsonld"
            ParkingSpot = f"{SMARTDATAMODELS_BASEURL}/dataModel.Parking/ParkingSpot/examples/example-normalized.jsonld"

        class ParksAndGarden:
            FlowerBed = f"{SMARTDATAMODELS_BASEURL}/dataModel.ParksAndGardens/FlowerBed/examples/example-normalized.jsonld"
            Garden = f"{SMARTDATAMODELS_BASEURL}/dataModel.ParksAndGardens/Garden/examples/example-normalized.jsonld"
            GreenSpaceRecord = f"{SMARTDATAMODELS_BASEURL}/dataModel.ParksAndGardens/GreenspaceRecord/examples/example-normalized.jsonld"

        class PointOfInterest:
            Beach = f"{SMARTDATAMODELS_BASEURL}/dataModel.PointOfInterest/Beach/examples/example-normalized.jsonld"
            Museum = f"{SMARTDATAMODELS_BASEURL}/dataModel.PointOfInterest/Museum/examples/example-normalized.jsonld"
            PointOfInterest = f"{SMARTDATAMODELS_BASEURL}/dataModel.PointOfInterest/PointOfInterest/examples/example-normalized.jsonld"
            Store = f"{SMARTDATAMODELS_BASEURL}/dataModel.PointOfInterest/Store/examples/example-normalized.jsonld"

        class Ports:
            BoatAuthorized = f"{SMARTDATAMODELS_BASEURL}/dataModel.Ports/BoatAuthorized/examples/example-normalized.jsonld"
            SeaportFacilities = f"{SMARTDATAMODELS_BASEURL}/dataModel.Ports/SeaportFacilities/examples/example-normalized.jsonld"
            BoatPlacesAvailable = f"{SMARTDATAMODELS_BASEURL}/dataModel.Ports/BoatPlacesAvailable/examples/example-normalized.jsonld"

        class StreetLightning:
            StreetLight = f"{SMARTDATAMODELS_BASEURL}/dataModel.Streetlighting/Streetlight/examples/example-normalized.jsonld"
            StreetLightControlCabinet = f"{SMARTDATAMODELS_BASEURL}/dataModel.Streetlighting/StreetlightControlCabinet/examples/example-normalized.jsonld"
            StreetLightGroup = f"{SMARTDATAMODELS_BASEURL}/dataModel.Streetlighting/StreetlightGroup/examples/example-normalized.jsonld"
            StreetLightModel = f"{SMARTDATAMODELS_BASEURL}/dataModel.Streetlighting/StreetlightModel/examples/example-normalized.jsonld"

        class Transportation:
            BikeHireDockingStation = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/BikeHireDockingStation/examples/example-normalized.jsonld"
            BikeLane = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/BikeLane/examples/example-normalized.jsonld"
            CityWork = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/CityWork/examples/example-normalized.jsonld"
            CrowFlowObserved = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/CrowdFlowObserved/examples/example-normalized.jsonld"
            EVChargingStation = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/EVChargingStation/examples/example-normalized.jsonld"
            FareCollectionSystem = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/FareCollectionSystem/examples/example-normalized.jsonld"
            ItemFlowObserved = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/ItemFlowObserved/examples/example-normalized.jsonld"
            RestrictedTrafficArea = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/RestrictedTrafficArea/examples/example-normalized.jsonld"
            RestrictionException = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/RestrictionException/examples/example-normalized.jsonld"
            Road = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/Road/examples/example-normalized.jsonld"
            RoadAccident = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/RoadAccident/examples/example-normalized.jsonld"
            RoadSegment = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/RoadSegment/examples/example-normalized.jsonld"
            SpecialRestriction = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/SpecialRestriction/examples/example-normalized.jsonld"
            TrafficFlowObserved = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/TrafficFlowObserved/examples/example-normalized.jsonld"
            TransportStation = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/TransportStation/examples/example-normalized.jsonld"
            Vehicle = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/Vehicle/examples/example-normalized.jsonld"
            VehicleModel = f"{SMARTDATAMODELS_BASEURL}/dataModel.Transportation/VehicleModel/examples/example-normalized.jsonld"

        class UrbanMobility:
            ArrivalEstimation = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/ArrivalEstimation/examples/example-normalized.jsonld"
            GtfsAccessPoint = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsAccessPoint/examples/example-normalized.jsonld"
            GtfsAgency = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsAgency/examples/example-normalized.jsonld"
            GtfsCalendarDateRule = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsCalendarDateRule/examples/example-normalized.jsonld"
            GtfsCalendarRule = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsCalendarRule/examples/example-normalized.jsonld"
            GtfsFrequency = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsFrequency/examples/example-normalized.jsonld"
            GtfsRoute = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsRoute/examples/example-normalized.jsonld"
            GtfsService = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsService/examples/example-normalized.jsonld"
            GtfsShape = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsShape/examples/example-normalized.jsonld"
            GtfsStation = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsStation/examples/example-normalized.jsonld"
            GtfsStop = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsStop/examples/example-normalized.jsonld"
            GtfsStopTime = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsStopTime/examples/example-normalized.jsonld"
            GtfsTransferRule = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsTransferRule/examples/example-normalized.jsonld"
            GtfsTrip = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/GtfsTrip/examples/example-normalized.jsonld"
            PublicTransportRoute = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/PublicTransportRoute/examples/example-normalized.jsonld"
            PublicTransportStop = f"{SMARTDATAMODELS_BASEURL}/dataModel.UrbanMobility/PublicTransportStop/examples/example-normalized.jsonld"

        class WasteManagement:
            WasteContainer = f"{SMARTDATAMODELS_BASEURL}/dataModel.WasteManagement/WasteContainer/examples/example-normalized.jsonld"
            WasteContainerIsle = f"{SMARTDATAMODELS_BASEURL}/dataModel.WasteManagement/WasteContainerIsle/examples/example-normalized.jsonld"
            WasteContainerModel = f"{SMARTDATAMODELS_BASEURL}/dataModel.WasteManagement/WasteContainerModel/examples/example-normalized.jsonld"

        class Weather:
            SeaConditions = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/SeaConditions/examples/example-normalized.jsonld"
            WeatherAlert = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/WeatherAlert/examples/example-normalized.jsonld"
            WeatherForecast = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/WeatherForecast/examples/example-normalized.jsonld"
            WeatherObserved = f"{SMARTDATAMODELS_BASEURL}/dataModel.Weather/WeatherObserved/examples/example-normalized.jsonld"
