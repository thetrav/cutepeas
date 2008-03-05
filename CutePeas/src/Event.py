listenerMap = {}

def addListener(id, listener):
    if not listenerMap.has_key(id):
        listenerMap[id] = []
    listenerMap[id].append(listener)
    
def removeListener(id, listener):
    if listenerMap.has_key(id):
        listenerMap[id].remove(listener)
    
def fireEvent(id, event):
    if listenerMap.has_key(id):
        for listener in listenerMap[id]:
            listener.eventFired(id, event)
            
def getId(object):
    return object