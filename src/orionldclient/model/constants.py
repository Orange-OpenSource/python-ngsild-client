#!/usr/bin/env python3

# Software Name: python-orion-client
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battelo@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

from enum import Enum

CORE_CONTEXT = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"

META_ATTR_CONTEXT = "@context"
META_ATTR_UNITCODE = "unitCode"
META_ATTR_OBSERVED_AT = "observedAt"
META_ATTR_DATASET_ID = "datasetId"


class PredefinedRelationship(Enum):
    HAS_PART = "hasPart"
    HAS_DIRECT_PART = "hasDirectPart"
    IS_CONTAINED_IN = "isContainedIn"


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


class SmartDatamodels:
    class SmartAgrifood:
        class Agrifood:
            AgriApp = "https://smart-data-models.github.io/dataModel.Agrifood/AgriApp/examples/example-normalized.jsonld"
            AgriCrop = "https://smart-data-models.github.io/dataModel.Agrifood/AgriCrop/examples/example-normalized.jsonld"
            AgriFarm = "https://smart-data-models.github.io/dataModel.Agrifood/AgriFarm/examples/example-normalized.jsonld"
            AgriGreenhouse = "https://smart-data-models.github.io/dataModel.Agrifood/AgriGreenhouse/examples/example-normalized.jsonld"
            AgriParcel = "https://smart-data-models.github.io/dataModel.Agrifood/AgriParcel/examples/example-normalized.jsonld"
            AgriParcelOperation = "https://smart-data-models.github.io/dataModel.Agrifood/AgriParcelOperation/examples/example-normalized.jsonld"
            AgriParcelRecord = "https://smart-data-models.github.io/dataModel.Agrifood/AgriParcelRecord/examples/example-normalized.jsonld"
            AgriPest = "https://smart-data-models.github.io/dataModel.Agrifood/AgriPest/examples/example-normalized.jsonld"
            AgriProductType = "https://smart-data-models.github.io/dataModel.Agrifood/AgriProductType/examples/example-normalized.jsonld"
            AgriSoil = "https://smart-data-models.github.io/dataModel.Agrifood/AgriSoil/examples/example-normalized.jsonld"
            Animal = "https://smart-data-models.github.io/dataModel.Agrifood/Animal/examples/example-normalized.jsonld"
            Compartment = "https://smart-data-models.github.io/dataModel.Agrifood/Compartment/examples/example-normalized.jsonld"
            Pen = "https://smart-data-models.github.io/dataModel.Agrifood/Pen/examples/example-normalized.jsonld"

        class Aquaculture:
            BreedingOperation = "https://smart-data-models.github.io/dataModel.Aquaculture/BreedingOperation/examples/example-normalized.jsonld"
            FishContainment = "https://smart-data-models.github.io/dataModel.Aquaculture/FishContainment/examples/example-normalized.jsonld"

        class Weather:
            SeaConditions = "https://smart-data-models.github.io/dataModel.Weather/SeaConditions/examples/example-normalized.jsonld"
            WeatherAlert = "https://smart-data-models.github.io/dataModel.Weather/WeatherAlert/examples/example-normalized.jsonld"
            WeatherForecast = "https://smart-data-models.github.io/dataModel.Weather/WeatherForecast/examples/example-normalized.jsonld"
            WeatherObserved = "https://smart-data-models.github.io/dataModel.Weather/WeatherObserved/examples/example-normalized.jsonld"

    class SmartCities:
        class Building:
            Building = "https://smart-data-models.github.io/dataModel.Building/Building/examples/example-normalized.jsonld"
            BuildingOperation = "https://smart-data-models.github.io/dataModel.Building/BuildingOperation/examples/example-normalized.jsonld"
            VibrationsObserved = "https://smart-data-models.github.io/dataModel.Building/VibrationsObserved/examples/example-normalized.jsonld"

        class Parking:
            OffStreetParking = "https://smart-data-models.github.io/dataModel.Parking/OffStreetParking/examples/example-normalized.jsonld"
            OnStreetParking = "https://smart-data-models.github.io/dataModel.Parking/OnStreetParking/examples/example-normalized.jsonld"
            ParkingAccess = "https://smart-data-models.github.io/dataModel.Parking/ParkingAccess/examples/example-normalized.jsonld"
            ParkingGroup = "https://smart-data-models.github.io/dataModel.Parking/ParkingGroup/examples/example-normalized.jsonld"
            ParkingSpot = "https://smart-data-models.github.io/dataModel.Parking/ParkingSpot/examples/example-normalized.jsonld"

        class ParksAndGarden:
            FlowerBed = "https://smart-data-models.github.io/dataModel.ParksAndGardens/FlowerBed/examples/example-normalized.jsonld"
            Garden = "https://smart-data-models.github.io/dataModel.ParksAndGardens/Garden/examples/example-normalized.jsonld"
            GreenSpaceRecord = "https://smart-data-models.github.io/dataModel.ParksAndGardens/GreenspaceRecord/examples/example-normalized.jsonld"

        class PointOfInterest:
            Beach = "https://smart-data-models.github.io/dataModel.PointOfInterest/Beach/examples/example-normalized.jsonld"
            Museum = "https://smart-data-models.github.io/dataModel.PointOfInterest/Museum/examples/example-normalized.jsonld"
            PointOfInterest = "https://smart-data-models.github.io/dataModel.PointOfInterest/PointOfInterest/examples/example-normalized.jsonld"
            Store = "https://smart-data-models.github.io/dataModel.PointOfInterest/Store/examples/example-normalized.jsonld"

        class Ports:
            BoatAuthorized = "https://smart-data-models.github.io/dataModel.Ports/BoatAuthorized/examples/example-normalized.jsonld"
            SeaportFacilities = "https://smart-data-models.github.io/dataModel.Ports/SeaportFacilities/examples/example-normalized.jsonld"
            BoatPlacesAvailable = "https://smart-data-models.github.io/dataModel.Ports/BoatPlacesAvailable/examples/example-normalized.jsonld"

        class StreetLightning:
            StreetLight = "https://smart-data-models.github.io/dataModel.Streetlighting/Streetlight/examples/example-normalized.jsonld"
            StreetLightControlCabinet = "https://smart-data-models.github.io/dataModel.Streetlighting/StreetlightControlCabinet/examples/example-normalized.jsonld"
            StreetLightGroup = "https://smart-data-models.github.io/dataModel.Streetlighting/StreetlightGroup/examples/example-normalized.jsonld"
            StreetLightModel = "https://smart-data-models.github.io/dataModel.Streetlighting/StreetlightModel/examples/example-normalized.jsonld"

        class Transportation:
            BikeHireDockingStation = "https://smart-data-models.github.io/dataModel.Transportation/BikeHireDockingStation/examples/example-normalized.jsonld"
            BikeLane = "https://smart-data-models.github.io/dataModel.Transportation/BikeLane/examples/example-normalized.jsonld"
            CityWork = "https://smart-data-models.github.io/dataModel.Transportation/CityWork/examples/example-normalized.jsonld"
            CrowFlowObserved = "https://smart-data-models.github.io/dataModel.Transportation/CrowdFlowObserved/examples/example-normalized.jsonld"
            EVChargingStation = "https://smart-data-models.github.io/dataModel.Transportation/EVChargingStation/examples/example-normalized.jsonld"
            FareCollectionSystem = "https://smart-data-models.github.io/dataModel.Transportation/FareCollectionSystem/examples/example-normalized.jsonld"
            ItemFlowObserved = "https://smart-data-models.github.io/dataModel.Transportation/ItemFlowObserved/examples/example-normalized.jsonld"
            RestrictedTrafficArea = "https://smart-data-models.github.io/dataModel.Transportation/RestrictedTrafficArea/examples/example-normalized.jsonld"
            RestrictionException = "https://smart-data-models.github.io/dataModel.Transportation/RestrictionException/examples/example-normalized.jsonld"
            Road = "https://smart-data-models.github.io/dataModel.Transportation/Road/examples/example-normalized.jsonld"
            RoadAccident = "https://smart-data-models.github.io/dataModel.Transportation/RoadAccident/examples/example-normalized.jsonld"
            RoadSegment = "https://smart-data-models.github.io/dataModel.Transportation/RoadSegment/examples/example-normalized.jsonld"
            SpecialRestriction = "https://smart-data-models.github.io/dataModel.Transportation/SpecialRestriction/examples/example-normalized.jsonld"
            TrafficFlowObserved = "https://smart-data-models.github.io/dataModel.Transportation/TrafficFlowObserved/examples/example-normalized.jsonld"
            TransportStation = "https://smart-data-models.github.io/dataModel.Transportation/TransportStation/examples/example-normalized.jsonld"
            Vehicle = "https://smart-data-models.github.io/dataModel.Transportation/Vehicle/examples/example-normalized.jsonld"
            VehicleModel = "https://smart-data-models.github.io/dataModel.Transportation/VehicleModel/examples/example-normalized.jsonld"

        class UrbanMobility:
            ArrivalEstimation = "https://smart-data-models.github.io/dataModel.UrbanMobility/ArrivalEstimation/examples/example-normalized.jsonld"
            GtfsAccessPoint = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsAccessPoint/examples/example-normalized.jsonld"
            GtfsAgency = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsAgency/examples/example-normalized.jsonld"
            GtfsCalendarDateRule = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsCalendarDateRule/examples/example-normalized.jsonld"
            GtfsCalendarRule = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsCalendarRule/examples/example-normalized.jsonld"
            GtfsFrequency = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsFrequency/examples/example-normalized.jsonld"
            GtfsRoute = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsRoute/examples/example-normalized.jsonld"
            GtfsService = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsService/examples/example-normalized.jsonld"
            GtfsShape = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsShape/examples/example-normalized.jsonld"
            GtfsStation = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsStation/examples/example-normalized.jsonld"
            GtfsStop = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsStop/examples/example-normalized.jsonld"
            GtfsStopTime = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsStopTime/examples/example-normalized.jsonld"
            GtfsTransferRule = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsTransferRule/examples/example-normalized.jsonld"
            GtfsTrip = "https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsTrip/examples/example-normalized.jsonld"
            PublicTransportRoute = "https://smart-data-models.github.io/dataModel.UrbanMobility/PublicTransportRoute/examples/example-normalized.jsonld"
            PublicTransportStop = "https://smart-data-models.github.io/dataModel.UrbanMobility/PublicTransportStop/examples/example-normalized.jsonld"

        class WasteManagement:
            WasteContainer = "https://smart-data-models.github.io/dataModel.WasteManagement/WasteContainer/examples/example-normalized.jsonld"
            WasteContainerIsle = "https://smart-data-models.github.io/dataModel.WasteManagement/WasteContainerIsle/examples/example-normalized.jsonld"
            WasteContainerModel = "https://smart-data-models.github.io/dataModel.WasteManagement/WasteContainerModel/examples/example-normalized.jsonld"

        class Weather:
            SeaConditions = "https://smart-data-models.github.io/dataModel.Weather/SeaConditions/examples/example-normalized.jsonld"
            WeatherAlert = "https://smart-data-models.github.io/dataModel.Weather/WeatherAlert/examples/example-normalized.jsonld"
            WeatherForecast = "https://smart-data-models.github.io/dataModel.Weather/WeatherForecast/examples/example-normalized.jsonld"
            WeatherObserved = "https://smart-data-models.github.io/dataModel.Weather/WeatherObserved/examples/example-normalized.jsonld"
