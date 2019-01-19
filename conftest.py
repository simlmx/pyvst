import pytest

from pyvst import SimpleHost


def _find_test_plugins():
    """
    One plugin path per line in .test_plugin_path.txt
    """
    with open('.test_plugin_path.txt') as f:
        path = f.read().strip()

    lines = path.split('\n')
    lines = [x.strip() for x in lines]
    lines = [x for x in lines if not x.startswith('#')]
    return lines


_VST_PLUGINS = _find_test_plugins()


@pytest.fixture(params=_VST_PLUGINS)
def vst(request):
    return request.param


@pytest.fixture()
def host(vst):
    """SimpleHost containing a loaded vst."""
    host = SimpleHost(vst)
    return host
