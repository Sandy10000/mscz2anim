# <pep8-80 compliant>


import bpy

from . import operators
from . import panels
from . import properties
from .translation import jajp


bl_info = {
    "name": "mscz2anim add-on",
    "author": "Sandy",
    "version": (2021, 8, 18),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar",
    "description":
        "Generate musical instrument performance animation"
        " from .mscz file of music score creation software musescore.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/Sandy10000/mscz2anim/wiki",
    "tracker_url": "https://github.com/Sandy10000/mscz2anim/issues",
    "category": "Animation"
}


translation_dict = {
    "ja_JP": jajp.dic,
}


class MSCZ2ANIM_PT_Panel(bpy.types.Panel):
    bl_label = "mscz2anim ver. %d.%d.%d" % bl_info["version"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "mscz2anim"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mscz2anim_prop

        layout.prop(
            props,
            "frame_start",
            text="Animation start frame")


classes = [
    operators.MSCZ2ANIM_OT_Load_Mscz,
    operators.MSCZ2ANIM_OT_Load_Sound,
    operators.MSCZ2ANIM_OT_Generate,
    MSCZ2ANIM_PT_Panel,
    panels.MSCZ2ANIM_PT_Load_Mscz,
    panels.MSCZ2ANIM_PT_Load_Sound,
    panels.MSCZ2ANIM_PT_Generate,
    panels.MSCZ2ANIM_PT_Log,
    properties.MSCZ2ANIM_Property,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.mscz2anim_prop = bpy.props.PointerProperty(
        type=properties.MSCZ2ANIM_Property)
    bpy.app.translations.register(__name__, translation_dict)


def unregister():
    bpy.app.translations.unregister(__name__)
    del bpy.types.Scene.mscz2anim_prop
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
