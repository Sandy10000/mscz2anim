# Does not meet PEP8 requirements


import bpy
from . import operators


class MSCZ2ANIM_Property(bpy.types.PropertyGroup):
    channel:bpy.props.IntProperty(default=1)
    dots: bpy.props.StringProperty(default="")
    durationType: bpy.props.StringProperty(default="")
    endRepeat: bpy.props.IntProperty()
    frame_start: bpy.props.IntProperty(default=1)
    index_Measure: bpy.props.IntProperty()
    index_Score: bpy.props.IntProperty()
    index_Staff: bpy.props.IntProperty()
    index_voice: bpy.props.IntProperty()
    instrument: bpy.props.EnumProperty(
        name="Instrument",
        items=operators.MSCZ2ANIM_OT_Load_Mscz.instrument_items)
    is_repeat: bpy.props.BoolProperty(default=False)
    log_dic_staff: bpy.props.BoolProperty(default=False)
    log_insert_keyframe: bpy.props.BoolProperty(default=False)
    log_list_measure: bpy.props.BoolProperty(default=False)
    log_list_voice: bpy.props.BoolProperty(default=False)
    log_measure_number: bpy.props.BoolProperty(default=False)
    log_note_length: bpy.props.BoolProperty(default=False)
    log_synchro_time: bpy.props.BoolProperty(default=False)
    log_tempo: bpy.props.BoolProperty(default=False)
    log_time: bpy.props.BoolProperty(default=False)
    max_frame: bpy.props.IntProperty()
    mscz_path: bpy.props.StringProperty(subtype='FILE_PATH')
    obj_name: bpy.props.StringProperty(default="")
    piano_key_down: bpy.props.FloatProperty(default=0.0698132)
    piano_key_up: bpy.props.FloatProperty(default=0.0)
    sigD: bpy.props.FloatProperty(default=0.0)
    sigN: bpy.props.FloatProperty(default=0.0)
    sound_length: bpy.props.FloatProperty(default=0.0)
    sound_path: bpy.props.StringProperty(subtype='FILE_PATH')
    startRepeat: bpy.props.IntProperty(default=0)
    tempo: bpy.props.FloatProperty(default=0.0)
    Tuplet: bpy.props.FloatProperty(default=1.0)
    use_defusedxml: bpy.props.BoolProperty(default=True)
