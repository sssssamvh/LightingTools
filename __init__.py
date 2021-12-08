################################################################################
# Imports
################################################################################


if 'bpy' not in locals():
    import bpy
    from . import operators
    from . import ui
else:
    import importlib
    operators = importlib.reload(operators)
    ui = importlib.reload(ui)


################################################################################
# Add-on information
################################################################################


bl_info = {
    'author': 'Sam Van Hulle',
    'blender': (3, 0, 0),
    'category': 'Tools',
    'name': 'Lighting Tools',
    'version': (0, 0, 1),
}


################################################################################
# Registration
################################################################################


modules = [
    operators,
    ui,
]

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()

if __name__ == '__main__':
    register()
