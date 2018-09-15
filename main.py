from pyvst import VstPlugin


def main():
    vst = VstPlugin('/home/simon/Downloads/DigitsLinux_2_1/DigitsVST_64.so')
    # vst = VstPlugin('/home/simon/code/oxefmsynth/oxevst64.so')
    print(vst.num_inputs)
    print(vst.num_outputs)
    print(vst.num_params)
    print(vst.num_programs)
    vst.set_param_value(10, 0.5)
    print(vst.get_param_value(10))
    print(vst.magic)
    print(vst.flags)
    print(vst.initial_delay)
    print(vst.unique_id)
    print(vst.version)
    print(vst._future2)

    for i in range(vst.num_params):
        name = vst.get_param_name(i)
        value = vst.get_param_value(i)
        display = vst.get_param_display(i)
        # label = vst.get_param_label(i)
        print('{}={} ({:.2f})'.format(name, display, value))

        prop = vst.get_param_properties(i)
        print(prop.step_float)
        print(prop.step_int)
        print(prop.flags)

    print(vst.vst_version)
    print(vst.num_midi_in)
    print(vst.num_midi_out)
    print(vst.get_input_properties(0))
    print(vst.get_output_properties(0))
    print(vst.get_output_properties(1))
    print(vst.get_output_properties(2))


if __name__ == '__main__':
    main()
