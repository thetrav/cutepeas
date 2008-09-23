
class Overlay:
    def __init__(self, cursor):
        self.elements = []
        self.mouseMotionAction = self.notInLayer
        self.cursor = cursor
    
    def addElement(self, element):
        self.elements.append(element)
        
    def removeElement(self, element):
        self.elements.remove(element)
    
    def mouseMoved(self, event):
        hit = []
        miss = []
        for element in self.elements():
            if element.isMouseOnElement(event):
                hit.append(element)
            else:
                miss.append(element)
        self.mouseMotionAction(event, hit, miss)
        
    def notInLayer(self, pixelPos, hit, miss):
        if len(hit) > 0:
            cursor.hideTool()
            for element in hit:
                element.mouseIsIn()
            self.mouseMotionAction = self.inLayer
    
    def inLayer(self, pixelPos, hit, miss):
        if len(hit) == 0:
            cursor.showTool()
            self.mouseMotionAction = self.notInLayer
        else:
            for element in hit:
                element.mouseIsIn()
        for element in miss:
            element.mouseIsOut()