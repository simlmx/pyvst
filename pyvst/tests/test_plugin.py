from pyvst.vstplugin import VstPlugin


def test_plugin():
    # TODO ship with some open source plugin
    # TODO this is also used in test_host.py, we should put it as a fixture in a confttest.py
    with open('.test_plugin_path.txt') as f:
        path = f.read().strip()

    vst = VstPlugin(path)
    assert vst.num_params > 0
