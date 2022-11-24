# ngsildclient 0.5.1
## November 24, 2022

- Allow to specify precision in Entity.loc()
- Added type to PostalAddressBuilder
- Urlencode query in subscription payloads
- Fixed issue #7 : Batch upsert with AsyncClient fails with Unsupported Media type

# ngsildclient 0.5.0
## October 26, 2022

- Added mapping between : an item returned from the underlying dict AND an Attribute object
- Added Multi-Attribute support for Properties and Relationships
- Added access to value and metadata thanks to Python @property
- Added dot-notation access to the entity (thanks to Scalpl)
- Added support for batchop options (Issue #5)
- Alt POST queries accept also accept a Path to a query file
- Fixed wrong temporal endpoint mount when TRoE shares the same port number
- Fixed issue with naive datetimes (switched to dateutil timezones)
- Fixed contexts bug all referencing the same array
- Removed Mocking
- Removed the Auto cached-date feature
- Completly rewrote Readme and use a new parking example

# ngsildclient 0.4.2
## October 14, 2022

- Added support for alternative (POST) query endpoints (Issue #4)
    - `entityOperations/query`
    - `temporal/entityOperations/query`

# ngsildclient 0.4.0
## October 12, 2022

- Improved batch operations
    - Added auto-batch support
    - Harmonized batchop results
- Added support for entity multi-attributes properties and relationships
- Added experimental dataviz for network graphs

# ngsildclient 0.3.2
## October 4, 2022

- Fixed sphinx autosummary in documentation
- Renamed query_all() to query() in all classes

# ngsildclient 0.3.1
## October 3, 2022

- Added temporal query support

# ngsildclient 0.2.1
## September 19, 2022

- Added Cookbook
- Added ``Entity.from_json()``
- Fixed bug in ``iso8601.utcnow()``

# ngsildclient 0.2.0
## September 8, 2022

- Added Asynchronous Client
- Added support for custom authentication (Pull Request #2)
- Fixed "Count does not send the context" (Pull Request #3)

# ngsildclient 0.1.10
## June 22, 2022

- Added multiple-relationship support

# ngsildclient 0.1.9
## May 18, 2022

- Added load/save batch of entities from file to memory
- Added bulk import entities from file to broker
- Added pretty json printing

# ngsildclient 0.1.8
## April 22, 2022

- Added API documentation.
- Refactored ``query`` methods.
- Added batch ability to ``query_generator()``.
- Added pagination support to ``delete_where()``, ``drop()``, ``purge()`` and ``flush_all()``.

# ngsildclient 0.1.7
## March 23, 2022

- Subscription support.
- Added Docker image : ``orangeopensource/ngsildclient`` on Dockerhub
- Added Docker image for use with Gradient Paperspace : ``orangeopensource/ngsildclient-paperspace`` on Dockerhub

# ngsildclient 0.1.6
## March 11, 2022

- Added documentation. *Available on readthedocs*
- Added NGSI-LD datetimes UTC support
- Added ability to handle NGSI-LD properties from the entity's inner properties

# ngsildclient 0.1.5
## March 1, 2022

- Handle JSON-LD Context parameter in ``get()`` and ``query()`` methods
- Wrap API endpoint ``jsonldContexts``
- Detect version for Java-Spring based brokers
- Improved behaviour in interactive mode (console)

# ngsildclient 0.1.4
## February 7, 2022

- Added pagination support
- Added MockerNgsi to allow generate a bunch of entities (for testing purpose)
- Fixed bug : unable to update prop in a loaded entity

# ngsildclient 0.1.3
## February 2, 2022

- Added ``count()`` method
- Added wrapping for ``batch`` operations and ``types``

# ngsildclient 0.1.2
## January 31, 2022

- Added query features : query entities by a type or a query string
- Added github CI workflow
- Fixed SPDX headers

# ngsildclient 0.1.1
## January 18, 2022

- Added ``overwrite`` option to create entity
- Added well-known relationships as constants
- Added ``MultiPoint`` support
- Added the ``Building`` and ``Pipe`` NGSI-LD example from the Smart Data Models Initiative

# ngsildclient 0.1.0
## January 14, 2022

First public release.

- Allow to build NGSI-LD compliant entities : ``model`` package
- Wrap a subset of the NGSI-LD API (single entity CRUD) : ``api`` package
- Build many examples from the [Smart Data Models Initiative](https://smartdatamodels.org/) : ``tests`` folder

