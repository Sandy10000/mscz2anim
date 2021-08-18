# <pep8-80 compliant>


import bpy

from . import operators


class MSCZ2ANIM_PT:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "mscz2anim"


class MSCZ2ANIM_PT_Load_Mscz(MSCZ2ANIM_PT, bpy.types.Panel):
    bl_label = "Load .mscz file"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mscz2anim_prop

        layout.prop(
            props,
            "use_defusedxml",
            text="Use defusedxml")
        layout.prop(
            props,
            "mscz_path",
            text="File path")
        layout.operator(
            operators.MSCZ2ANIM_OT_Load_Mscz.bl_idname,
            text=bpy.app.translations.pgettext("Load .mscz file"))


class MSCZ2ANIM_PT_Load_Sound(MSCZ2ANIM_PT, bpy.types.Panel):
    bl_label = "Load sound file"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mscz2anim_prop

        layout.prop(
            props,
            "sound_path",
            text="File path")
        layout.prop(
            props,
            "channel",
            text="channel")
        layout.operator(
            operators.MSCZ2ANIM_OT_Load_Sound.bl_idname,
            text=bpy.app.translations.pgettext("Load sound file"))


class MSCZ2ANIM_PT_Generate(MSCZ2ANIM_PT, bpy.types.Panel):
    bl_label = "Generate animation"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mscz2anim_prop

        layout.prop(
            props,
            "instrument",
            text="Piano")
        layout.operator(
            operators.MSCZ2ANIM_OT_Generate.bl_idname,
            text=bpy.app.translations.pgettext("Generate animation"))


class MSCZ2ANIM_PT_Log(MSCZ2ANIM_PT, bpy.types.Panel):
    bl_label = bpy.app.translations.pgettext("Log")
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.mscz2anim_prop

        layout.prop(
            props,
            "log_tempo",
            text="tempo")
        layout.prop(
            props,
            "log_dic_staff",
            text="_dic_staff")
        layout.prop(
            props,
            "log_list_measure",
            text="list_measure")
        layout.prop(
            props,
            "log_synchro_time",
            text="synchro_time")
        layout.prop(
            props,
            "log_insert_keyframe",
            text="insert_keyframe")
        layout.prop(
            props,
            "log_measure_number",
            text="measure_number")
        layout.prop(
            props,
            "log_note_length",
            text="note_length")
        layout.prop(
            props,
            "log_time",
            text="time")
