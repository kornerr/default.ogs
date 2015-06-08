
import pymjin2

class CameraControllerComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
    def onComponentStateChange(self, st):
        print "CameraController.onComponentStateChange"
        for key in st.keys:
            print "key", key
            value = st.value(key)[0]
            if (key == self.parent.keyPos):
                if (not self.parent.ignoreCameraUpdates):
                    self.parent.syncCameraWithNode(value)
                else:
                    print "ignoreCameraUpdates"
            elif (key == self.parent.keyRot):
                if (not self.parent.ignoreCameraUpdates):
                    self.parent.syncCameraWithNode(None, value)
                else:
                    print "ignoreCameraUpdates"
            elif (key == "camera.position"):
                if (not self.parent.ignoreNodeUpdates):
                    self.parent.syncNodeWithCamera(value)
                else:
                    print "ignoreNodeUpdates"

class CameraControllerUIActions(object):
    def __init__(self, wnd):
        self.wnd = wnd
    def name(self):
        return "CameraController"
    def onUIActionsExecute(self, action, state):
        s = pymjin2.State()
        postfix = None
        if (action == "MoveBackward"):
            postfix = "Backward"
        elif (action == "MoveDown"):
            postfix = "Down"
        elif (action == "MoveForward"):
            postfix = "Forward"
        elif (action == "MoveLeft"):
            postfix = "Left"
        elif (action == "MoveRight"):
            postfix = "Right"
        elif (action == "MoveUp"):
            postfix = "Up"
        s.add("camera.move" + postfix , "1" if state else "0")
        self.wnd.setState(s)

class CameraController(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
        self.ignoreCameraUpdates = False
        self.ignoreNodeUpdates = False
    def __del__(self):
        pass
    def deinit(self):
        self.core.dscene.removeListener(self.componentListener)
        self.core.wnd.removeListener(self.componentListener)
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
        self.core.wnd.addListener(["camera.position"], self.componentListener)
        # Sync right after assignment.
        self.syncCameraWithNode()
        self.uiActions = CameraControllerUIActions(self.core.wnd)
        self.core.uiActions.addListener(self.uiActions)
        # Setup camera shortcuts.
        st = self.core.pini.load("camera.shortcuts")
        self.core.uiActionsShortcuts.clear()
        self.core.uiActionsShortcuts.setState(st)
        self.core.uiActionsShortcuts.setGroupEnabled("CameraController", True)
    def syncCameraWithNode(self, posValue = None, rotValue = None):
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
        self.ignoreCameraUpdates = True
        self.core.wnd.setState(st)
        self.ignoreCameraUpdates = False
    def syncNodeWithCamera(self, value):
        print "syncNodeWithCamera", value
        st = pymjin2.State()
        st.add(self.keyPos, value)
        self.ignoreNodeUpdates = True
        self.core.dscene.setState(st)
        self.ignoreNodeUpdates = False

def create():
    return CameraController()

