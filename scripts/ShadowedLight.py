
import pymjin2

class ShadowedLightComponentListener(pymjin2.ComponentListener):
    def __init__(self, parent):
        pymjin2.ComponentListener.__init__(self)
        self.parent = parent
        self.keys = [self.parent.key]
    def onComponentStateChange(self, st):
        print "ShadowedLight.onComponentStateChange"
        self.parent.sync(st.value(st.keys[0])[0])

class ShadowedLight(pymjin2.DSceneNodeScriptInterface):
    def __init__(self):
        pymjin2.DSceneNodeScriptInterface.__init__(self)
    def __del__(self):
        pass
    def deinit(self):
        print "ShadowedLight.deinit"
        self.core.dscene.removeListener(self.listener)
        self.listener = None
        pass
    def init(self, core, nodeName):
        print "ShadowedLight.init"
        self.core = core
        self.nodeName = nodeName
        self.key = "node.{0}.position".format(self.nodeName)
        self.listener = ShadowedLightComponentListener(self)
        self.core.dscene.addListener(self.listener.keys, self.listener)
        # Assign shadow map.
        # TODO: retrieve "simpleLight" from "node.{0}.light"
#        self.core.shadowCompositor.setScene(self.core.dsceneNodeLight.lightShadow("simpleLight"))
#        self.core.shadowGraph.clear()
#        self.core.shadowGraph.add(self.core.dsceneNodeLight.lightShadow("simpleLight"))
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

