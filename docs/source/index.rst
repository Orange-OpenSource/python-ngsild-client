ngsildclient documentation
==========================

Welcome to the **ngsildclient** documentation, where you can learn about ngsildclient and explore its features.

**ngsildclient** is a Python NGSI-LD_ client implementation.

NGSI-LD has been standardized by the ETSI and is widely used in the Fiware_ ecosystem.

Goals
-----

The ngsildclient Python library has two main objectives.

1. **Build NGSI-LD compliant entities**

   | The task of writing large NGSI-LD compliant entities using JSON is tedious, error-prone and results in a significant amount of code.
   | ngsilclient provides primitives to build and manipulate NGSI-LD entities without effort, in respect with the ETSI specifications_.

2. **Wrap the NGSI-LD API**

   | As a Python NGSI-LD client it allows to interact with a broker by sending and retrieving NGSI-LD entities.
   | As of v0.1.5 it supports a subset of the API.

In practice
-----------

ngsildclient can be useful in practice to :

- **model a domain-specific system**  
   it has many benefits in the exploration phase : 

   - use the interactive mode to quickly build entities *thanks to Python REPL (console)*
   - use Jupyter notebooks to share and discuss about modeling
   - load and extend example entities from the Smart Data Model Initiatives
  

- **demonstrate feasibility**
   quickly develop a Proof Of Concept by :
   
   - populating the broker with your entities
   - query the broker to test relationships
  

- **develop a full NGSI-LD Agent**
   putting all parts together the NGSI-LD Agent :

   - collects incoming domain-specific data
   - converts data to NGSI-LD compliant entities
   - feed the NGSI-LD broker
  

- **administrate the broker**
   allow admin tasks in interactive mode :

   - purge entities
   - list contexts

  

.. toctree::
   :hidden:

   License <license>
   API Reference <_autosummary/ngsildclient>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _NGSI-LD: https://en.wikipedia.org/wiki/NGSI-LD
.. _Fiware: https://www.fiware.org
.. _specifications: https://www.etsi.org/committee/cim

