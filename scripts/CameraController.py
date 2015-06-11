
import pymjin2

class CameraControllerComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
    def onComponentStateChange(self, st):
        #print "CameraController.onComponentStateChange"
        for key in st.keys:
            #print "key", key, "value", st.value(key)
            value = st.value(key)[0]
            if (key == self.parent.keyPos):
                self.parent.syncCameraWithNode(value)
            elif (key == self.parent.keyRot):
                self.parent.syncCameraWithNode(None, value)
            elif (key == "camera.position"):
                self.parent.syncNodeWithCamera(value)
            elif (key == "camera.rotationq"):
                self.parent.syncNodeWithCamera(None, value)

class CameraControllerInputListener(pymjin2.InputListener):
    def __init__(self, parent):
        pymjin2.InputListener.__init__(self)
        self.parent = parent
        self.lastX = None
        self.lastY = None
        self.enableRotation = False
    def onWindowInput(self, e):
        if (e.input == pymjin2.INPUT_MOUSE_BUTTON_RIGHT):
            self.enableRotation = e.press
            self.lastX = e.x
            self.lastY = e.y
            st = pymjin2.State()
            st.set("mouse.visible", "0" if self.enableRotation else "1")
            self.parent.core.wnd.setState(st)
            self.parent.core.uiActionsShortcuts.setGroupEnabled(
                "CameraController", self.enableRotation)
        elif ((e.input == pymjin2.INPUT_MOUSE_MOVE) and
              self.enableRotation):
            deltaX = self.lastX - e.x
            deltaY = self.lastY - e.y
            self.parent.rotateNodeBy(deltaX, deltaY)
            # Center mouse.
            self.parent.core.wndMouse.center()
            st = self.parent.core.wnd.state(["mouse.center"])
            v = st.value("mouse.center")[0].split(" ")
            self.lastX = int(v[0])
            self.lastY = int(v[1])
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
        self.mouseSensitivity = 0.1
        self.ignoreCameraSync = False
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
        self.core.wnd.addListener(
            ["camera.position",
             "camera.rotationq"],
            self.componentListener)
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
    def rotateNodeBy(self, dx, dy):
        keyx = "node.{0}.rotationx".format(self.nodeName)
        keyz = "node.{0}.rotationz".format(self.nodeName)
        st = self.core.dscene.state([keyx, keyz])
        valuex = float(st.value(keyx)[0])
        valuex += dy * self.mouseSensitivity
        st.set(keyx, str(valuex))
        valuez = float(st.value(keyz)[0])
        valuez += dx * self.mouseSensitivity
        st.set(keyz, str(valuez))
        self.core.dscene.setState(st)
    def syncCameraWithNode(self, posValue = None, rotValue = None):
        if (self.ignoreCameraSync):
            return;
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
    def syncNodeWithCamera(self, posValue = None, rotValue = None):
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
        st = pymjin2.State()
        st.add(self.keyPos, newPosValue)
        st.add(self.keyRot, newRotValue)
        self.ignoreCameraSync = True
        self.core.dscene.setState(st)
        self.ignoreCameraSync = False

def create():
    return CameraController()

