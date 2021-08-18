# <pep8-80 compliant>


import bpy
import zipfile
import os.path

from . import staff
from . import measure


class MSCZ2ANIM_OT_Load_Mscz(bpy.types.Operator):
    bl_idname = "mscz2anim.load_mscz"
    bl_label = "mscz2anim.load_mscz"
    bl_description = "load .mscz"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        props = scene.mscz2anim_prop
        if props.use_defusedxml:
            import defusedxml.ElementTree as ET
        else:
            import xml.etree.ElementTree as ET
        path = os.path.abspath(bpy.path.abspath(props.mscz_path))
        filename = bpy.path.display_name_from_filepath(path) + ".mscx"
        with zipfile.ZipFile(path) as myzip:
            with myzip.open(filename) as myfile:
                tree = ET.parse(myfile)
        MSCZ2ANIM_OT_Load_Mscz._root = tree.getroot()
        return {"FINISHED"}

    _root = ""

    def get_root():
        return MSCZ2ANIM_OT_Load_Mscz._root

    def instrument_items(scene, context):
        root = MSCZ2ANIM_OT_Load_Mscz.get_root()
        result = []
        try:
            root
            for index, value in enumerate(root.iter("Instrument")):
                result.append(
                    (str(index), value.attrib["id"], value.attrib["id"]))
            return result
        except AttributeError:
            return result


class MSCZ2ANIM_OT_Load_Sound(bpy.types.Operator):
    bl_idname = "mscz2anim.load_sound"
    bl_label = "mscz2anim.Load_sound"
    bl_description = "Load sound"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        props = scene.mscz2anim_prop
        bpy.data.sounds.load(props.sound_path)
        scene.sequence_editor.sequences.new_sound(
            name=bpy.path.basename(props.sound_path),
            filepath=props.sound_path,
            channel=props.channel,
            frame_start=props.frame_start)
        return {"FINISHED"}


class MSCZ2ANIM_OT_Generate(bpy.types.Operator):
    bl_idname = "mscz2anim.generate"
    bl_label = "mscz2anim.generate"
    bl_description = "generate"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.mscz2anim_prop
        root = MSCZ2ANIM_OT_Load_Mscz.get_root()
        list_staff = MSCZ2ANIM_OT_Generate._list_staff
        MSCZ2ANIM_OT_Generate._process_pre()
        for i in range(len(list_staff)):
            for index, child in enumerate(root[props.index_Score]):
                if child.tag == 'Staff' and\
                        child.attrib['id'] == list_staff[i]:
                    props.index_Staff = index
                    staff.Staff.process_staff()
        MSCZ2ANIM_OT_Generate._process_post()
        return {"FINISHED"}

    _index_part = []

    _list_staff = []

    def _process_pre():
        MSCZ2ANIM_OT_Generate._insert_frame0()
        MSCZ2ANIM_OT_Generate._set_index_score()
        MSCZ2ANIM_OT_Generate._set_index_part()
        MSCZ2ANIM_OT_Generate._set_list_staff()
        MSCZ2ANIM_OT_Generate._set_tempo()
        measure.Measure.repeat_check()

    def _insert_frame0():
        for index in range(21, 108):
            obj = bpy.data.objects["piano." + str(index)]
            obj.rotation_euler.x = 0
            obj.keyframe_insert(
                data_path="rotation_euler", index=0, frame=0)

    def _set_index_score():
        props = bpy.context.scene.mscz2anim_prop
        root = MSCZ2ANIM_OT_Load_Mscz.get_root()
        for index, child in enumerate(root):
            if child.tag == 'Score':
                props.index_Score = index

    def _set_index_part():
        props = bpy.context.scene.mscz2anim_prop
        root = MSCZ2ANIM_OT_Load_Mscz.get_root()
        MSCZ2ANIM_OT_Generate._index_part = []
        for index, child in enumerate(root[props.index_Score]):
            if child.tag == 'Part':
                MSCZ2ANIM_OT_Generate._index_part.append(index)

    def _set_list_staff():
        props = bpy.context.scene.mscz2anim_prop
        root = MSCZ2ANIM_OT_Load_Mscz.get_root()
        index_part = MSCZ2ANIM_OT_Generate._index_part
        for child in root[props.index_Score][index_part[int(
                props.instrument)]]:
            if child.tag == 'Staff':
                MSCZ2ANIM_OT_Generate._list_staff.append(child.attrib['id'])

    def _set_tempo():
        props = bpy.context.scene.mscz2anim_prop
        root = MSCZ2ANIM_OT_Load_Mscz.get_root()
        props.tempo = float(
            root.find("./Score/Staff/Measure/voice/Tempo/tempo").text)
        if props.log_tempo:
            print(
                "tempo=" + str(props.tempo * 60) +
                "bpm(" + str(props.tempo) + "bps)")

    def _process_post():
        MSCZ2ANIM_OT_Generate._set_frame()
        MSCZ2ANIM_OT_Generate._set_keyframe_interpolation()

    def _set_frame():
        scene = bpy.context.scene
        props = scene.mscz2anim_prop
        scene.frame_end = props.max_frame
        scene.frame_start = 0
        scene.frame_current = 0

    def _set_keyframe_interpolation():
        for i in range(21, 108):
            kfp = bpy.data.actions[
                "piano." + str(i) + "Action"].fcurves[0].keyframe_points
            for kf in kfp:
                kf.interpolation = 'CONSTANT'
