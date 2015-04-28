
import pymjin2

class SampleInputListener(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
    def onWindowInput(self, e):
        print "SampleInput.onWindowInput", e.x, e.y
        return False

class SampleInput(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
        print "SampleInput.__init__"
    def __del__(self):
        print "SampleInput.__del__"
    def deinit(self):
        print "SampleInput.deinit"
        self.windowInput.removeListener(self.inputListener)
        self.inputListener = None
    def init(self, window, windowInput, scene, nodeName):
        print "SampleInput.init"
        self.window = window
        self.windowInput = windowInput
        self.scene = scene
        self.nodeName = nodeName
        print "nn: ", self.nodeName
        self.inputListener = SampleInputListener()
        self.windowInput.addListener(self.inputListener)

def create():
    return SampleInput()

