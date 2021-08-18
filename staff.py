# <pep8-80 compliant>


import bpy

from . import operators
from . import measure


class Staff:
    def process_staff():
        props = bpy.context.scene.mscz2anim_prop
        root = operators.MSCZ2ANIM_OT_Load_Mscz.get_root()
        Staff._dic_staff['time'] = [0.0, 0.0, 0.0, 0.0]
        if props.log_dic_staff:
            print(Staff._dic_staff)
        measure.Measure.initialize_list_measure()
        for index, child in enumerate(
                root[props.index_Score][props.index_Staff]):
            if child.tag == 'Measure':
                measure.Measure.append_list_measure(index)
                measure.Measure.append_list_measure2(index)
        if props.log_list_measure:
            measure.Measure.print_list_measure()
        if props.is_repeat:
            measure.Measure.process_repeat()
        measure.Measure.process_measure()

    def get_dic_staff(key):
        props = bpy.context.scene.mscz2anim_prop
        return Staff._dic_staff[key][props.index_voice]

    def set_dic_staff(key, value):
        props = bpy.context.scene.mscz2anim_prop
        Staff._dic_staff[key][props.index_voice] = value

    def synchro_time():
        props = bpy.context.scene.mscz2anim_prop
        _dic_staff = Staff._dic_staff
        Staff._dic_staff['time'][1] = Staff._dic_staff['time'][0]
        Staff._dic_staff['time'][2] = Staff._dic_staff['time'][0]
        Staff._dic_staff['time'][3] = Staff._dic_staff['time'][0]
        if props.log_synchro_time:
            print("_dic_staff['time']=" + str(Staff._dic_staff['time']))

    def print_dic_staff():
        print("_dic_staff=" + str(Staff._dic_staff))

    _dic_staff = {
        'time': [0.0, 0.0, 0.0, 0.0],
        'Tie': [False, False, False, False],
        'sound_length2': [0.0, 0.0, 0.0, 0.0],
    }
