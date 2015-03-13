# Xml Format #

example:
```
<Level name="Example Level" width="9" height="9">

<Tool id="DeleteTool"/>
<Tool id="StandardBlock"/>
<Tool id="GelBlock"/>

<Block type="Standard" xIndex="4" yIndex="2"/>
<Block type="Standard" xIndex="4" yIndex="1"/>
<Block type="Standard" xIndex="4" yIndex="0"/>
<Block type="Spring" xIndex="5" yIndex="0"/>

<Pea left="300" top="600"/>
<Pea left="200" top="600"/>

</Level>
```

I like the idea of declaring tools, so we can restrict/add new tools per level, however I'd also say we should ignore these elements for release 0.1

Note also that there is no mention of nodes or surfaces in the file format.

This lends itself to the following load process:
  1. Create level with width x height slots
  1. Create tool widgets
  1. Add blocks as per standard mechanism, either without ghost, or listen for ghost finishing
  1. Add peas at given locations, put them in the PhysicsSimulation performing an unscored jump.