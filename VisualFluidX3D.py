bl_info = {
    "name": "VisualFluidX3D",
    "author": "Davide Vigano",
    "version": (0, 1),
    "blender": (4, 1, 0),
    "location": "Preferences > Add-ons",
    "description": "Clones the FluidX3D addon from GitHub into the addon directory.",
    "warning": "",
    "doc_url": "",
    "category": "System",
}

import bpy
import subprocess
import os

def git_clone_repository():
    # Repository URL
    repo_url = "https://github.com/ProjectPhysX/FluidX3D.git"
    
    # Directory where this script is located
    addon_dir = os.path.dirname(__file__)
    
    # Command to clone the repository
    cmd = ["git", "clone", repo_url, os.path.join(addon_dir, "FluidX3D")]
    
    # Execute the git command
    try:
        subprocess.run(cmd, check=True)
        return "FluidX3D cloned successfully into: " + addon_dir
    except subprocess.CalledProcessError as e:
        return "Failed to clone repository: " + str(e)

class VISUALFLUIDX3D_OT_clone(bpy.types.Operator):
    """Clone FluidX3D Repository"""
    bl_idname = "wm.visual_fluidx3d_clone"
    bl_label = "Clone FluidX3D"

    def execute(self, context):
        message = git_clone_repository()
        self.report({'INFO'}, message)
        return {'FINISHED'}

def add_clone_button(self, context):
    self.layout.operator(
        VISUALFLUIDX3D_OT_clone.bl_idname,
        text="Clone FluidX3D Repository",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(VISUALFLUIDX3D_OT_clone)
    bpy.types.VIEW3D_MT_mesh_add.append(add_clone_button)

def unregister():
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_clone)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_clone_button)

if __name__ == "__main__":
    register()
