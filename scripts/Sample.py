
import pymjin2

class SampleInputListener(pymjin2.InputListener):
    def __init__(self):
        pymjin2.InputListener.__init__(self)
    def onWindowInput(self, e):
        print "Sample.onWindowInput", e.x, e.y
        return False

class Sample(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
        print "Sample.__init__"
        self.inputListener = SampleInputListener()
    def __del__(self):
        print "Sample.__del__"
        self.inputListener = None
    def deinit(self):
        print "Sample.deinit"
        self.windowInput.removeListener(self.inputListener)
    def init(self, window, windowInput, scene, nodeName):
        print "Sample.init"
        self.window = window
        self.windowInput = windowInput
        self.scene = scene
        self.nodeName = nodeName
        print "nn: ", self.nodeName
        self.windowInput.addListener(self.inputListener)

def create():
    return Sample()

