bl_info = {
    "name": "VisualFluidX3D",
    "author": "Davide Vigano",
    "version": (0, 1),
    "blender": (4, 1, 0),
    "location": "Preferences > Add-ons",
    "description": "Clones and compiles the FluidX3D addon from GitHub into the addon directory.",
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

def compile_solution():
    solution_path = os.path.join(os.getcwd(), "FluidX3D", "FluidX3D.sln")
    print(solution_path)
    
    # Check if the solution file exists
    if not os.path.exists(solution_path):
        print("Solution file does not exist in the current directory.")
        return "Solution file does not exist."

    # Compile the solution using Visual Studio's devenv
    try:
        subprocess.run(["devenv", solution_path, "/Build", "Release"], check=True)
        return "Solution compiled successfully."
    except subprocess.CalledProcessError as e:
        return f"Failed to compile the solution: {e}"

class VISUALFLUIDX3D_OT_compile(bpy.types.Operator):
    """Compile FluidX3D Solution"""
    bl_idname = "wm.visual_fluidx3d_compile"
    bl_label = "Compile FluidX3D"

    def execute(self, context):
        message = compile_solution()
        self.report({'INFO'}, message)
        return {'FINISHED'}

class VisualFluidX3DPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Clone the FluidX3D repository to your Blender addon directory.")
        layout.operator(VISUALFLUIDX3D_OT_clone.bl_idname)
        layout.operator(VISUALFLUIDX3D_OT_compile.bl_idname)

def register():
    bpy.utils.register_class(VISUALFLUIDX3D_OT_clone)
    bpy.utils.register_class(VISUALFLUIDX3D_OT_compile)
    bpy.utils.register_class(VisualFluidX3DPreferences)

def unregister():
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_clone)
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_compile)
    bpy.utils.unregister_class(VisualFluidX3DPreferences)

if __name__ == "__main__":
    register()
