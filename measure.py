# <pep8-80 compliant>


import bpy

from . import operators
from . import voice


class Measure:
    def process_measure():
        props = bpy.context.scene.mscz2anim_prop
        root = operators.MSCZ2ANIM_OT_Load_Mscz.get_root()
        staff = root[props.index_Score][props.index_Staff]
        for props.index_Measure in Measure._list_measure2:
            if props.log_measure_number:
                print("Measure number=" + str(Measure.get_measure_number()))
            list_voice = []
            for index, child in enumerate(staff[props.index_Measure]):
                if child.tag == 'voice':
                    list_voice.append(index)
            if props.log_list_voice:
                print("list_voice=" + str(list_voice))
            voice.Voice.process_voice(list_voice)

    def initialize_list_measure():
        Measure._list_measure = []
        Measure._list_measure2 = []

    def append_list_measure(value):
        Measure._list_measure.append(value)

    def append_list_measure2(value):
        Measure._list_measure2.append(value)

    def get_measure_number():
        props = bpy.context.scene.mscz2anim_prop
        return Measure._list_measure.index(props.index_Measure) + 1

    def print_list_measure():
        print("_list_measure=" + str(Measure._list_measure))

    def repeat_check():
        props = bpy.context.scene.mscz2anim_prop
        root = operators.MSCZ2ANIM_OT_Load_Mscz.get_root()
        for child in root[props.index_Score]:
            if child.tag == 'Staff' and child.attrib['id'] == '1':
                for index, child2 in enumerate(child):
                    if child2.tag == 'Measure':
                        Measure.append_list_measure(index)
                        for child3 in child2:
                            if child3.tag == 'startRepeat':
                                props.startRepeat =\
                                    Measure._list_measure.index(index)
                                props.is_repeat = True
                            if child3.tag == 'endRepeat':
                                props.endRepeat =\
                                    Measure._list_measure.index(index)

    def process_repeat():
        props = bpy.context.scene.mscz2anim_prop
        for i, index in enumerate(Measure._generate_list_repeat_measure()):
            Measure._list_measure2.insert(props.endRepeat + i + 1, index)
        if props.log_list_measure:
            print("list_Measure=" + str(Measure._list_measure))
            print("list_Measure_length=" + str(len(Measure._list_measure)))
            print("list_Measure2=" + str(Measure._list_measure2))
            print("list_Measure_length2=" + str(len(Measure._list_measure2)))

    _list_measure = []

    _list_measure2 = []

    def _generate_list_repeat_measure():
        props = bpy.context.scene.mscz2anim_prop
        result = []
        for index in range(props.startRepeat, props.endRepeat + 1):
            result.append(Measure._list_measure[index])
        if props.log_list_measure:
            print("list_repeat=" + str(result))
        return result
