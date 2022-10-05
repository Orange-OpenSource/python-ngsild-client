ngsildclient documentation
==========================

Welcome to the **ngsildclient** documentation, where you can learn about ngsildclient and explore its features.

**ngsildclient** is a Python open source NGSI-LD client that :

- allows you to easily interact with a NGSI-LD broker
- provides facilities to build NGSI-LD entities

| Get started in minutes : query the broker for entities, timeseries data, subscribe to events.
| Effortlessly build complex entities and relationships that you'll be able to persist and update.

| The library provides a NGSI-LD **Client** suitable for use in interactive mode, i.e. in a Jupyter notebook.
| Alternatively you can prefer the **AsyncClient**, typically when user interactivity is not needed and seeking for performance - i.e. writing a real-time NGSI-LD agent.


Project Goals
-------------

The ngsildclient Python library has two main objectives.

1. :ref:`Build NGSI-LD compliant entities<Build Entities>`

   | The task of writing large NGSI-LD compliant entities using JSON is tedious, error-prone and results in a significant amount of code.
   | ngsilclient provides primitives to build and manipulate NGSI-LD entities without effort, in respect with the ETSI specifications_.

2. :ref:`Implement a NGSI-LD API Client <Interact with the broker>`

   | A large subset of the NGSI-LD API is covered.
   | **ngsildclient** is not seeking to wrap the entire NGSI-LD API.

Standardization
---------------

| NGSI-LD_ has been standardized by the ETSI_ and is widely used in the Fiware_ ecosystem.
| **ngsildclient** is based on the NGSI-LD API ETSI Specification [ETSI_GS_CIM_009_V1.5.1]_.

Acting as a Context Producer/Consumer **ngsildclient** is able to send/receive NGSI-LD entities to/from the Context Broker for creation and other operations.

.. toctree::
   :hidden:

   Home Page <self>
   Use Cases <usecases>
   Install <install>
   Get Started <started>
   Build Entities <build>
   Interact with the Broker <client>
   Cookbook <cookbook>
   License <license>
   API Reference <api>

.. [ETSI_GS_CIM_009_V1.5.1] ETSI Group `Specification <https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.05.01_60/gs_CIM009v010501p.pdf>`_
   Context Information Management (CIM)
   NGSI-LD API
   v1.5.1
   2021-11
.. _NGSI-LD: https://en.wikipedia.org/wiki/NGSI-LD
.. _ETSI: https://www.etsi.org/
.. _Fiware: https://www.fiware.org
.. _specifications: https://www.etsi.org/committee/cim

