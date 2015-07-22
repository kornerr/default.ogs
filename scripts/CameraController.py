
import pymjin2

class CameraControllerComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
        self.lastX = None
        self.lastY = None
        self.center = None
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
            elif (key == "mouse.center"):
                self.center = value
            elif (key == "mouse.position"):
                v = value.split(" ")
                x = int(v[0])
                y = int(v[1])
                if (self.parent.enableRotation):
                    deltaX = self.lastX - x
                    deltaY = self.lastY - y
                    self.parent.rotateNodeBy(deltaX, deltaY)
                    # Center mouse.
                    s = pymjin2.State()
                    s.set("mouse.position", self.center)
                    self.parent.core.wnd.setState(s)
                    v = self.center.split(" ")
                    self.lastX = int(v[0])
                    self.lastY = int(v[1])
                else:
                    self.lastX = x
                    self.lastY = y

class CameraControllerUIActions(object):
    def __init__(self, parent):
        self.parent = parent
    def name(self):
        return "CameraController"
    def onUIActionsExecute(self, action, state):
        self.parent.processUIAction(action, state)

class CameraController(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
        self.mouseSensitivity = 0.1
        self.ignoreCameraSync = False
        self.enableRotation = False
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
        self.core.wnd.addListener(
            ["camera.position",
             "camera.rotationq",
             "mouse.position",
             "mouse.center"],
            self.componentListener)
        # Sync right after assignment.
        self.syncCameraWithNode()
        self.uiActions = CameraControllerUIActions(self)
        self.core.uiActions.addListener(self.uiActions)
        # Setup camera shortcuts.
        st = self.core.pini.load("camera.shortcuts")
        self.core.uiActionsShortcuts.clear()
        self.core.uiActionsShortcuts.setState(st)
        self.core.uiActionsShortcuts.setGroupEnabled("CameraController", True)
    def processUIAction(self, action, state):
        s = pymjin2.State()
        if (action == "ToggleMove"):
            self.enableRotation = state
            s.set("mouse.visible", "0" if self.enableRotation else "1")
            # Disable all movement.
            if (not self.enableRotation):
                s.set("camera.moveBackward", "0")
                s.set("camera.moveDown",     "0")
                s.set("camera.moveForward",  "0")
                s.set("camera.moveLeft",     "0")
                s.set("camera.moveRight",    "0")
                s.set("camera.moveUp",       "0")
        if (self.enableRotation):
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
            if (postfix):
                s.set("camera.move" + postfix , "1" if state else "0")
        self.core.wnd.setState(s)
    def rotateNodeBy(self, dz, dx):
        keys = []
        keyx = "node.{0}.rotationx".format(self.nodeName)
        keyz = "node.{0}.rotationz".format(self.nodeName)
        if (dz != 0):
            keys.append(keyz)
        if (dx != 0):
            keys.append(keyx)
        if (len(keys)):
            st = self.core.dscene.state(keys)
            if (dx != 0):
                valuex = float(st.value(keyx)[0])
                diff = float(dx) * self.mouseSensitivity
                valuex += diff
                st.set(keyx, str(valuex))
            if (dz != 0):
                valuez = float(st.value(keyz)[0])
                diff = float(dz) * self.mouseSensitivity
                valuez += diff
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

