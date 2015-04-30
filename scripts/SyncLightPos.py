
import pymjin2

class SyncLightPosComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
        self.keys = [self.parent.key]
    def onComponentStateChange(self, st):
        #print "SyncLightPos.onComponentStateChange"
        self.parent.sync(st.value(st.keys[0])[0])

class SyncLightPos(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
    def __del__(self):
        pass
    def deinit(self):
        #print "SyncLightPos.deinit"
        self.core.dscene.removeListener(self.listener)
        self.listener = None
        pass
    def init(self, core, nodeName):
        #print "SyncLightPos.init"
        self.core = core
        self.nodeName = nodeName
        self.key = "node.{0}.position".format(self.nodeName)
        self.listener = SyncLightPosComponentListener(self)
        self.core.dscene.addListener(self.listener.keys, self.listener)
        # Sync right after assignment.
        self.sync()
    def sync(self, value = None):
        newValue = value
        #print "newValue:", newValue
        if (newValue is None):
            st = self.core.dscene.state([self.key])
            newValue = st.value(self.key)[0]
        st = pymjin2.State()
        st.add("uniforms.lightPos", newValue)
        self.core.mainCompositor.setState(st)

def create():
    return SyncLightPos()

