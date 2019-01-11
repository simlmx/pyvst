from pyvst.vstplugin import VstPlugin


def test_plugin(vst):
    vst = VstPlugin(vst)
    assert vst.num_params > 0

    # All the vsts we test are synths
    assert vst.is_synth
