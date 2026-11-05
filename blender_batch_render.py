"""Virtual Cinematography Batch Render Script for Blender

Renders one still image per camera in the current scene, applying cinematic
camera settings (lens, sensor, depth of field) for each shot.
The original camera settings are restored afterwards.

Usage (background):  blender -b scene.blend -P blender_batch_render.py
The .blend file must be saved first: the output folder is relative to it.
"""

import os
import re

import bpy

# --- Settings ---
FOCAL_LENGTH_MM = 35
SENSOR_WIDTH_MM = 36
F_STOP = 2.8
DEFAULT_FOCUS_DISTANCE_M = 5.0   # Used when a camera has no focus object
OUTPUT_FOLDER = "//../renders/"  # Relative to the .blend file


def sanitize_filename(name):
    """Replaces characters that are unsafe in file names."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def snapshot_camera(cam_data):
    """Saves the camera settings this script changes."""
    return {
        "lens": cam_data.lens,
        "sensor_width": cam_data.sensor_width,
        "use_dof": cam_data.dof.use_dof,
        "aperture_fstop": cam_data.dof.aperture_fstop,
        "focus_distance": cam_data.dof.focus_distance,
    }


def restore_camera(cam_data, saved):
    """Puts the saved camera settings back."""
    cam_data.lens = saved["lens"]
    cam_data.sensor_width = saved["sensor_width"]
    cam_data.dof.use_dof = saved["use_dof"]
    cam_data.dof.aperture_fstop = saved["aperture_fstop"]
    cam_data.dof.focus_distance = saved["focus_distance"]


def setup_cinematic_camera(camera_obj):
    """Applies cinematic settings to a given camera object."""
    cam_data = camera_obj.data
    cam_data.lens = FOCAL_LENGTH_MM
    cam_data.sensor_width = SENSOR_WIDTH_MM
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = F_STOP

    # Keep a focus object if the camera has one, otherwise use a fixed distance
    if cam_data.dof.focus_object is None:
        cam_data.dof.focus_distance = DEFAULT_FOCUS_DISTANCE_M


def main():
    scene = bpy.context.scene

    if not bpy.data.filepath:
        print("Error: Save the .blend file first. The output folder is relative to it.")
        return

    output_dir = bpy.path.abspath(OUTPUT_FOLDER)
    os.makedirs(output_dir, exist_ok=True)

    # Only cameras in the current scene (bpy.data.objects lists every scene)
    cameras = [obj for obj in scene.objects if obj.type == "CAMERA"]

    if not cameras:
        print("Error: No cameras found in the scene!")
        return

    print(f"Found {len(cameras)} cameras. Starting batch render pipeline...")

    # Remember the scene state so it can be restored at the end
    original_camera = scene.camera
    original_filepath = scene.render.filepath
    original_format = scene.render.image_settings.file_format

    scene.render.image_settings.file_format = "PNG"

    used_names = set()
    rendered = 0
    failed = []

    try:
        for index, cam in enumerate(cameras, start=1):
            saved = snapshot_camera(cam.data)
            try:
                scene.camera = cam
                setup_cinematic_camera(cam)

                # Unique, file-safe name for every shot
                base = f"shot_{sanitize_filename(cam.name)}"
                name, suffix = base, 2
                while name in used_names:
                    name = f"{base}_{suffix}"
                    suffix += 1
                used_names.add(name)

                file_path = os.path.join(output_dir, name + ".png")
                scene.render.filepath = file_path

                print(f"[{index}/{len(cameras)}] Rendering: {cam.name} -> {file_path}")
                bpy.ops.render.render(write_still=True)
                rendered += 1
            except Exception as error:  # One failed shot must not stop the batch
                print(f"Failed: {cam.name}: {error}")
                failed.append(cam.name)
            finally:
                restore_camera(cam.data, saved)
    finally:
        scene.camera = original_camera
        scene.render.filepath = original_filepath
        scene.render.image_settings.file_format = original_format

    if failed:
        print(f"Batch finished: {rendered} rendered, {len(failed)} failed: {', '.join(failed)}")
    else:
        print(f"Batch rendering process completed successfully ({rendered} shots).")


if __name__ == "__main__":
    main()
