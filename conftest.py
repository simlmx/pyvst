import pytest


def _find_test_plugins():
    """
    One plugin path per line in .test_plugin_path.txt
    """
    with open('.test_plugin_path.txt') as f:
        path = f.read().strip()

    return path.split('\n')


_VST_PLUGINS = _find_test_plugins()


@pytest.fixture(params=_VST_PLUGINS)
def vst(request):
    return request.param
