Five practical use cases
========================

ngsildclient can be useful in practice to :

- **model a domain-specific system**  
   it has many benefits in the exploration phase : 

   - use the interactive mode to quickly build entities *thanks to Python REPL (console)*
   - use Jupyter notebooks to share and discuss about modeling or for didactic purpose
   - load and extend example entities from the Smart Data Model Initiatives
  

- **demonstrate feasibility**
   quickly develop a Proof Of Concept by :
   
   - populating the broker with sample entities
   - query the broker to test relationships
  

- **develop a full NGSI-LD Agent**
   putting all parts together the NGSI-LD Agent :

   - collects incoming domain-specific data
   - converts data to NGSI-LD compliant entities
   - feed the NGSI-LD broker

- **create a digital twin simulation**
   by mocking hundreds of NGSI-LD entities :

   - representative of the real world
   - using Python to drive their behaviour
  
- **administrate the broker**
   allow admin tasks in interactive mode :

   - purge entities
   - list contexts