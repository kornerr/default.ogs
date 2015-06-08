
import pymjin2

class CameraControllerComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
    def onComponentStateChange(self, st):
        #print "CameraController.onComponentStateChange"
        for key in st.keys:
            value = st.value(key)[0]
            if (key == self.parent.keyPos):
                self.parent.syncPosRot(value)
            elif (key == self.parent.keyRot):
                self.parent.syncPosRot(None, value)

class CameraControllerInputListener(pymjin2.InputListener):
    def __init__(self, parent):
        pymjin2.InputListener.__init__(self)
        self.parent = parent
    def onWindowInput(self, e):
        # Fix unmodifiedInput being almost always 0 for Qt key presses.
        if (not e.unmodifiedInput):
            e.unmodifiedInput = e.input
        print "CameraControllerInput", e.unmodifiedInput
        return False

class CameraController(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
    def __del__(self):
        pass
    def deinit(self):
        #print "CameraController.deinit"
        self.core.dscene.removeListener(self.componentListener)
        self.componentListener = None
        self.core.wndInput.removeListener(self.inputListener)
        self.inputListener = None
    def init(self, core, nodeName):
        #print "CameraController.init"
        self.core = core
        self.nodeName = nodeName
        self.keyPos = "node.{0}.position".format(nodeName)
        self.keyRot = "node.{0}.rotationq".format(nodeName)
        self.componentListener = CameraControllerComponentListener(self)
        self.core.dscene.addListener([self.keyPos,
                                      self.keyRot],
                                      self.componentListener)
        # Sync right after assignment.
        self.syncPosRot()
        self.inputListener = CameraControllerInputListener(self)
        self.core.wndInput.addListener(self.inputListener)
    def syncPosRot(self, posValue = None, rotValue = None):
        # Position.
        newPosValue = posValue
        if (newPosValue is None):
            st = self.core.dscene.state([self.keyPos])
            newPosValue = st.value(self.keyPos)[0]
        # Rotation.
        newRotValue = rotValue
        if (newRotValue is None):
            st = self.core.dscene.state([self.keyRot])
            newRotValue = st.value(self.keyRot)[0]
        # Application.
        st = pymjin2.State()
        st.add("camera.position",  newPosValue)
        st.add("camera.rotationq", newRotValue)
        self.core.wnd.setState(st)

def create():
    return CameraController()

