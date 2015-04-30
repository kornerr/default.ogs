
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
        #print "SampleInput.__init__"
    def __del__(self):
        #print "SampleInput.__del__"
        pass
    def deinit(self):
        #print "SampleInput.deinit"
        self.core.wndInput.removeListener(self.inputListener)
        self.inputListener = None
    def init(self, core, nodeName):
        self.core = core
        self.inputListener = SampleInputListener()
        self.core.wndInput.addListener(self.inputListener)
        self.nodeName = nodeName

def create():
    return SampleInput()

