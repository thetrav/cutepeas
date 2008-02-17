from Images import images



class Tool:
    def __init__(self, cursorIcon):
        self.cursorIcon = cursorIcon
    
class DeleteTool:
    def __init__(self):
        self.cursorIcon = images["Tool-Delete"]
        
    def invokeTool(self, event):
        pass

class BlockTool:
    def __init__(self, cursorIcon, blockFactory):
        self.cursorIcon = images["Tool-" + cursorIcon]
        self.blockFactory = blockFactory
    
    def invokeTool(self, event):
        pass
