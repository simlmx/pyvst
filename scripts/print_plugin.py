import argparse

from pyvst import VstPlugin


def _main(filename):
    plugin = VstPlugin(filename)

    # TODO print more than that!
    print('-- Parameters --')
    for index in range(plugin.num_params):
        print('[{}] {} = {} {}'.format(
            index,
            plugin.get_param_name(index),
            plugin.get_param_value(index),
            plugin.get_param_label(index)
        ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('vst', help='path to .so file')
    args = parser.parse_args()

    _main(args.vst)
