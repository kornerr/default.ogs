
import pymjin2

class ShadowedLightComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
        self.keys = [self.parent.key]
    def onComponentStateChange(self, st):
        #print "ShadowedLight.onComponentStateChange"
        self.parent.sync(st.value(st.keys[0])[0])

class ShadowedLight(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
    def __del__(self):
        pass
    def deinit(self):
        #print "ShadowedLight.deinit"
        self.core.dscene.removeListener(self.listener)
        self.listener = None
        pass
    def init(self, core, nodeName):
        #print "ShadowedLight.init"
        self.core = core
        self.nodeName = nodeName
        self.key = "node.{0}.position".format(self.nodeName)
        self.listener = ShadowedLightComponentListener(self)
        self.core.dscene.addListener(self.listener.keys, self.listener)
        # Light name.
        lightNameKey = "node.{0}.light".format(self.nodeName)
        s = self.core.dscene.state([lightNameKey])
        lightName = s.value(lightNameKey)[0]
        # Assign shadow map.
        self.core.dsceneNodeLight.setGraph(lightName, self.core.dscene.graph())
        graph = self.core.dsceneNodeLight.lightShadow(lightName)
        self.core.shadowCompositor.setScene(graph)
        self.core.shadowGraph.clear()
        self.core.shadowGraph.add(graph)
        # Sync right after assignment.
        self.sync()
    def sync(self, value = None):
        newValue = value
        if (newValue is None):
            st = self.core.dscene.state([self.key])
            newValue = st.value(self.key)[0]
        st = pymjin2.State()
        st.add("uniforms.lightPos", newValue)
        self.core.mainCompositor.setState(st)

def create():
    return ShadowedLight()

