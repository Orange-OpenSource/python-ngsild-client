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

