
import pymjin2

class CameraControllerComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
    def onComponentStateChange(self, st):
        #print "CameraController.onComponentStateChange"
        for key in st.keys:
            #print "key", key
            value = st.value(key)[0]
            if (key == self.parent.keyPos):
                self.parent.syncCameraWithNode(value)
            elif (key == self.parent.keyRot):
                self.parent.syncCameraWithNode(None, value)
            elif (key == "camera.position"):
                self.parent.syncNodeWithCamera(value)

class CameraControllerInputListener(pymjin2.InputListener):
    def __init__(self, parent):
        pymjin2.InputListener.__init__(self)
        self.parent = parent
        self.lastY = None
        self.enableRotation = False
    def onWindowInput(self, e):
        if (e.input == pymjin2.INPUT_MOUSE_BUTTON_RIGHT):
            self.enableRotation = e.press
            self.lastY = e.y
        elif ((e.input == pymjin2.INPUT_MOUSE_MOVE) and
              self.enableRotation):
            deltaY = self.lastY - e.y
            self.lastY = e.y
            self.parent.rotateNodeBy(0, deltaY)
        return False

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
        self.mouseSensitivity = 0.05
    def __del__(self):
        pass
    def deinit(self):
        self.core.dscene.removeListener(self.componentListener)
        self.core.wnd.removeListener(self.componentListener)
        self.componentListener = None
        self.core.uiActions.removeListener(self.uiActions)
        self.uiActions = None
        self.core.wndInput.removeListener(self.inputListener)
        self.inputListener = None
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
        self.inputListener = CameraControllerInputListener(self)
        self.core.wndInput.addListener(self.inputListener)
        # Sync right after assignment.
        self.syncCameraWithNode()
        self.uiActions = CameraControllerUIActions(self.core.wnd)
        self.core.uiActions.addListener(self.uiActions)
        # Setup camera shortcuts.
        st = self.core.pini.load("camera.shortcuts")
        self.core.uiActionsShortcuts.clear()
        self.core.uiActionsShortcuts.setState(st)
        self.core.uiActionsShortcuts.setGroupEnabled("CameraController", True)
    def rotateNodeBy(self, dx, dy):
        print "rotateNodeBy", dx, dy
        key = "node.{0}.rotationx".format(self.nodeName)
        st = self.core.dscene.state([key])
        value = float(st.value(key)[0])
        value += dy * self.mouseSensitivity
        st.set(key, str(value))
        self.core.dscene.setState(st)
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
        self.core.wnd.setState(st)
    def syncNodeWithCamera(self, value):
        st = pymjin2.State()
        st.add(self.keyPos, value)
        self.core.dscene.setState(st)

def create():
    return CameraController()

