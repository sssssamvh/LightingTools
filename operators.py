##############################################################################
# Imports
##############################################################################


if 'bpy' not in locals():
    import bpy
else:
    from importlib import reload


##############################################################################
# Operators
##############################################################################


class LIGHTING_OT_create_light(bpy.types.Operator):
    '''Create a light with pre-set properties'''

    bl_idname = 'lighting_tools.lighting_ot_create_light'
    bl_label = 'Create Lights'
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(name='Name', default='light')
    amount: bpy.props.IntProperty(name='Amount', default=1)
    light_type: bpy.props.EnumProperty(name='Type', items=[
        ('POINT', 'Point', 'sdfbdsfb', 'LIGHT_POINT', 0),
        ('SUN', 'Sun', 'dsdbf', 'LIGHT_SUN', 1),
        ('SPOT', 'Spot', 'sdfbsdfb', 'LIGHT_SPOT', 2),
        ('AREA', 'Area', 'sgsdf', 'LIGHT_AREA', 3),
    ], default='SPOT')
    purpose: bpy.props.EnumProperty(name='Purpose', items=[
        ('regular', 'Regular', 'Light for regular view layers',
            'LIGHT_DATA', 0),
        ('vol', 'Volumetric', 'Volumetric light', 'VOLUME_DATA', 1),
    ])
    with_aim: bpy.props.BoolProperty(name='With Aim', default=False)

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        lay.prop(self, 'name')
        lay.prop(self, 'amount')
        if self.light_type != 'POINT':
            lay.prop(self, 'with_aim')
        lay.separator()
        lay.use_property_split = False
        lay.row().prop(self, 'light_type', expand=True)
        lay.separator()
        lay.row().prop(self, 'purpose', expand=True)

    def execute(self, context):
        # Determine the lights' name based on their purpose.
        is_volumetric = self.purpose == 'vol'
        if is_volumetric:
            name = f'{self.name}.VOL.001'
        else:
            name = f'{self.name}.LGT.001'
        ray_types = ['diffuse', 'glossy', 'transmission']
        # Clear the current selection.
        for o in context.selected_objects:
            o.select_set(False)
        # Iterate over the amount of requested lights.
        for i in range(self.amount):
            # Create the light.
            light = bpy.data.lights.new(name=name, type=self.light_type)
            ob = bpy.data.objects.new(name=name, object_data=light)
            ob.location[2] = 1.0
            context.scene.collection.objects.link(ob)
            # Set ray type visibility based on the purpose.
            for ray_type in ray_types:
                setattr(ob, f'visible_{ray_type}', not is_volumetric)
            ob.visible_volume_scatter = is_volumetric
            # If With Aim has been enabled, create the aim and constraint
            if self.with_aim and self.light_type != 'POINT':
                aim = bpy.data.objects.new(name=f'{self.name}Aim.LOC.001',
                    object_data=None)
                context.scene.collection.objects.link(aim)
                constraint = ob.constraints.new(type='DAMPED_TRACK')
                constraint.target = aim
                constraint.track_axis = 'TRACK_NEGATIVE_Z'
            # Select the newly created light, and make it the active object.
            context.view_layer.objects.active = ob
            ob.select_set(True)
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    LIGHTING_OT_create_light,
])
