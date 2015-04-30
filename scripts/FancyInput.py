
import pymjin2

class FancyInputListener(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
    def onWindowInput(self, e):
        print "FancyInput.onWindowInput", e.x, e.y, e.x + e.y
        return False

class FancyInput(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
        self.core = None
        #print "FancyInput.__init__"
    def __del__(self):
        #print "FancyInput.__del__"
        pass
    def deinit(self):
        #print "FancyInput.deinit"
        self.core.wndInput.removeListener(self.inputListener)
        self.inputListener = None
    def init(self, core, nodeName):
        #print "FancyInput.init"
        self.core = core
        self.nodeName = nodeName
        self.inputListener = FancyInputListener()
        self.core.wndInput.addListener(self.inputListener)

def create():
    return FancyInput()

