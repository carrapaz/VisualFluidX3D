import webbrowser
import subprocess
import json
import bpy
import os

from bpy.props import BoolProperty, PointerProperty


bl_info = {
    "name": "VisualFluidX3D",
    "author": "Davide Viganò",
    "version": (0, 1),
    "blender": (4, 1, 0),
    "location": "Preferences > Add-ons",
    "description": "Clones, compiles, and runs the FluidX3D addon from GitHub.",
    "warning": "",
    "doc_url": "",
    "category": "System",
}



# SET-UP---------------------------------------------------------------------------------------

def get_addon_dir():
    # Construct the path dynamically using Blender's version
    version_folder = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
    addon_dir = os.path.join(os.environ['APPDATA'], 'Blender Foundation', 'Blender', version_folder, 'scripts', 'addons', 'FluidX3D')
    return addon_dir



def git_clone_repository():
    # Repository URL
    repo_url = "https://github.com/ProjectPhysX/FluidX3D.git"
    # Directory where this script is located
    addon_dir = get_addon_dir()
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



class VISUALFLUIDX3D_OT_CloneRepo(bpy.types.Operator):
    """Clone FluidX3D Repository"""
    bl_idname = "wm.visual_fluidx3d_clone_repo"
    bl_label = "Clone FluidX3D Repository"
    bl_description = "Clones the latest version of the FluidX3D repository to the addon directory"

    def execute(self, context):
        git_clone_repository()
        return {'FINISHED'}
    
# ---------------------------------------------------------------------------------------------



# COMPILE AND RUN -----------------------------------------------------------------------------

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
    
    executable_path = os.path.join(get_addon_dir(), 'bin', 'FluidX3D.exe')
    # Command to open a new console window
    command = f'start cmd /K "{executable_path}"'
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Failed to run the application: {e}")



def compile_and_play_simulation():
    
    msbuild_path = find_msbuild()
    print("found msbuild")
    
    solution_path = os.path.join(get_addon_dir(), 'FluidX3D.sln')
    print("solution path: ",solution_path)
    
    compile_solution(msbuild_path, solution_path)
    print("Solution compiled")
    run_application()
    


class VISUALFLUIDX3D_OT_CompileAndPlay(bpy.types.Operator):
    """Compile and Run FluidX3D Simulation"""
    bl_idname = "wm.visual_fluidx3d_compile_and_play"
    bl_label = "Compile and Run Simulation"
    bl_description = "Starts the FluidX3D simulation with the current settings"

    def execute(self, context):
        compile_and_play_simulation()
        return {'FINISHED'}
    
# ---------------------------------------------------------------------------------------------



# UI PANNEL ----------------------------------------------------------------------------------- 

def is_repository_cloned(addon_dir):
    # Check if the directory exists and contains any files or subdirectories
    return os.path.exists(addon_dir) and any(os.listdir(addon_dir))



class VisualFluidX3DPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        addon_dir = get_addon_dir()

        if not is_repository_cloned(addon_dir):
            layout.operator(VISUALFLUIDX3D_OT_CloneRepo.bl_idname)
            
        layout.operator(VISUALFLUIDX3D_OT_CompileAndPlay.bl_idname)



class FLUIDX3D_PT_main_panel(bpy.types.Panel):
    bl_label = "FluidX3D"
    bl_idname = "FLUIDX3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'   # The space where the panel is located
    bl_region_type = 'UI'       # The region of the space (UI for the sidebar)
    bl_category = 'FluidX3D'    # The name of the tab where the panel will be located
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        addon_dir = get_addon_dir()

        if not is_repository_cloned(addon_dir):
            layout.operator("wm.visual_fluidx3d_clone_repo", text="Clone FluidX3D Repository", icon="DUPLICATE")
        layout.operator("wm.visual_fluidx3d_compile_and_play", text="Compile and Run", icon="PLAY")
 
 
 
class DUMMY_OT_button(bpy.types.Operator):
    """Handle Velocity Set Selection"""
    bl_idname = "dummy.button"
    bl_label = "Set Velocity"
    
    number: bpy.props.IntProperty()  # Identify which button is pressed

    def execute(self, context):
        # Here you would handle the action based on the 'number' property
        # This example just logs the button number
        velocity_sets = {
            1: "D2Q9",
            2: "D3Q15",
            3: "D3Q19",
            4: "D3Q27"
        }
        velocity_set = velocity_sets.get(self.number, "Unknown")
        self.report({'INFO'}, f"{velocity_set} selected")
        return {'FINISHED'}



class VelocitySettings(bpy.types.PropertyGroup):
    # Properties to manage the state of each button
    is_d2q9_active: bpy.props.BoolProperty(name="D2Q9 Active", default=False)
    is_d3q15_active: bpy.props.BoolProperty(name="D3Q15 Active", default=False)
    is_d3q19_active: bpy.props.BoolProperty(name="D3Q19 Active", default=False)
    is_d3q27_active: bpy.props.BoolProperty(name="D3Q27 Active", default=False)
    
    
    
class FLUIDX3D_PT_settings_subpanel(bpy.types.Panel):
    bl_label = "Settings"
    bl_idname = "FLUIDX3D_PT_settings_subpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FluidX3D'
    bl_parent_id = "FLUIDX3D_PT_main_panel"  
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        layout.label(text="Velocity set:",icon="OUTLINER_OB_FORCE_FIELD")
        
        # Velocity sets
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=False, align=True)
        
        grid.operator("dummy.button", text="D2Q9", icon="MATPLANE").number = 1
        grid.operator("dummy.button", text="D3Q15", icon="CUBE").number = 2
        grid.operator("dummy.button", text="D3Q19", icon="CUBE").number = 3
        grid.operator("dummy.button", text="D3Q27", icon="CUBE").number = 4
        
        layout.label(text="Relaxation:")

             
                
                
                
class FLUIDX3D_PT_docs_subpanel(bpy.types.Panel):
    bl_label = "Help"
    bl_idname = "FLUIDX3D_PT_docs_subpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FluidX3D'
    bl_parent_id = "FLUIDX3D_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        # Button for opening documentation
        layout.operator("wm.url_open", text="Documentation", icon="HELP").url = "https://github.com/ProjectPhysX/FluidX3D/blob/master/DOCUMENTATION.md"

# ---------------------------------------------------------------------------------------------        
        
        
        
# REGISTER UNREGISTER -------------------------------------------------------------------------

def register():
    bpy.utils.register_class(VISUALFLUIDX3D_OT_CloneRepo)
    bpy.utils.register_class(VISUALFLUIDX3D_OT_CompileAndPlay)
    bpy.utils.register_class(VisualFluidX3DPreferences)
    bpy.utils.register_class(FLUIDX3D_PT_main_panel)
    bpy.utils.register_class(FLUIDX3D_PT_settings_subpanel)
    bpy.utils.register_class(FLUIDX3D_PT_docs_subpanel)
    bpy.utils.register_class(DUMMY_OT_button)

def unregister():
    bpy.utils.register_class(DUMMY_OT_button)
    bpy.utils.unregister_class(FLUIDX3D_PT_docs_subpanel)
    bpy.utils.unregister_class(FLUIDX3D_PT_settings_subpanel)
    bpy.utils.unregister_class(FLUIDX3D_PT_main_panel)
    bpy.utils.unregister_class(VisualFluidX3DPreferences)
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_CompileAndPlay)
    bpy.utils.unregister_class(VISUALFLUIDX3D_OT_CloneRepo)
    
# ---------------------------------------------------------------------------------------------



if __name__ == "__main__":
    register()
