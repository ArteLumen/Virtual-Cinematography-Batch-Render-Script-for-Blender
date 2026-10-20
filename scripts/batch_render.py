"Virtual Cinematography Batch Render Script for Blender"

import os
import bpy


def setup_cinematic_camera(camera_obj):
  """Applies cinematic settings to a given camera object."""
  cam_data = camera_obj.data
  cam_data.lens = 35  
  cam_data.sensor_width = 36 
  cam_data.dof.use_dof = True  
  cam_data.dof.aperture_fstop = 2.8  


def main():
  
  output_dir = bpy.path.abspath("//../renders/")
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

 
  cameras = [obj for obj in bpy.data.objects if obj.type == "CAMERA"]

  if not cameras:
    print("Error: No cameras found in the scene!")
    return

  print(f"Found {len(cameras)} cameras. Starting batch render pipeline...")

  for cam in cameras:

    bpy.context.scene.camera = cam

    setup_cinematic_camera(cam)

    file_path = os.path.join(output_dir, f"shot_{cam.name}.png")
    bpy.context.scene.render.filepath = file_path

    print(f"Rendering: {cam.name} -> {file_path}")

    bpy.ops.render.render(write_still=True)

  print("Batch rendering process completed successfully.")


if __name__ == "__main__":
  
  main()
