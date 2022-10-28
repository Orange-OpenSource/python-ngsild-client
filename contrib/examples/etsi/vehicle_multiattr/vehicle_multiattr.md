# Entity

A vehicle with two speed attributes, one measured by speedometer the other one by GPS.

# Origin

NGSI-LD example from the ETSI Context Information Managment (CIM) NGSI-LD API.<br>
Reference : ETSI GS CIM 009 V1.5.1 (2021-11), Annex C.2.2

# Comments

Two methods to build the `speed` multi-attribute.<br>
First one is to use `MultAttrValue`.<br>
Second one (variant) is to create a speed attribute as usual then duplicate it.