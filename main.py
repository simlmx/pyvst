from pyvst import VstPlugin


def main():
    vst = VstPlugin('/home/simon/Downloads/DigitsLinux_2_1/DigitsVST_64.so')
    # vst = VstInstrument('/home/simon/code/oxefmsynth/oxevst64.so')
    print(vst.num_inputs)
    print(vst.num_outputs)
    print(vst.num_params)
    print(vst.num_programs)
    vst.set_parameter(0, 0.5)
    print(vst.get_parameter(0))
    print(vst.magic)
    print(vst.flags)
    print(vst.initial_delay)
    print(vst.unique_id)
    print(vst.version)
    print(vst._future2)

    from ctypes import c_void_p
    ptr = c_void_p()
    print(vst._dispatch(6, ptr=ptr))


if __name__ == '__main__':
    main()
