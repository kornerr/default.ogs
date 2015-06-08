
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

class CameraControllerUIActions(object):
    def __init__(self, wnd):
        self.wnd = wnd
    def name(self):
        return "CameraController"
    def onUIActionsExecute(self, action, state):
        s = pymjin2.State()
        postfix = None
        if (action == "MoveBackward"):
            postfix = "backward"
        elif (action == "MoveDown"):
            postfix = "down"
        elif (action == "MoveForward"):
            postfix = "forward"
        elif (action == "MoveLeft"):
            postfix = "left"
        elif (action == "MoveRight"):
            postfix = "right"
        elif (action == "MoveUp"):
            postfix = "up"
        s.add("camera.move." + postfix , "1" if state else "0")
        self.wnd.setState(s)

class CameraController(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
    def __del__(self):
        pass
    def deinit(self):
        self.core.dscene.removeListener(self.componentListener)
        self.componentListener = None
        self.core.uiActions.removeListener(self.uiActions)
        self.uiActions = None
    def init(self, core, nodeName):
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
        self.uiActions = CameraControllerUIActions(self.core.wnd)
        self.core.uiActions.addListener(self.uiActions)
        # Setup camera shortcuts.
        st = self.core.pini.load("camera.shortcuts")
        self.core.uiActionsShortcuts.clear()
        self.core.uiActionsShortcuts.setState(st)
        self.core.uiActionsShortcuts.setGroupEnabled("CameraController", True)
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

