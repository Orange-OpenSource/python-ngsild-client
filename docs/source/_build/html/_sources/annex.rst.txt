Annex
=====

Realistic Examples
------------------

Some realistic entities from the Smart Data Models Initiative built with the library.

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

.. _PointOfInterest: https://github.com/smart-data-models/dataModel.PointOfInterest
