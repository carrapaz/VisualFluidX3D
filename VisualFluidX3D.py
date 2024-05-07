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

def git_clone_repository():
    # Repository URL
    repo_url = "https://github.com/ProjectPhysX/FluidX3D.git"
    # Directory where this script is located
    addon_dir = os.path.join(os.environ['APPDATA'], 'Blender Foundation', 'Blender', '4.1', 'scripts', 'addons', 'FluidX3D')
    # Command to clone the repository
    cmd = ["git", "clone", repo_url, addon_dir]
    # Execute the git command
    try:
        subprocess.run(cmd, check=True)
        print("FluidX3D cloned successfully into: " + addon_dir)
    except subprocess.CalledProcessError as e:
        print("Failed to clone repository: " + str(e))

def find_msbuild():
    # Path to vswhere.exe - adjust if necessary
    vswhere_path = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
    # Use vswhere to find the installation path for MSBuild
    try:
        result = subprocess.run([vswhere_path, "-latest", "-requires", "Microsoft.Component.MSBuild", "-find", "MSBuild\\**\\Bin\\MSBuild.exe", "-format", "json"], capture_output=True, text=True, check=True)
        installations = json.loads(result.stdout)
        if installations:
            return installations[0]  # Returns the path to the latest MSBuild executable
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
    executable_path = os.path.join(os.getcwd(), "FluidX3D", "bin", "FluidX3D")
    # Command to open a new console window
    command = f'start cmd /K "{executable_path}"'
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Failed to run the application: {e}")

def compile_and_play_simulation():
    
    msbuild_path = find_msbuild()
    print("found msbuild")
    
    solution_path = os.path.join(os.environ['APPDATA'], 'Blender Foundation', 'Blender', '4.1', 'scripts', 'addons', 'FluidX3D', "FluidX3D.sln")
    print("solution path: ",solution_path)
    
    compile_solution(msbuild_path, solution_path)
    run_application()


class VISUALFLUIDX3D_OT_CloneRepo(bpy.types.Operator):
    """Clone FluidX3D Repository"""
    bl_idname = "wm.visual_fluidx3d_clone_repo"
    bl_label = "Clone FluidX3D Repository"

    def execute(self, context):
        git_clone_repository()
        return {'FINISHED'}

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
        layout.operator(VISUALFLUIDX3D_OT_CloneRepo.bl_idname)
        layout.operator(VISUALFLUIDX3D_OT_CompileAndPlay.bl_idname)

def register():
    bpy.utils.register_class(VISUALFLUIDX3D_OT_CloneRepo)
    bpy.utils.register_class(VISUALFLUIDX3D_OT_CompileAndPlay)
    bpy.utils.register_class(VisualFluidX3DPreferences)

def unregister():
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_CloneRepo)
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_CompileAndPlay)
    bpy.utils.unregister_class(VisualFluidX3DPreferences)

if __name__ == "__main__":
    register()
