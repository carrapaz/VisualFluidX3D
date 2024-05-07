import bpy
import subprocess
import os
import json

bl_info = {
    "name": "VisualFluidX3D",
    "author": "Davide Vigano",
    "version": (0, 1),
    "blender": (4, 1, 0),
    "location": "Preferences > Add-ons",
    "description": "Clones, compiles, and runs the FluidX3D addon from GitHub.",
    "warning": "",
    "doc_url": "",
    "category": "System",
}

def find_msbuild():
    vswhere_path = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
    try:
        result = subprocess.run([vswhere_path, "-latest", "-requires", "Microsoft.Component.MSBuild", "-find", "MSBuild\\**\\Bin\\MSBuild.exe", "-format", "json"], capture_output=True, text=True, check=True)
        installations = json.loads(result.stdout)
        if installations:
            return installations[0]
    except subprocess.CalledProcessError as e:
        print(f"Error finding MSBuild with vswhere: {e}")
    return None

def compile_solution(msbuild_path, solution_path):
    try:
        result = subprocess.run([msbuild_path, solution_path, "/p:Configuration=Release"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print("Failed to compile the solution:")
            print(result.stdout)
            print(result.stderr)
        else:
            print("Solution compiled successfully.")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def run_application():
    executable_path = os.path.join(os.getcwd(), "FluidX3D", "bin", "FluidX3D.exe")
    command = f'start cmd /K "{executable_path}"'
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Failed to run the application: {e}")

def compile_and_play_simulation():
    msbuild_path = find_msbuild()
    solution_path = os.path.join(os.environ['APPDATA'], 'Blender Foundation', 'Blender', '4.1', 'scripts', 'addons', 'FluidX3D', "FluidX3D.sln")
    compile_solution(msbuild_path, solution_path)
    run_application()

class VISUALFLUIDX3D_OT_CompileAndPlay(bpy.types.Operator):
    """Compile and Run FluidX3D Simulation"""
    bl_idname = "wm.visual_fluidx3d_compile_and_play"
    bl_label = "Compile and Run Simulation"

    def execute(self, context):
        compile_and_play_simulation()
        return {'FINISHED'}

class VisualFluidX3DPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(VISUALFLUIDX3D_OT_CompileAndPlay.bl_idname)

def register():
    bpy.utils.register_class(VISUALFLUIDX3D_OT_CompileAndPlay)
    bpy.utils.register_class(VisualFluidX3DPreferences)

def unregister():
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_CompileAndPlay)
    bpy.utils.unregister_class(VisualFluidX3DPreferences)

if __name__ == "__main__":
    register()
