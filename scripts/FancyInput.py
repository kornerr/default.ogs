
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
        print "FancyInput.__init__"
    def __del__(self):
        print "FancyInput.__del__"
    def deinit(self):
        print "FancyInput.deinit"
        self.windowInput.removeListener(self.inputListener)
        self.inputListener = None
    def init(self, window, windowInput, scene, nodeName):
        print "FancyInput.init"
        self.window = window
        self.windowInput = windowInput
        self.scene = scene
        self.nodeName = nodeName
        print "nn: ", self.nodeName
        self.inputListener = FancyInputListener()
        self.windowInput.addListener(self.inputListener)

def create():
    return FancyInput()

