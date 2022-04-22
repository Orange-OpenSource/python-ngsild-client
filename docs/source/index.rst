ngsildclient documentation
==========================

Welcome to the **ngsildclient** documentation, where you can learn about ngsildclient and explore its features.

**ngsildclient** is a Python NGSI-LD client implementation.

| NGSI-LD_ has been standardized by the ETSI_ and is widely used in the Fiware_ ecosystem.
| **ngsildclient** is based on the NGSI-LD API ETSI Specification [ETSI_GS_CIM_009_V1.5.1]_.


Project Goals
-------------

The ngsildclient Python library has two main objectives.

1. :ref:`Build NGSI-LD compliant entities<Build Entities>`

   | The task of writing large NGSI-LD compliant entities using JSON is tedious, error-prone and results in a significant amount of code.
   | ngsilclient provides primitives to build and manipulate NGSI-LD entities without effort, in respect with the ETSI specifications_.

2. :ref:`Wrap the NGSI-LD API<Interact with the broker>`

   | As a Python NGSI-LD client it allows to interact with a broker by sending and retrieving NGSI-LD entities.
   | As of v0.1.8 it supports a subset of the API.

.. toctree::
   :hidden:

   Home Page <self>
   Use Cases <usecases>
   Install <install>
   Get Started <started>
   Build Entities <build>
   Interact with the Broker <client>
   Annex <annex>
   License <license>
   API Reference <_autosummary/ngsildclient>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. [ETSI_GS_CIM_009_V1.5.1] ETSI Group `Specification <https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.05.01_60/gs_CIM009v010501p.pdf>`_
   Context Information Management (CIM)
   NGSI-LD API
   v1.5.1
   2021-11
.. _NGSI-LD: https://en.wikipedia.org/wiki/NGSI-LD
.. _ETSI: https://www.etsi.org/
.. _Fiware: https://www.fiware.org
.. _specifications: https://www.etsi.org/committee/cim

