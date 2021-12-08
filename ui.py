##############################################################################
# Imports
##############################################################################


if 'bpy' not in locals():
    import bpy
else:
    from importlib import reload


##############################################################################
# Classes
##############################################################################


class VIEW3D_PT_lighting_tools(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_lighting_tools'
    bl_label = 'Lighting Tools'
    bl_category = 'SamTools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        lay = self.layout
        lay.operator('lighting_tools.lighting_ot_create_light',
            icon='OUTLINER_OB_LIGHT')


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_lighting_tools,
])
