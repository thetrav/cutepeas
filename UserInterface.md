# Description #

The UserInterface class is supposed to contain the widgets that the user uses to interact with the game.  This is supposed to be separate from the model of the Level (see LevelClass) itself, however currently that split is poorly implemented.

The UserInterface class has a collection of active widgets and a collection of passive widgets.  Both are rendered, but only the active widget collection receives events.

The UserInterface class also manages the Cursor class which means interacting with the tools, the buttons and the scene itself.

Currently it all works reasonably well, but I'd really love to refactor this one quite a lot so that there's a good split between the view/control in UserInterface and the model in Level.  I think there is too much model currently in UserInterface

## Active Widgets ##
  * ToolBar
    * ToolButton
  * Button

## Passive Widgets ##
  * Score
  * Timer
  * Text