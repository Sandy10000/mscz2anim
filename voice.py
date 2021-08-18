# <pep8-80 compliant>


import bpy

from . import operators
from . import staff
from . import measure


class Voice:
    def process_voice(list_voice):
        props = bpy.context.scene.mscz2anim_prop
        root = operators.MSCZ2ANIM_OT_Load_Mscz.get_root()
        m = root[props.index_Score][props.index_Staff][props.index_Measure]
        for props.index_voice, index in enumerate(list_voice):
            for child in m[index]:
                if child.tag == 'TimeSig':
                    for child2 in child:
                        if child2.tag == 'sigN':
                            props.sigN = float(child2.text)
                        if child2.tag == 'sigD':
                            props.sigD = float(child2.text)
                        if props.log_note_length:
                            Voice._print_note_length()
                if child.tag == 'Tempo':
                    for child2 in child:
                        if child2.tag == 'tempo':
                            props.tempo = float(child2.text)
                if child.tag == 'Tuplet':
                    Voice._process_tuplet(child)
                if child.tag == 'endTuplet':
                    props.Tuplet = 1.0
                if child.tag == 'Chord' or child.tag == 'Rest':
                    Voice._process_chord_rest(child)
        staff.Staff.synchro_time()

    _dic_durationType = {
        'whole': 1.0,
        'half': 0.5,
        'quarter': 0.25,
        'eighth': 0.125,
        '16th': 0.0625,
        '32nd': 0.03125
    }

    def _get_sound_length():
        props = bpy.context.scene.mscz2anim_prop
        if props.durationType == 'measure':
            result = props.sigN / props.tempo
        else:
            result = Voice._dic_durationType[props.durationType] *\
                props.Tuplet * props.sigD / props.tempo
        if props.dots == '1':
            result *= 1.5
        return result

    def _process_chord_rest(child):
        props = bpy.context.scene.mscz2anim_prop
        get_dic_staff = staff.Staff.get_dic_staff
        set_dic_staff = staff.Staff.set_dic_staff
        props.dots = ""
        props.durationType = ""
        Articulation = ""
        Arpeggio = ""
        Note = []
        for child2 in child:
            if child2.tag == 'dots':
                props.dots = child2.text
            if child2.tag == 'durationType':
                props.durationType = child2.text
            if child2.tag == 'Articulation':
                for child3 in child2:
                    if child3.tag == 'subtype':
                        Articulation = child3.text
            if child2.tag == 'Tuplet':
                Voice._process_tuplet(child2)
            if child2.tag == 'endTuplet':
                props.Tuplet = 1.0
            if child2.tag == 'Note':
                for child3 in child2:
                    if child3.tag == 'Spanner' and\
                            child3.attrib['type'] == 'Tie':
                        for child4 in child3:
                            if child4.tag == 'next':
                                set_dic_staff('Tie', True)
                    if child3.tag == 'pitch':
                        Note.append(child3.text)
            if child2.tag == 'Arpeggio':
                for child3 in child2:
                    if child3.tag == 'subtype':
                        Arpeggio = child3.text
        props.sound_length = Voice._get_sound_length()
        set_dic_staff('sound_length2', props.sound_length)
        Voice._key_down(Arpeggio, Note)
        if not get_dic_staff('Tie'):
            Voice._key_up(Arpeggio, Note)
            set_dic_staff('sound_length2', 0.0)
        else:
            set_dic_staff('Tie', False)
        set_dic_staff('time', get_dic_staff('time') + props.sound_length)
        if props.log_time:
            print(
                "voice" + str(props.index_voice + 1) +
                " ,time=" + str(get_dic_staff('time')))

    def _process_tuplet(child):
        normalNotes = float(child.find("./normalNotes").text)
        actualNotes = float(child.find("./actualNotes").text)
        bpy.context.scene.mscz2anim_prop.Tuplet = normalNotes / actualNotes

    def _insert_keyframe(time, rotation):
        scene = bpy.context.scene
        props = scene.mscz2anim_prop
        fps = scene.render.fps
        frame_number = int(fps * time) + props.frame_start
        props.max_frame = max(props.max_frame, frame_number)
        obj = bpy.data.objects[props.obj_name]
        obj.rotation_euler.x = rotation
        obj.keyframe_insert(
            data_path="rotation_euler", index=0, frame=frame_number)
        if props.log_insert_keyframe:
            print(
                "m" + str(measure.Measure.get_measure_number()) +
                " ,v" + str(props.index_voice + 1) +
                " ,f" + str(frame_number) +
                " ," + props.obj_name +
                " ,r" + str(rotation))

    def _key_down(Arpeggio, Note):
        props = bpy.context.scene.mscz2anim_prop
        for n in Note:
            props.obj_name = "piano." + n
            Voice._insert_keyframe(
                staff.Staff.get_dic_staff('time'), props.piano_key_down)

    def _key_up(Arpeggio, Note):
        props = bpy.context.scene.mscz2anim_prop
        for n in Note:
            props.obj_name = "piano." + n
            Voice._insert_keyframe(
                staff.Staff.get_dic_staff('time') + (
                    staff.Staff.get_dic_staff('sound_length2') * .95),
                props.piano_key_up)

    def _print_note_length():
        props = bpy.context.scene.mscz2anim_prop
        print("sigN=" + str(props.sigN) + " ,sigD=" + str(props.sigD))
        print("whole:" + str(props.sigD / props.tempo) + "s")
        print("half:" + str(props.sigD / props.tempo * .5) + "s")
        print("quarter:" + str(props.sigD / props.tempo * .25) + "s")
        print("eighth:" + str(props.sigD / props.tempo * .125) + "s")
        print("16th:" + str(props.sigD / props.tempo * .0625) + "s")
        print("32nd:" + str(props.sigD / props.tempo * .03125) + "s")
