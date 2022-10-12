#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from __future__ import annotations

import json
import requests
import httpx
import aiofiles
import logging

from copy import deepcopy
from functools import partialmethod
from dataclasses import dataclass, field

from datetime import datetime
from typing import overload, Any, Union, List, Tuple, Optional, Callable
from rich import print_json

from .exceptions import *
from .ngsidict import NgsiDict
from ngsildclient.utils import iso8601, url, is_interactive
from ngsildclient.utils.urn import Urn

from ngsildclient.model.constants import CORE_CONTEXT, Rel, AttrType, Auto, NESTED, NgsiDate, NgsiGeometry, NgsiLocation

logger = logging.getLogger(__name__)

"""This module contains the definition of the Entity class.
"""

@dataclass
class MultiAttrValue:
    value: Any
    datasetid: str
    unitcode: str = None
    observedat: Union[str, datetime] = None
    userdata: dict = field(default_factory=dict)

def mkprop(*args, **kwargs):
    return NgsiDict().mkprop(*args, **kwargs)

def mkrel(*args, **kwargs):
    return NgsiDict().mkprop(*args, **kwargs)    

class Entity:
    """The main goal of this class is to build, manipulate and represent a NGSI-LD compliant entity.

    The preferred constructor allows to create an entity from its NGSI-LD type and identifier (and optionally context),
    If no context is provided, it defaults to the NGSI-LD Core Context.
    The identifier can be written using the "long form" : the fully qualified urn string.
    It can also be shorten :
    - omit the urn prefix (scheme+nss)
    - omit the type inside the identifier, assuming the naming convention "urn:ngsi-ld:<type>:<remainder>"

    An alternate constructor allows to create an entity by just providing its id (and optionally context).
    In this case the type is inferred from the fully qualified urn string,
    assuming the naming convention "urn:ngsi-ld:<type>:<remainder>".

    The load() classmethod allows to load a NGSI-LD entity from a file or remotely through HTTP.
    For convenience some `SmartDataModels <https://smartdatamodels.org/>`_ examples are made available.

    Once initiated, we can build a complete NGSI-LD entity by adding attributes to the NGSI-LD entity.
    An attribute can be a Property, TemporalProperty, GeoProperty or RelationShip.
    Methods prop(), tprop(), gprop() and rel() are used to respectively build a Property, TemporalProperty,
    GeoProperty, and Relationship.
    Attributes can carry metadatas, such as "observedAt".
    Attributes can carry user data.

    Nested attributes are supported.
    Methods prop(), tprop(), gprop() are chainable, allowing to build nested properties.

    Dates and Datetimes are ISO8601.
    Helper functions are provided in the module utils.iso8601.
    Often a same date (the one when the measure/event happened) is used many times in the entity.
    When building an entity, the first time a datetime is used it is cached, then can be reused using "Auto".

    Given a NGSI-LD entity, many actions are possible :
    - access/add/remove/update attributes
    - access/update/remove values
    - print the content in the normalized or simplified (aka KeyValues) flavor
    - save the entity to a file
    - send it to the NGSI-LD Context Broker for creation/update (use the ngsildclient.api package)

    A NGSI-LD entity is backed by a NgsiDict object (a custom dictionary that inherits from the native Python dict).
    So if for any reasons you're stuck with the library and cannot achieve to build a NGSI-LD entity
    that fully matches your target datamodel, it's always possible to manipulate directly the underlying dictionary.

    Raises
    ------
    NgsiMissingIdError
        The identifier is missing
    NgsiMissingTypeError
        The type is missing
    NgsiMissingContextError
        The context is missing

    See Also
    --------
    model.NgsiDict : a custom dictionary that inherits from the native dict and provides primitives to build attributes
    api.client.Client : the NGSI-LD Context Broker client to interact with a Context Broker

    Example
    -------
    >>> from datetime import datetime
    >>> from ngsildclient import *

    >>> # Create the entity
    >>> e = Entity("AirQualityObserved", "RZ:Obsv4567")

    >>> # Add a temporal property named dateObserved
    >>> # We could provide a string if preferred (rather than a datetime)
    >>> e.tprop("dateObserved", datetime(2018, 8, 7, 12))

    >>> # Add a property named NO2 with a pollutant concentration value and a metadata to indicate the unit (mg/m3)
    >>> # The accuracy property is nested
    >>> e.prop("NO2", 22, unitcode="GP", observedat=Auto).prop("accuracy", 0.95, NESTED)

    >>> # Add a relationship towards a POI NGSI-LD Entity
    >>> e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")

    >>> # Pretty-print to standard output
    >>> e.pprint()
    {
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ],
        "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "type": "AirQualityObserved",
        "dateObserved": {
            "type": "Property",
            "value": {
                "@type": "DateTime",
                "@value": "2018-08-07T12:00:00Z"
            }
        },
        "NO2": {
            "type": "Property",
            "value": 22,
            "unitCode": "GP",
            "observedAt": "2018-08-07T12:00:00Z",
            "accuracy": {
                "type": "Property",
                "value": 0.95
            }
        },
        "refPointOfInterest": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"
        }
    }

    >>> # Update a property by overriding it
    >>> e.prop("dateObserved", iso8601.utcnow())

    >>> # Update a value using the dot notation
    >>> e["NO2.accuracy.value"] = 0.96

    >>> # Remove a property
    >>> e.rm("NO2.accuracy")
    """

    @dataclass
    class Settings:
        """The default settings used to build an Entity"""

        autoprefix: bool = True
        """A boolean to enable/disable the automatic insertion of the type into the identifier.
        Default is enabled.
        """

        strict: bool = False  # for future use
        autoescape: bool = True  # for future use
        f_print: Callable = print_json if is_interactive() else print

    globalsettings: Settings = Settings()

    @overload
    def __init__(self, type: str, id: str, *, ctx: list = [CORE_CONTEXT]):
        """Create a NGSI-LD compliant entity

        One can omit the urn and namespace, "urn:ngsi-ld:" will be added automatically.
        One can omit the type inside the identifier.

        By default, the constructor assumes the identifier naming convention "urn:ngsi-ld:<type>:<remainder>" and automatically
        insert the type into the identifier.
        The default behaviour can be disabled : Entity.globalsettings.autoprefix = False.


        Parameters
        ----------
        type : str
            entity type
        id : str
            entity identifier
        ctx : list, optional
            the NGSI-LD context, by default the NGSI-LD Core Context

        Example
        -------
        >>> from ngsildclient.model.entity import Entity
        >>> e1 = Entity("AirQualityObserved", "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567") # long form
        >>> e2 = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567") # omit scheme + nss
        >>> e3 = Entity("AirQualityObserved", "RZ:Obsv4567") # omit scheme + nss + type
        >>> print(e1 == e2 == e3)
        True
        >>> e1.pprint()
        {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ],
            "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "type": "AirQualityObserved"
        }
        """
        ...

    @overload
    def __init__(self, id: str, *, ctx: list = [CORE_CONTEXT]):
        """Create a NGSI-LD compliant entity.

        Type is inferred from the fully qualified identifier.
        Works only if your identifiers follow the naming convention "urn:ngsi-ld:<type>:<remainder>"

        Parameters
        ----------
        id : str
            entity identifier (fully qualified urn)
        context : list, optional
            the NGSI-LD context, by default the NGSI-LD Core Context

        Example
        -------
        >>> from ngsildclient.model.entity import Entity
        >>> e = Entity("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
        >>> e.pprint()
        {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ],
            "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "type": "AirQualityObserved"
        }
        """
        ...

    def __init__(
        self,
        arg1: str = None,
        arg2: str = None,
        *,
        ctx: list = [CORE_CONTEXT],
        payload: dict = None,
        autoprefix: Optional[bool] = None,
    ):
        logger.debug(f"{arg1=} {arg2=}")

        if autoprefix is None:
            autoprefix = Entity.globalsettings.autoprefix

        self._lastprop: NgsiDict = None
        self._anchored: bool = False

        if payload is not None:  # create Entity from a dictionary
            if not payload.get("id", None):
                raise NgsiMissingIdError()
            if not payload.get("type", None):
                raise NgsiMissingTypeError()
            if not payload.get("@context", None):
                raise NgsiMissingContextError()
            self._payload: NgsiDict = NgsiDict(payload)
            return

        # create a new Entity using its id and type

        if arg2:
            type, id = arg1, arg2
        else:
            type, id = None, arg1

        dt = iso8601.extract(id)

        if type is None:  # try to infer type from the fully qualified identifier
            id = Urn.prefix(id)
            urn = Urn(id)
            if (type := urn.infertype()) is None:
                raise NgsiMissingTypeError(f"{urn.fqn=}")
        else:  # type is not None
            autoprefix &= not Urn.is_prefixed(id)
            if autoprefix:
                bareid = Urn.shorten(id)
                prefix = f"{type}:"
                if not bareid.startswith(prefix):
                    id = prefix + bareid
            id = Urn.prefix(id)  # set the prefix "urn:ngsi-ld:" if not already done
            urn = Urn(id)

        self._payload: NgsiDict = NgsiDict(
            {"@context": ctx, "id": urn.fqn, "type": type},
            dtcached=dt if dt else iso8601.utcnow(),
        )

    @classmethod
    def from_dict(cls, payload: dict):
        """Create a NGSI-LD entity from a dictionary.

        The input dictionary must at least contain the 'id', 'type' and '@context'.
        This method assumes that the input dictionary matches a valid NGSI-LD structure.

        Parameters
        ----------
        payload : dict
            The given dictionary.

        Returns
        -------
        Entity
            The result Entity instance
        """
        return cls(payload=payload)

    @classmethod
    def from_json(cls, content: str):
        """Create a NGSI-LD entity from JSON content.

        The JSON content must at least contain the "id", "type" and "@context".
        This method assumes that the input JSON content matches a valid NGSI-LD structure.

        Parameters
        ----------
        payload : str
            The given JSON content.

        Returns
        -------
        Entity
            The result Entity instance
        """
        payload: dict = json.loads(content)
        return cls(payload=payload)

    @classmethod
    def duplicate(cls, entity: Entity) -> Entity:
        """Duplicate a given entity.

        Parameters
        ----------
        entity : Entity
            The input Entity

        Returns
        -------
        Entity
            The output entity
        """
        new = deepcopy(entity)
        return new

    def copy(self) -> Entity:
        """Duplicates the entity

        Returns
        -------
        Entity
            The new entity
        """
        return Entity.duplicate(self)

    @property
    def id(self):
        return self._payload["id"]

    @id.setter
    def id(self, eid: str):
        self._payload["id"] = eid

    @property
    def type(self):
        return self._payload["type"]

    @type.setter
    def type(self, etype: str):
        self._payload["type"] = etype

    @property
    def context(self):
        return self._payload["@context"]

    @context.setter
    def context(self, ctx: list):
        self._payload["@context"] = ctx

    @property
    def relationships(self) -> List[Tuple[str, str]]:
        r: List[Tuple[str, str]] = []
        for k, v in self._payload.items():
            if isinstance(v, dict) and v.get("type") == "Relationship":
                r.append((k, v.get("object")))
            elif isinstance(v, List):
                for x in v:
                    if isinstance(x, dict) and x.get("type") == "Relationship":
                        r.append((k, x.get("object")))
        return r

    def __getitem__(self, item):
        return self._payload.__getitem__(item)

    def __setitem__(self, key, item):
        self._payload.__setitem__(key, item)

    def __delitem__(self, key):
        self._payload.__delitem__(key)
        return self

    def anchor(self):
        """Set an anchor.

        Allow to specify that the last property is used as an anchor.
        Once the anchor property is specified, new properties are attached to the anchor property.

        Parameters
        ----------
        entity : Entity
            The input Entity

        Returns
        -------
        Entity
            The output entity

        Example
        -------
        Here an anchor is set at the "availableSpotNumber" property.
        Hence the "reliability" and "providedBy" properties are attached to (nested in) the "availableSpotNumber" property.
        Without anchoring, the "reliability" and "providedBy" properties would apply to the entity's root.

        >>> from ngsildclient.model.entity import Entity
        >>> e = Entity("OffStreetParking", "Downtown1")
        >>> e.prop("availableSpotNumber", 121, observedat=datetime(2017, 7, 29, 12, 5, 2)).anchor()
        >>> e.prop("reliability", 0.7).rel("providedBy", "Camera:C1").unanchor()
        >>> e.pprint()
        {
            "@context": [
                "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "http://example.org/ngsi-ld/parking.jsonld"
            ],
            "id": "urn:ngsi-ld:OffStreetParking:Downtown1",
            "type": "OffStreetParking",
            "availableSpotNumber": {
                "type": "Property",
                "value": 121,
                "observedAt": "2017-07-29T12:05:02Z",
                "reliability": {
                    "type": "Property",
                    "value": 0.7
                },
                "providedBy": {
                    "type": "Relationship",
                    "object": "urn:ngsi-ld:Camera:C1"
                }
            }
        }
        """
        self._anchored = True
        return self

    def unanchor(self):
        """Remove the anchor.

        See Also
        --------
        Entity.anchor()
        """

        self._anchored = False
        return self

    def _update_entity(self, attrname: str, property: NgsiDict, nested: bool = False):
        nested |= self._anchored
        if nested and self._lastprop is not None:
            # update _lastprop only if not anchored
            self._lastprop[attrname] = property
            if not self._anchored:
                self._lastprop = property
        else:
            self._lastprop = self._payload[attrname] = property

    def prop(
        self,
        name: str,
        value: Any,
        nested: bool = False,
        *,  # keyword-only arguments after this
        unitcode: str = None,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
        userdata: NgsiDict = NgsiDict(),
        escape: bool = False,
    ) -> Entity:
        """Build a Property.

        Build a property and attach it to the current entity.
        One can chain prop(),tprop(), gprop(), rel() methods to build nested properties.

        Parameters
        ----------
        name : str
            the property name
        value : Any
            the property value
        observedat : Union[str, datetime], optional
            observetAt metadata, timestamp, ISO8601, UTC, by default Noneself._update_entity(name, property, nested)
        userdata : NgsiDict, optional
            a dict or NgsiDict containing user data, i.e. userdata={"reliability": 0.95}, by default NgsiDict()
        escape : bool, optional
            if set escape the string value (useful if contains forbidden characters), by default False

        Returns
        -------
        Entity
            The updated entity

        Example
        -------
        >>> from ngsildclient.model.entity import Entity
        >>> e = Entity("AirQualityObserved", "RZ:Obsv4567")
        >>> e.prop("NO2", 22, unitcode="GP") # basic property
        {'type': 'Property', 'value': 22, 'unitCode': 'GP'}
        >>> e.prop("PM10", 18, unitcode="GP").prop("reliability", 0.95) # chain methods to obtain a nested property
        {'type': 'Property', 'value': 0.95}
        >>> e.pprint()
        {
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ],
        "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "type": "AirQualityObserved",
        "NO2": {
            "type": "Property",
            "value": 22,
            "unitCode": "GP"
        },
        "PM10": {
            "type": "Property",
            "value": 18,
            "unitCode": "GP",
            "reliability": {
                "type": "Property",
                "value": 0.95
            }
        }
        """
        property = self._payload._build_property(value, unitcode, observedat, datasetid, userdata, escape)
        self._update_entity(name, property, nested)
        return self

    def addr(self, value: str):
        return self.prop("address", value)

    def gprop(
        self,
        name: str,
        value: NgsiGeometry,
        nested: bool = False,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
    ) -> Entity:
        """Build a GeoProperty.

        Build a GeoProperty and attach it to the current entity.
        One can chain prop(),tprop(), gprop(), rel() methods to build nested properties.

        Parameters
        ----------
        name : str
            the property name
        value : NgsiGeometry
            the property value

        Returns
        -------
        Entity datasetid
            The updated entity

        Example
        -------
        >>> from ngsildclient.model.entity import Entity
        >>> e = Entity("PointOfInterest", "RZ:MainSquare")
        >>> e.prop("description", "Beach of RZ")
        >>> e.gprop("location", (44, -8))
        >>> e.pprint()
        {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ],
            "id": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare",
            "type": "PointOfInterest",
            "description": {
                "type": "Property",
                "value": "Beach of RZ"
            },
            "location": {datasetid
                "type": "GeoProperty",
                "value": {
                "type": "Point",
                "coordinates": [
                    -8,datasetid
            }
        }
        """
        property = self._payload._build_geoproperty(value, observedat, datasetid)
        self._update_entity(name, property, nested)
        return self

    loc = partialmethod(gprop, "location")
    """ A helper method to set the frequently used "location" geoproperty.

    entity.loc((44, -8)) is a shorcut for entity.gprop("location", (44, -8))
    """

    def tprop(self, name: str, value: NgsiDate = None, nested: bool = False) -> Entity:
        """Build a TemporalProperty.

        Build a TemporalProperty and attach it to the current entity.
        One can chain prop(),tprop(), gprop(), rel() methoddatasetids to build nested properties.

        Parameters
        ----------
        name : str
            the property name
        value : NgsiDate
            the property value, utcnow() if None

        Returns
        -------
        Entity
            The updated entity

        Example
        -------
        >>> from datetime import datetime
        >>> from ngsildclient.model.entity import Entity
        >>> e = Entity("AirQualityObserved", "RZ:Obsv4567")
        >>> e.tprop("dateObserved", datetime(2018, 8, 7, 12))
        >>> e.pprint()
        {
            "@context": [datasetid
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ],
            "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "type": "AirQualityObserved",
            "dateObserved": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": "2018-08-07T12:00:00Z"
                }
            }
        }
        """
        if value is None:
            value = self._payload._dtcached
        property = self._payload._build_temporal_property(value)
        self._update_entity(name, property, nested)
        return self

    obs = partialmethod(tprop, "dateObserved")
    """ A helper method to set the frequently used "dateObserved" property.

    entity.obs("2022-01-12T12:54:38Z") is a shorcut for entity.tprop("dateObserved", "2022-01-12T12:54:38Z")
    """

    def rel(
        self,
        name: Union[Rel, str],
        value: Union[str, List[str], Entity, List[Entity]],
        nested: bool = False,
        *,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
        userdata: NgsiDict = NgsiDict(),
    ) -> Entity:
        """Build a Relationship Property.

        Build a Relationship Property and attach it to the current entity.
        One can chain prop(),tprop(), gprop(), rel() methods to build nested properties.

        Parameters
        ----------
        name : str
            the property name
        value : str
            the property value

        Returns
        -------
        Entity
            The updated entity

        Example
        -------
        >>> from ngsildclient.model.entity import Entity
        >>> e = Entity("AirQualityObserved", "RZ:Obsv4567")
        >>> e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
        >>> e.pprint()
        {
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ],
            "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "type": "AirQualityObserved",
            "refPointOfInterest": {
                "type": "Relationship",
                "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"
            }
        }
        """
        if isinstance(name, Rel):
            name = name.value
        property = self._payload._build_relationship(value, observedat, datasetid, userdata)
        self._update_entity(name, property, nested)
        return self

    def __eq__(self, other: Entity):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self._payload == other._payload

    def __repr__(self):
        return self._payload.__repr__()

    def to_dict(self, kv=False) -> NgsiDict:
        """Returns the entity as a dictionary.

        The returned type is NgsiDict, fully compatible with a native dict.

        Parameters
        ----------
        kv : bool, optional
            KeyValues format (aka simplified representation), by default False

        Returns
        -------
        NgsiDict
            The underlying native Python dictionary
        """
        return self._to_keyvalues() if kv else self._payload

    def _to_keyvalues(self) -> NgsiDict:
        """Compute a NgsiDict that contains only the highest-level of information.

        Returns
        -------
        NgsiDict
            The simplified representation
        """
        d = NgsiDict()
        for k, v in self._payload.items():
            if isinstance(v, dict):
                if v["type"] == AttrType.PROP.value:  # apply to Property and TemporalProperty
                    value = v["value"]
                    if isinstance(value, dict):
                        value = value.get("@value", value)  # for Temporal Property only
                    d[k] = value
                elif v["type"] == AttrType.GEO.value:
                    d[k] = v["value"]
                elif v["type"] == AttrType.REL.value:
                    d[k] = v["object"]
            else:
                d[k] = v
        return d

    def to_json(self, kv=False, *args, **kwargs) -> str:
        """Returns the entity as JSON.

        Parameters
        ----------
        kv : bool, optional
            KeyValues format (aka simplified representation), by default False

        Returns
        -------
        str
            The JSON content
        """
        payload: NgsiDict = self.to_dict(kv)
        return payload.to_json(*args, **kwargs)

    def pprint(self, kv=False, *args, **kwargs):
        """Pretty-print the entity to the standard ouput.

        Parameters
        ----------
        kv : bool, optional
            KeyValues format (aka simplified representation), by default False
        """
        Entity.globalsettings.f_print(self.to_json(kv, indent=2, *args, **kwargs))

    @classmethod
    def load(cls, filename: str):
        """Load an Entity from a JSON file, locally from the filesystem or remotely through HTTP.

        For convenience some `SmartDataModels <https://smartdatamodels.org/>`_ examples are made available thanks to the Smart Data Models initiative.
        You can benefit from autocompletion to navigate inside the available datamodels.

        Parameters
        ----------
        filename : str
            If filename corresponds to an URL, the JSON file is downloaded from HTTP.
            Else it is retrieved locally from the filesystem.

        Returns
        -------
        Entity
            The Entity instance

        See Also
        --------
        model.constants.SmartDataModels

        Example
        -------
        >>> from ngsildclient import *
        >>> e = Entity.load(SmartDataModels.SmartCities.Weather.WeatherObserved)
        """
        if url.isurl(filename):
            resp = requests.get(filename)
            payload = resp.json()
        else:
            with open(filename, "r") as fp:
                payload = json.load(fp)
        if isinstance(payload, List):
            return [cls.from_dict(x) for x in payload]
        return cls.from_dict(payload)

    @classmethod
    async def load_async(cls, filename: str):
        """Load an Entity from a JSON file, locally from the filesystem or remotely through HTTP.

        For convenience some `SmartDataModels <https://smartdatamodels.org/>`_ examples are made available thanks to the Smart Data Models initiative.
        You can benefit from autocompletion to navigate inside the available datamodels.

        Parameters
        ----------
        filename : str
            If filename corresponds to an URL, the JSON file is downloaded from HTTP.
            Else it is retrieved locally from the filesystem.

        Returns
        -------
        Entity
            The Entity instance

        See Also
        --------
        model.constants.SmartDataModels

        Example
        -------
        >>> from ngsildclient import *
        >>> e = await Entity.load_async(SmartDataModels.SmartCities.Weather.WeatherObserved)
        """
        if url.isurl(filename):
            resp = httpx.get(filename)
            payload = resp.json()
        else:
            async with aiofiles.open(filename, "r") as fp:
                contents = await fp.read()
                payload = json.loads(contents)
        if isinstance(payload, List):
            return [cls.from_dict(x) for x in payload]
        return cls.from_dict(payload)

    @classmethod
    def load_batch(cls, filename: str):
        """Load a batch of entities from a JSON file.

        Parameters
        ----------
        filename : str
            The input file must contain a JSON array

        Returns
        -------
        List[Entity]
            A list of entities

        Example
        -------
        >>> from ngsildclient import *
        >>> rooms = Entity.load_batch("/tmp/rooms_all.jsonld")
        """
        with open(filename, "r") as fp:
            payload = json.load(fp)
        if not isinstance(payload, List):
            raise ValueError("The JSON payload MUST be an array")
        return [cls.from_dict(x) for x in payload]

    @classmethod
    async def load_batch_async(cls, filename: str):
        """Load a batch of entities from a JSON file.

        Parameters
        ----------
        filename : str
            The input file must contain a JSON array

        Returns
        -------
        List[Entity]
            A list of entities

        Example
        -------
        >>> from ngsildclient import *
        >>> rooms = await Entity.load_batch_async("/tmp/rooms_all.jsonld")
        """
        async with aiofiles.open(filename, "r") as fp:
            contents = await fp.read()
            payload = json.loads(contents)
        if not isinstance(payload, List):
            raise ValueError("The JSON payload MUST be an array")
        return [cls.from_dict(x) for x in payload]

    def save(self, filename: str, *, indent: int = 2):
        """Save the entity to a file.

        Parameters
        ----------
        filename : str
            Name of the output file
        indent : int, optional
            identation size (number of spaces), by default 2
        """
        with open(filename, "w") as fp:
            json.dump(self._payload, fp, default=str, ensure_ascii=False, indent=indent)

    async def save_async(self, filename: str, *, indent: int = 2):
        """Save the entity to a file.

        Parameters
        ----------
        filename : str
            Name of the output file
        indent : int, optional
            identation size (number of spaces), by default 2
        """
        async with aiofiles.open(filename, "w") as fp:
            payload = json.dumps(self._payload, default=str, ensure_ascii=False, indent=indent)
            await fp.write(payload)

    @classmethod
    def save_batch(cls, entities: List[Entity], filename: str, *, indent: int = 2):
        """Save a batch of entities to a JSON file.

        Parameters
        ----------
        entities: List[Entity]
            Batch of entities to be saved

        filename : str
            If filename corresponds to an URL, the JSON file is downloaded from HTTP.
            Else it is retrieved locally from the filesystem.

        Example
        -------
        >>> from ngsildclient import *
        >>> rooms = [Entity("Room", "Room1"), Entity("Room", "Room2")]
        >>> Entity.save_batch(rooms, "/tmp/rooms_all.jsonld")
        """
        payload = [x._payload for x in entities]
        with open(filename, "w") as fp:
            json.dump(payload, fp, default=str, ensure_ascii=False, indent=indent)

    @classmethod
    async def save_batch_async(cls, entities: List[Entity], filename: str, *, indent: int = 2):
        """Save a batch of entities to a JSON file.

        Parameters
        ----------
        entities: List[Entity]
            Batch of entities to be saved

        filename : str
            If filename corresponds to an URL, the JSON file is downloaded from HTTP.
            Else it is retrieved locally from the filesystem.

        Example
        -------
        >>> from ngsildclient import *
        >>> rooms = [Entity("Room", "Room1"), Entity("Room", "Room2")]
        >>> await Entity.save_batch_async(rooms, "/tmp/rooms_all.jsonld")
        """
        payload = [x._payload for x in entities]
        async with aiofiles.open(filename, "w") as fp:
            payload = json.dumps(payload, default=str, ensure_ascii=False, indent=indent)
            await fp.write(payload)
