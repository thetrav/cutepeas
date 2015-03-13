# Notes #

I have been considering writing a generic event handling structure.

Basically there's a module which handles notifications and listeners, here's the interface

```
EventMgr.addListener(id, listener)
EventMgr.removeListener(listener)
EventMgr.fireEvent(objectId, event)
EventMgr.getId(object) id
```

objectId will be unique to an object and event will be an object containing whatever is relevant to the event.


Example use:
```
class ButtonListener:
  def __init__(self):
    button = Button()
    button.id = EventMgr.getId()
    EventMgr.addListener(button.id, self)
```
button is then put into play, and within button's code:
```
EventMgr.fireEvent(self.id, ButtonClickedEvent(self))
```

Event manager then checks through its map of listeners for any listeners listening to the button's id, and calls eventFired(event) on them

## things worth considering ##
It's important that the event manager maintains the id's to ensure they are unique.  They don't have to be numbers, and could even be references themselves.

cleanup between levels could be a little annoying with this, as everything that listens is referenced (and therefore not garbage collected) until it is removed

This doesn't have to be used only for UI components.  Here are some non UI examples for events:
  * Physics notify Score that jump finishes
  * Pathfinding notify Pea that the world has changed