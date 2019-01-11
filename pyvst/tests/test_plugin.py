from pyvst.vstplugin import VstPlugin


def test_plugin(vst):
    vst = VstPlugin(vst)
    assert vst.num_params > 0
