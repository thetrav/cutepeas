listenerMap = {}

def addListener(id, listener):
    if not listenerMap[id]:
        listnerMap[id] = []
    listenerMap[id].append(listener)
    
def removeListener(id, listener):
    if listenerMap[id]:
        listenerMap[id].remove(listener)
    
def fireEvent(id, event):
    if listenerMap[id]:
        for listener in listenerMap[id]:
            listener.eventFired(event)
            
def getId(object):
    return object